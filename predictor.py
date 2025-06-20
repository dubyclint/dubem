# predictor.py

import re
from datetime import datetime
from fuzzywuzzy import process

# Local imports
from config import KNOWN_TEAMS
from basketball_model import predict_basketball_match
from football_model import predict_football_match

def detect_sport(input_text):
    text = input_text.lower()

    if any(kw in text for kw in ["basketball", "ceb", "mpbl", "lkl"]):
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

    # Remove time, date, league keywords
    text = re.sub(r'(at|on|\d{1,2}:\d{2}|\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|pm|am)', '', text).strip()

    # Split by 'vs' or 'against'
    vs_match = re.search(r'(vs|against)', text)
    if not vs_match:
        return {"error": "Could not find 'vs' or 'against'"}

    vs_index = vs_match.start()
    team_a = text[:vs_index].strip().title()
    team_b = text[vs_index + 2:].strip().title()

    # Clean up team names
    team_a = re.sub(r'[^\w\s]', '', team_a).strip()
    team_b = re.sub(r'[^\w\s]', '', team_b).strip()

    # Fuzzy match known teams
    team_a = match_team(team_a, KNOWN_TEAMS)
    team_b = match_team(team_b, KNOWN_TEAMS)

    if not team_a or not team_b:
        return {"error": f"Could not match teams: {team_a} vs {team_b}"}

    # Date extraction
    date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', text)
    if date_match:
        date = date_match.group(1)
    else:
        date_match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', text)
        if date_match:
            day, month, year = date_match.group(1).split('/')
            date = f"{year}-{month}-{day}"
        else:
            date = datetime.now().strftime("%Y-%m-%d")

    return {
        "home_team": team_a,
        "away_team": team_b,
        "date": date
    }

def match_team(name, known_teams, threshold=80):
    best_match, score = process.extractOne(name, known_teams)
    return best_match if score >= threshold else None

def predict_sports_match(input_text):
    sport = detect_sport(input_text)
    parsed = extract_teams_and_date(input_text)

    if "error" in parsed:
        return {"error": parsed["error"], "sport": sport}

    home_team = parsed["home_team"]
    away_team = parsed["away_team"]

    if sport == "basketball":
        return predict_basketball_match(home_team, away_team, parsed["date"])
    elif sport == "football":
        return predict_football_match(home_team, away_team, parsed["date"])
    elif sport == "tennis":
        return predict_tennis_match(home_team, away_team, parsed["date"])
    elif sport == "hockey":
        return predict_hockey_match(home_team, away_team, parsed["date"])
    elif sport == "volleyball":
        return predict_volleyball_match(home_team, away_team, parsed["date"])
    elif sport == "cricket":
        return predict_cricket_match(home_team, away_team, parsed["date"])
    else:
        return {"error": "Sport not supported yet.", "input": input_text}