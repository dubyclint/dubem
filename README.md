# ⚽ Football Match Predictor Bot

A Telegram bot that predicts football match outcomes using live match data, odds, sentiment, injuries, environment, and astrological influence.

## 🔧 Features

- Predicts match outcome: Win1 / Draw / Win2
- Accepts natural language input: "Team1 vs Team2", "Team1 vs Team2 on DATE"
- Fetches live match details via API-Sports
- Gets player motivation via news sentiment analysis
- Checks for key injuries
- Includes environmental and astrological effects

## 📦 Requirements

- Python 3.x
- Telegram Bot Token
- API Keys:
  - [API-Sports](https://api-sports.io/) 
  - [NewsAPI](https://newsapi.org/) 
  - [OpenWeatherMap](https://openweathermap.org/api) 

## 🛠️ Setup Instructions

1. Clone this repo
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables in `.env` or directly in Railway
4. Run locally: `python bot.py`
5. Or deploy on Render/Railway

## 🤖 Commands

- `/start` – Get welcome message
- Send any match query: "Team1 vs Team2" or "Team1 vs Team2 on DATE"

Made with ❤️ by [YourName]