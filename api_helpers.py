# api_helpers.py
import requests
import os
from textblob import TextBlob

def get_team_data(team_name, api_key):
    search_url = "https://v3.football.api-sports.io/teams" , "https://www.forebet.com/en/football-predictions"
    params = {"name": team_name}
    headers = {"x-rapidapi-key": api_key}

    response = requests.get(search_url, headers=headers, params=params).json()
    if response['results'] == 0:
        return None

    team_id = response['response'][0]['team']['id']
    stats_url = f"https://v3.football.api-sports.io/teams/statistics" 
    params = {"team": team_id, "season": "2024-2025"}
    return requests.get(stats_url, headers=headers, params=params).json()

def analyze_sentiment(team_name):
    try:
        url = "https://newsapi.org/v2/everything" 
        params = {"q": team_name, "language": "en", "sortBy": "relevancy"}
        headers = {"Authorization": f"Bearer {os.getenv('NEWS_API_KEY')}"}
        response = requests.get(url, params=params, headers=headers).json()
        articles = response.get("articles", [])
        texts = [a["title"] + ". " + a["description"] for a in articles[:5]]
        combined_text = " ".join(texts)
        polarity = TextBlob(combined_text).sentiment.polarity
        score = round((polarity + 1) * 2.5, 1)
        statement = "High motivation" if score >= 4 else "Moderate motivation" if score >= 2.5 else "Low motivation"
        return {"score": score, "statement": statement}
    except:
        return {"score": 3, "statement": "Sentiment analysis failed"}

def check_injuries(team_name):
    return {"score": 5, "statement": "No major injuries reported."}

def assess_environment(location, date):
    return {"score": 4.5, "statement": "Good pitch, mild weather."}

def calculate_astro_score(team1, team2, date):
    return {"score": 4.8, "statement": "Strong cosmic alignment."}
