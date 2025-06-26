# predictor.py

import re
from datetime import datetime

def extract_sport_and_teams(text):
    text = text.strip().lower()

    # Format: "sport: teamA vs teamB"
    match = re.match(r'(\w+):\s*(.+)', text)
    if not match:
        return {"error": "Invalid format. Use 'sport: teamA vs teamB'"}

    sport = match.group(1).strip()
    teams_text = match.group(2).strip()

    # Remove time/date/league keywords
    teams_text = re.sub(r'(at|on|\d{1,2}:\d{2}|\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|pm|am)', '', teams_text).strip()

    # Split by 'vs' or 'against'
    vs_match = re.search(r'(vs|against)', teams_text)
    if not vs_match:
        return {"error": "Could not find 'vs' or 'against'"}

    vs_index = vs_match.start()
    team_a = teams_text[:vs_index].strip().title()
    team_b = teams_text[vs_index + 2:].strip().title()

    # Clean up names
    team_a = re.sub(r'[^\w\s]', '', team_a).strip()
    team_b = re.sub(r'[^\w\s]', '', team_b).strip()

    return {
        "sport": sport,
        "home_team": team_a,
        "away_team": team_b,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

def predict_sports_match(input_text):
    parsed = extract_sport_and_teams(input_text)

    if "error" in parsed:
        return {"error": parsed["error"]}

    sport = parsed["sport"]
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
        return {"error": f"Sport '{sport}' not supported yet."}