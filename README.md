# ⚽ Football Match Predictor Bot

A Telegram bot that predicts football match outcomes using:
- 🧠 Natural language understanding via OpenAI (GPT)
- 🌐 Live match data from API-Sports
- 🧑‍🔬 Player motivation (via sentiment analysis)
- ⚠️ Injury impact
- 🌤️ Environmental conditions
- 🌕 Astrological influence

---

## 🔥 Key Features

- Accepts natural language input like:
  - "Will Barcelona beat Real Madrid next week?"
  - "Who wins if Liverpool plays PSG in Paris on July 5th?"
- Uses GPT to extract team names, date, location
- Fetches live stats from [API-Sports](https://api-sports.io/) 
- Predicts outcome using a hybrid model of ML + cosmic alignment
- Returns full breakdown of probabilities with explanations

---

## 📦 Requirements

- Python 3.x
- Telegram Bot Token
- API Keys:
  - [API-Sports](https://api-sports.io/) 
  - [OpenAI API](https://platform.openai.com/)  (for GPT)
  - [NewsAPI](https://newsapi.org/)  *(optional)*
  - [OpenWeatherMap](https://openweathermap.org/api)  *(optional)*

---

## 🛠️ Setup Instructions

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/football-predictor.git 
   cd football-predictor