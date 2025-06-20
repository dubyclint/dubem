# predictor.py

import re
from datetime import datetime
from fuzzywuzzy import process

def detect_sport(input_text):
    text = input_text.lower()
    
    if any(kw in text for kw in ["basketball", "nba", "ceb", "mpbl", "lkl", "lublin"]):
        return "basketball"
    elif any(kw in text for kw in ["soccer", "football", "premier", "liga", "bundesliga"]):
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
    from config import KNOWN_TEAMS
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