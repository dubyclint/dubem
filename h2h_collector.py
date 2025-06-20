import os
import requests

RAPID_API_KEY = os.getenv("5350ef98397a7c1f987ab8fd442085e4")

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
