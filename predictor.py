import re
from datetime import datetime
from api_helpers import (
    get_team_data,
    analyze_sentiment,
    check_injuries,
    assess_environment,
    calculate_astro_score
)

def extract_teams_and_date(text):
    # Try match date
    date_match = re.search(r'\b\d{4}-\d{2}-\d{2}\b', text)
    date = date_match.group() if date_match else datetime.now().strftime("%Y-%m-%d")

    # Try location
    location_match = re.search(r'at ([\w\s]+)', text)
    location = location_match.group(1).strip() if location_match else None

    # Extract team names
    vs_split = re.split(r' vs ', text, flags=re.IGNORECASE)
    if len(vs_split) < 2:
        vs_split = re.split(r' against ', text, flags=re.IGNORECASE)
    if len(vs_split) < 2:
        return {"error": "Could not parse team names"}

    home_team = vs_split[0].strip()
    away_team = re.sub(r'(on|\d{4}-\d{2}-\d{2}|at [\w\s]+)', '', vs_split[1]).strip()

    return {
        "home_team": home_team,
        "away_team": away_team,
        "date": date,
        "location": location or "Default Stadium"
    }

def calculate_strength_enhanced(features):
    base_strength = (
        0.3 * features["wins_ratio"] +
        0.2 * features["goal_diff"] +
        0.1 * features["form_score"]
    )
    enhancements = (
        0.1 * features.get("motivation", {"score": 3})["score"] +
        0.1 * features.get("injury_impact", {"score": 3})["score"] +
        0.1 * features.get("environment", {"score": 3})["score"] +
        0.1 * features.get("astrology", {"score": 3})["score"]
    ) / 5
    return base_strength + enhancements

def predict_match_enhanced(input_text):
    parsed = extract_teams_and_date(input_text)
    if "error" in parsed:
        return parsed

    home_team = parsed["home_team"]
    away_team = parsed["away_team"]
    date = parsed["date"]
    location = parsed["location"]

    from api_helpers import get_team_data
    home_data = get_team_data(home_team, os.getenv("API_SPORTS_KEY"))
    away_data = get_team_data(away_team, os.getenv("API_SPORTS_KEY"))

    if not home_data or not away_data:
        return {"error": "Could not find team data"}

    def extract_features(team_data):
        stats = team_data['response']
        fixtures = stats['fixtures']
        goals = stats['goals']
        win_ratio = fixtures['wins']['total'] / max(1, fixtures['total'])
        goal_diff = goals['for']['total']['total'] - goals['against']['total']['total']
        form = sum([1 if r == 'W' else 0 for r in stats['form'][-5:]]) / 5
        return {
            "wins_ratio": win_ratio,
            "goal_diff": goal_diff,
            "form_score": form
        }

    home_features = extract_features(home_data)
    away_features = extract_features(away_data)

    home_features["motivation"] = analyze_sentiment(home_team)
    home_features["injury_impact"] = check_injuries(home_team)
    home_features["environment"] = assess_environment(location, date=date)
    home_features["astrology"] = calculate_astro_score(home_team, away_team, date=date)

    away_features["motivation"] = analyze_sentiment(away_team)
    away_features["injury_impact"] = check_injuries(away_team)
    away_features["environment"] = assess_environment(location, date=date)
    away_features["astrology"] = calculate_astro_score(away_team, home_team, date=date)

    home_strength = calculate_strength_enhanced(home_features)
    away_strength = calculate_strength_enhanced(away_features)

    delta = home_strength - away_strength
    win1_prob = 1 / (1 + np.exp(-0.5 * delta))
    win2_prob = 1 / (1 + np.exp(0.5 * delta))
    draw_prob = 1 - win1_prob - win2_prob + 0.1
    total = win1_prob + win2_prob + draw_prob

    return {
        "match": f"{home_team} vs {away_team}",
        "date": date,
        "location": location,
        "home_team_analysis": home_features,
        "away_team_analysis": away_features,
        "prediction": {
            "Win1": win1_prob / total,
            "Draw": draw_prob / total,
            "Win2": win2_prob / total
        }
    }