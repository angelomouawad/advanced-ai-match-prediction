# Technical Report Premier League Match Predictor

**Student:** Angelo  
**Course:** Advanced AI UCLL 2026  
**Repository:** [github.com/angelomouawad/advanced-ai-match-prediction](https://github.com/angelomouawad/advanced-ai-match-predictionO)

---

## 1. Introduction

Football match prediction is a hard problem. Even professional models rarely exceed 60% accuracy because football has a lot of randomness. The goal of this project was to build a system that takes two team names and predicts whether the home team wins, the away team wins, or if it ends in a draw.

I chose to combine a neural network with an LLM sentiment analysis model. The idea is that match statistics alone don't capture everything because injuries, suspensions, and team morale matter too. So I used pre match news articles scored by an NLP model as extra input features.

---

## 2. Data

**Sources:**
- **football-data.co.uk**: free CSVs with Premier League results and stats from 2000 to 2026. Each row is one match with columns for goals, shots, corners, cards, and betting odds.
- **Understat**: expected goals (xG) data via a Python API wrapper. Available from 2014/15 onwards.
- **The Guardian API**: football news articles fetched per team per match for seasons 2020 onwards.

**Preprocessing:**
- Combined 26 CSV files into one dataset (Around 9,700 matches). Some files used different encodings (latin-1, windows-1252) which caused errors that had to be handled per file.
- Dropped columns with more than 90% missing values (attendance, woodwork hits, offsides, booking points).
- Filtered to 2014 onwards for model training since xG data only starts there (Around 4,000 matches).
- Dropped all post match statistics (shots, corners, cards) since those aren't available before a match happens.
- Engineered rolling features over the last 5 matches per team: average form (points per game), goals scored, goals conceded, xG, and head to head win rate.
- Sentiment scores from Guardian articles were generated using a HuggingFace RoBERTa model and stored as two columns: home_sentiment and away_sentiment (range -1.0 to +1.0).

**Challenges:**
- Some older CSVs had inconsistent column counts and encoding issues.
- The Guardian API has a 500 request/day limit on the free tier. With around 2,400 matches × 2 teams, collection had to be ongoing daily via a checkpoint system.
- Team names differ between sources (for example "Manchester United" vs "Man United"), requiring manual mapping.

---

## 3. Model and Methods

**Sentiment pipeline (LLM component):**  
For each match from 2020 onwards, the Guardian API is queried for articles about each team published in the 5 days before the match. These headlines are passed through `cardiffnlp/twitter-roberta-base-sentiment`, a RoBERTa model fine-tuned on social media text. It outputs a label (negative / neutral / positive) with a confidence score, which is converted to a single number between -1.0 and +1.0. This value is a real input feature to the neural network, removing it would change the predictions.

**Neural network:**  
A multi-layer perceptron built in PyTorch with the following architecture:

```
Input (11 features)
→ Linear(128) → BatchNorm → ReLU → Dropout(0.3)
→ Linear(64)  → BatchNorm → ReLU → Dropout(0.3)
→ Linear(32)  → ReLU
→ Linear(3)   → Softmax
```

- Optimizer: Adam (lr=0.001, weight_decay=1e-4)
- Loss: CrossEntropyLoss with class weights [1.0, 1.5, 1.0] to prevent the model from ignoring draws
- Learning rate scheduler: ReduceLROnPlateau (halves lr when validation loss plateaus)
- Training: 100 epochs, best weights saved by validation loss

**Web app:**  
A Flask backend loads the saved model weights and serves predictions via a REST API. The frontend is a single HTML/CSS/JS page where you select two teams and get a prediction with probability bars, head to head stats, recent form, and xG averages.

---

## 4. Results and Evaluation

| Metric | Value |
|--------|-------|
| Test accuracy | Around 55% |
| Random baseline | 33% |
| Home Win recall | Around 0.75 |
| Draw recall | Around 0.20 |
| Away Win recall | Around 0.50 |

The model performs well above random. Home wins are predicted most reliably, which makes sense since home advantage is a real pattern in football (Around 46% of Premier League matches are home wins). Draws are the hardest to predict, this is a known challenge in football prediction. Increasing the draw class weight from 1.0 to 1.5 improved draw recall from 0.01 to around 0.20 without hurting overall accuracy too much.

The training curves show the model learns quickly in the first 15 epochs and then stabilises. There is no significant overfitting, validation loss stays close to training loss throughout.

---

## 5. Contributions

**What I built myself:**
- Full data pipeline (loading, cleaning, merging multiple sources)
- Feature engineering (rolling stats, head to head, sentiment integration)
- Neural network architecture and training loop
- Flask web application and frontend

**What I found online:**
- football-data.co.uk datasets
- Understat Python wrapper for xG data
- `cardiffnlp/twitter-roberta-base-sentiment` model from HuggingFace

**What I used GenAI for:**
- Debugging errors during data loading and merging
- Suggestions on model architecture and class weighting strategy

---

## 6. Challenges and Future Work

**Challenges:**
- Getting all data sources to align on team names and dates took a lot of trial and error.
- The Guardian API rate limit means sentiment data collection is still running. Currently about 60% of the 2020–2026 matches have sentiment scores.
- The model plateaus early, suggesting the features have limited predictive power, football is genuinely hard to predict.

**Future improvements:**
- Complete the sentiment dataset, this should improve accuracy once all matches are scored
- Add more features: league position, days since last match, travel distance for away games
- Add live data so upcoming fixtures can be predicted with current form, not historical averages
- Allow users to manually input sentiment context (e.g. "key player injured") before predicting
