from flask import Flask, request, jsonify, send_from_directory
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import pickle
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder="templates")

BASE      = os.path.dirname(os.path.abspath(__file__))
DATA_DIR  = os.path.join(BASE, "..", "Data")

MODEL_PATH    = os.path.join(DATA_DIR, "model.pth")
SCALER_PATH   = os.path.join(DATA_DIR, "scaler.pkl")
FEATURES_PATH = os.path.join(DATA_DIR, "feature_cols.pkl")
DATA_PATH     = os.path.join(DATA_DIR, "model_data.csv")

class MatchPredictor(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128), nn.BatchNorm1d(128), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(128, 64),        nn.BatchNorm1d(64),  nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(64, 32),         nn.ReLU(),
            nn.Linear(32, 3)
        )
    def forward(self, x):
        return self.net(x)

with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)
with open(FEATURES_PATH, "rb") as f:
    FEATURE_COLS = pickle.load(f)

model = MatchPredictor(input_dim=len(FEATURE_COLS))
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

data = pd.read_csv(DATA_PATH)
data["Date"] = pd.to_datetime(data["Date"])

ALL_TEAMS = sorted(set(data["HomeTeam"].unique()) | set(data["AwayTeam"].unique()))

def get_team_stats(team, is_home):
    home_m = data[data["HomeTeam"] == team].tail(5)
    away_m = data[data["AwayTeam"] == team].tail(5)
    all_m  = pd.concat([home_m, away_m]).sort_values("Date").tail(5)
    prefix = "home" if is_home else "away"
    return {
        f"{prefix}_form"   : float(all_m[f"{prefix}_form"].mean()),
        f"{prefix}_gf_avg" : float(all_m[f"{prefix}_gf_avg"].mean()),
        f"{prefix}_ga_avg" : float(all_m[f"{prefix}_ga_avg"].mean()),
        f"{prefix}_xg_avg" : float(all_m[f"{prefix}_xg_avg"].mean()),
    }

def get_h2h(home_team, away_team, n=5):
    mask = (
        ((data["HomeTeam"] == home_team) & (data["AwayTeam"] == away_team)) |
        ((data["HomeTeam"] == away_team) & (data["AwayTeam"] == home_team))
    )
    prev = data[mask].tail(n)
    if len(prev) == 0:
        return 0.4
    wins = sum(
        1 for _, r in prev.iterrows()
        if (r["HomeTeam"] == home_team and r["target"] == 0) or
           (r["AwayTeam"] == home_team and r["target"] == 2)
    )
    return round(wins / len(prev), 4)

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/api/teams")
def teams():
    return jsonify(ALL_TEAMS)

@app.route("/api/predict", methods=["POST"])
def predict():
    body      = request.json
    home_team = body.get("home_team")
    away_team = body.get("away_team")

    if not home_team or not away_team:
        return jsonify({"error": "Both teams required"}), 400
    if home_team == away_team:
        return jsonify({"error": "Teams must be different"}), 400
    if home_team not in ALL_TEAMS or away_team not in ALL_TEAMS:
        return jsonify({"error": "Unknown team"}), 400

    home_stats = get_team_stats(home_team, is_home=True)
    away_stats = get_team_stats(away_team, is_home=False)
    h2h        = get_h2h(home_team, away_team)

    features = {**home_stats, **away_stats, "h2h_home_winrate": h2h}
    if "home_sentiment" in FEATURE_COLS:
        features["home_sentiment"] = 0.0
        features["away_sentiment"] = 0.0

    X = np.array([[features[c] for c in FEATURE_COLS]], dtype=np.float32)
    X = scaler.transform(X)

    with torch.no_grad():
        probs = torch.softmax(model(torch.tensor(X)), dim=1).numpy()[0]

    def get_form_string(team):
        recent = data[
            (data["HomeTeam"] == team) | (data["AwayTeam"] == team)
        ].sort_values("Date").tail(5)
        results = []
        for _, r in recent.iterrows():
            if r["HomeTeam"] == team:
                results.append("W" if r["target"] == 0 else ("D" if r["target"] == 1 else "L"))
            else:
                results.append("W" if r["target"] == 2 else ("D" if r["target"] == 1 else "L"))
        return results

    return jsonify({
        "home_team"  : home_team,
        "away_team"  : away_team,
        "home_win"   : round(float(probs[0]) * 100, 1),
        "draw"       : round(float(probs[1]) * 100, 1),
        "away_win"   : round(float(probs[2]) * 100, 1),
        "prediction" : ["home", "draw", "away"][int(probs.argmax())],
        "h2h"        : round(h2h * 100),
        "home_form"  : get_form_string(home_team),
        "away_form"  : get_form_string(away_team),
        "home_xg"    : round(home_stats["home_xg_avg"], 2),
        "away_xg"    : round(away_stats["away_xg_avg"], 2),
        "home_gf"    : round(home_stats["home_gf_avg"], 2),
        "away_gf"    : round(away_stats["away_gf_avg"], 2),
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
