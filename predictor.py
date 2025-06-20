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
    # Your existing code...