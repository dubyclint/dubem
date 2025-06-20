# h2h_collector.py

import os
import requests

# Read API key from Railway or .env
RAPID_API_KEY = os.getenv("API_SPORTS_KEY")

def search_basketball_team(name):
    url = f"https://v1.basketball.api-sports.io/teams?search={name}"
    headers = {
        'x-rapidapi-host': "v1.basketball.api-sports.io",
        'x-rapidapi-key': RAPID_API_KEY
    }
    try:
        response = requests.get(url, headers=headers).json()
        return response['response'][0]['team']['name'] if response['results'] > 0 else None
    except:
        return None

def search_football_team(name):
    url = f"https://v1.football.api-sports.io/teams?search={name}"
    headers = {
        'x-rapidapi-host': "v1.football.api-sports.io",
        'x-rapidapi-key': RAPID_API_KEY
    }
    try:
        response = requests.get(url, headers=headers).json()
        return response['response'][0]['team']['name'] if response['results'] > 0 else None
    except:
        return None

# Add similar functions for tennis, hockey, volleyball, cricket... 