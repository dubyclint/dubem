# predictor.py

import re
from datetime import datetime
from h2h_collector import (
    search_basketball_team,
    search_football_team,
    search_tennis_player,
    search_hockey_team,
    search_volleyball_team,
    search_cricket_team
)

def extract_teams_and_date(text):
    text = text.strip().lower()

    # Remove time/date/league keywords
    text = re.sub(r'(at|on|\d{1,2}:\d{2}|\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|pm|am)', '', text).strip()

    # Split by 'vs' or 'against'
    vs_match = re.search(r'(vs|against)', text)
    if not vs_match:
        return {"error": "Could not find 'vs' or 'against'"}

    vs_index = vs_match.start()
    team_a = text[:vs_index].strip().title()
    team_b = text[vs_index + 2:].strip().title()

    # Clean up names
    team_a = re.sub(r'[^\w\s]', '', team_a).strip()
    team_b = re.sub(r'[^\w\s]', '', team_b).strip()

    return {
        "home_team": team_a,
        "away_team": team_b,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

def detect_sport(input_text):
    parsed = extract_teams_and_date(input_text)
    if "error" in parsed:
        return "unknown"

    home_team = parsed["home_team"]
    away_team = parsed["away_team"]

    # Try API-based detection
    if search_basketball_team(home_team) and search_basketball_team(away_team):
        return "basketball"
    elif search_football_team(home_team) and search_football_team(away_team):
        return "football"
    elif search_tennis_player(home_team) and search_tennis_player(away_team):
        return "tennis"
    elif search_hockey_team(home_team) and search_hockey_team(away_team):
        return "hockey"
    elif search_volleyball_team(home_team) and search_volleyball_team(away_team):
        return "volleyball"
    elif search_cricket_team(home_team) and search_cricket_team(away_team):
        return "cricket"
    else:
        return "unknown"

def predict_sports_match(input_text):
    sport = detect_sport(input_text)
    parsed = extract_teams_and_date(input_text)

    if "error" in parsed:
        return {"error": parsed["error"], "sport": sport}

    home_team = parsed["home_team"]
    away_team = parsed["away_team"]

    if sport == "basketball":
        from basketball_model import predict_basketball_match
        return predict_basketball_match(home_team, away_team, parsed["date"])
    elif sport == "football":
        from football_model import predict_football_match
        return predict_football_match(home_team, away_team, parsed["date"])
    elif sport == "tennis":
        from tennis_model import predict_tennis_match
        return predict_tennis_match(home_team, away_team, parsed["date"])
    elif sport == "hockey":
        from hockey_model import predict_hockey_match
        return predict_hockey_match(home_team, away_team, parsed["date"])
    elif sport == "volleyball":
        from volleyball_model import predict_volleyball_match
        return predict_volleyball_match(home_team, away_team, parsed["date"])
    elif sport == "cricket":
        from cricket_model import predict_cricket_match
        return predict_cricket_match(home_team, away_team, parsed["date"])
    else:
        return {"error": "Sport not supported yet.", "input": input_text}