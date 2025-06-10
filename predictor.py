# predictor.py

from datetime import datetime
from api_helpers import get_team_data
from openai_helper import extract_match_details

def predict_match_enhanced(input_text):
    parsed = extract_match_details(input_text)
    if "error" in parsed:
        return parsed

    home_team = parsed.get("home_team")
    away_team = parsed.get("away_team")
    date = parsed.get("date") or datetime.now().strftime("%Y-%m-%d")
    location = parsed.get("location") or None  # Now optional

    home_data = get_team_data(home_team)
    away_data = get_team_data(away_team)

    if not home_data or not away_data:
        return {"error": "Could not fetch match data for the given teams."}

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
        "location": location or "Unknown Venue",
        "home_team_analysis": home_features,
        "away_team_analysis": away_features,
        "prediction": {
            "Win1": win1_prob / total,
            "Draw": draw_prob / total,
            "Win2": win2_prob / total
        }
    }