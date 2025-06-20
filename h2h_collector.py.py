import os
import requests
from datetime import datetime

def search_team(name, headers):
    url = f"https://v1.basketball.api-sports.io/teams?search={name}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    data = response.json()
    return data["response"][0]["team"]["id"] if data["results"] > 0 else None

def get_last_six_matches(team_a, team_b):
    try:
        headers = {
            'x-rapidapi-host': "v1.basketball.api-sports.io",
            'x-rapidapi-key': os.getenv("API_SPORTS_KEY")
        }

        team_a_id = search_team(team_a, headers)
        team_b_id = search_team(team_b, headers)

        if not team_a_id or not team_b_id:
            print(f"⚠️ Could not find IDs for {team_a} or {team_b}")
            return []

        url = f"https://v1.basketball.api-sports.io/games?h2h={team_a_id}-{team_b_id}"
        response = requests.get(url, headers=headers).json()

        matches = response.get("response", [])
        return matches[:6]

    except Exception as e:
        print("🚨 Error fetching H2H data:", str(e))
        return []