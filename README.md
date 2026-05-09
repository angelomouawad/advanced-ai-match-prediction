# Premier League Match Predictor

> An AI-powered football match outcome predictor combining a PyTorch neural network, xG data, and NLP sentiment analysis to predict Premier League results.

---

## Project Overview

This project predicts the outcome of Premier League matches (Home Win / Draw / Away Win) using a hybrid AI pipeline:

- **Structured match data**: 26 seasons of Premier League statistics from football-data.co.uk (2000–2026)
- **Expected Goals (xG)**: fetched from Understat via API for seasons 2014/15 onwards
- **NLP Sentiment Analysis**: pre match Guardian news articles scored using a HuggingFace RoBERTa transformer model, used as input features to the neural network
- **PyTorch Neural Network**: a multi layer perceptron trained on engineered features to classify match outcomes

The project is presented through a Flask web application where you can select any two Premier League teams and get a live prediction with probability bars, head to head history, recent form, and attack statistics.

---

## AI Architecture

```
Pre-match news (Guardian API)
        ↓
RoBERTa Sentiment Model (HuggingFace)
        ↓
Sentiment score [-1.0 → +1.0]
        ↓
Combined with structured features:
  • Rolling form (last 5 games)
  • Goals scored / conceded avg
  • xG average
  • Head-to-head win rate
        ↓
PyTorch MLP Neural Network
  Input(11) → Linear(128) → BN → ReLU → Dropout(0.3)
            → Linear(64)  → BN → ReLU → Dropout(0.3)
            → Linear(32)  → ReLU
            → Linear(3)   → Softmax
        ↓
Prediction: Home Win / Draw / Away Win
```

**Model performance:** 51% test accuracy (vs 33% random baseline)

---

## Project Structure

```
VSC - Project/
├── Data/
│   ├── Premier League/        # Raw CSV files per season (2000–2026)
│   ├── combined_data.csv      # Merged dataset with xG + sentiment
│   ├── model_data.csv         # Engineered features ready for training
│   ├── model.pth              # Saved PyTorch model weights
│   ├── scaler.pkl             # Fitted StandardScaler
│   ├── feature_cols.pkl       # Feature column names
│   ├── training_curves.png    # Loss and accuracy plots
│   ├── confusion_matrix.png   # Test set confusion matrix
│   ├── feature_distributions.png
│   ├── dataset_overview.png
│   └── missing_values.png
├── Src/
│   ├── app.py                 # Flask backend
│   ├── templates/
│   │   └── index.html         # Frontend web app
│   └── match_results.ipynb    # Full data pipeline & training notebook
├── .env                       # API keys (not committed)
├── .env.example               # Example env file
└── requirements.txt
```

---

## Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Copy the example env file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
GUARDIAN_KEY=your-guardian-api-key-here
```

Get a free Guardian API key at [open-platform.theguardian.com](https://open-platform.theguardian.com)

### 4. Run the notebook

Open `Src/match_results.ipynb` in Jupyter and run all cells in order:

| Cell | Description |
|------|-------------|
| 1 | Load & combine all season CSVs |
| 2 | Fetch xG data from Understat |
| 3 | Load HuggingFace sentiment model |
| 4 | Fetch & score pre-match news sentiment (Guardian API) |
| 5 | Clean data & engineer features |
| 6 | Train PyTorch neural network |
| 7 | Plot training curves & confusion matrix |

> The sentiment cell (4) fetches 500 articles/day due to the free API tier. I had to run it daily until complete, however I already saved the results so this cell DOES NOT have to be executed.

### 5. Run the web app

```bash
cd Src
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Data Sources

| Source | Data | Coverage |
|--------|------|----------|
| [football-data.co.uk](https://www.football-data.co.uk) | Match results, stats, betting odds | 2000–2026 |
| [Understat](https://understat.com) | Expected Goals (xG) | 2014–2026 |
| [The Guardian API](https://open-platform.theguardian.com) | Pre-match news articles | 2020–2026 |

---

## API Keys Required

| API | Purpose | Free Tier | Sign Up |
|-----|---------|-----------|---------|
| Guardian API | Fetch pre-match news | 500 req/day | [open-platform.theguardian.com](https://open-platform.theguardian.com) |

---

## Model Details

- **Algorithm:** Multi-Layer Perceptron (PyTorch)
- **Input features:** 11 (9 without sentiment, 11 with)
- **Output classes:** Home Win (0), Draw (1), Away Win (1)
- **Training split:** 70% train / 15% validation / 15% test
- **Optimizer:** Adam (lr=0.001, weight_decay=1e-4)
- **Loss:** CrossEntropyLoss with class weights [1.0, 1.5, 1.0]
- **Epochs:** 100
- **Test accuracy:** 51% (random baseline: 33%)

---

## Author

**Angelo**
UCLL Advanced AI Project 2026
