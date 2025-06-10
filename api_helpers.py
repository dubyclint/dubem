# api_helpers.py

import requests
import os
from textblob import TextBlob

API_SPORTS_KEY = os.getenv("API_SPORTS_KEY")

def get_team_data(team_name):
    """
    Fetches team data from API-Sports based on team name.
    Returns None if not found.
    """
    if not team_name or not API_SPORTS_KEY:
        return None

    search_url = "https://v3.football.api-sports.io/teams" 
    params = {"name": team_name}
    headers = {"x-rapidapi-key": API_SPORTS_KEY}

    try:
        response = requests.get(search_url, headers=headers, params=params).json()
    except Exception as e:
        print(f"🚨 Error fetching team data for '{team_name}': {str(e)}")
        return None

    if response['results'] == 0:
        print(f"❌ No data found for team: {team_name}")
        return None

    team_id = response['response'][0]['team']['id']
    stats_url = "https://v3.football.api-sports.io/teams/statistics" 
    params = {"team": team_id, "season": "2024-2025"}

    try:
        return requests.get(stats_url, headers=headers, params=params).json()
    except Exception as e:
        print(f"🚨 Error fetching stats for '{team_name}': {str(e)}")
        return None

# Other helper functions below can remain unchanged
def analyze_sentiment(team_name):
    return {"score": 3.5, "statement": "Neutral sentiment"}

def check_injuries(team_name):
    return {"score": 4.5, "statement": "No major injuries reported"}

def assess_environment(location, date):
    return {"score": 4.0, "statement": "Good playing conditions"}

def calculate_astro_score(team1, team2, date):
    return {"score": 4.7, "statement": "Favorable cosmic alignment"}