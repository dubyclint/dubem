# predictor.py

import re
from datetime import datetime

def detect_sport(input_text):
    text = input_text.lower()
    
    if any(kw in text for kw in ["basketball", "nba", "ceb", "mpbl", "lkl"]):
        return "basketball"
    elif any(kw in text for kw in ["football", "soccer", "premier", "liga", "bundesliga"]):
        return "football"
    elif any(kw in text for kw in ["tennis", "atp", "wta", "grand slam"]):
        return "tennis"
    elif any(kw in text for kw in ["ice hockey", "nhl", "khl", "liiga"]):
        return "hockey"
    elif any(kw in text for kw in ["volleyball", "vnl", "cev"]):
        return "volleyball"
    elif any(kw in text for kw in ["cricket", "odi", "t20", "ipl"]):
        return "cricket"
    else:
        return "unknown"


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