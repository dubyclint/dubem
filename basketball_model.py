from h2h_collector import get_last_six_matches
from pattern_detector import detect_repeating_pattern
import numpy as np

WEIGHTS = {
    "starter_skill": 0.3,
    "bench_depth": 0.1,
    "defensive_efficiency": 0.15,
    "motivation": 0.1,
    "h2h_win_percent": 0.08,
    "turnover_rate": -0.05,
    "rebound_margin": 0.07,
    "key_player_impact": 0.07,
    "injury_status": -0.05,
    "coach_strategy": 0.05,
    "pattern_confidence": 0.17
}

def calculate_strength_score(team_data):
    return sum(w * team_data.get(k, 0) for k, w in WEIGHTS.items())

def predict_basketball_match(team_a, team_b, match_date):
    h2h_matches = get_last_six_matches(team_a, team_b)
    if not h2h_matches:
        return default_basketball_prediction(team_a, team_b, match_date)

    patterns = detect_repeating_pattern(h2h_matches)
    strength_a = calculate_strength_score(get_team_stats(team_a))
    strength_b = calculate_strength_score(get_team_stats(team_b))

    delta = strength_a - strength_b
    win_a = 1 / (1 + np.exp(-0.8 * delta))
    win_b = 1 - win_a

    return {
        "match": f"{team_a} vs {team_b}",
        "date": match_date,
        "sport": "Basketball",
        "winner": team_a if win_a > win_b else team_b,
        "win_percent": win_a if win_a > win_b else win_b,
        "score_range": {
            "home_min": int((strength_a - 0.5) * 10),
            "home_max": int((strength_a + 0.5) * 10),
            "away_min": int((strength_b - 0.5) * 10),
            "away_max": int((strength_b + 0.5) * 10),
            "total_min": int((strength_a + strength_b - 1.0) * 10),
            "total_max": int((strength_a + strength_b + 1.0) * 10)
        },
        "pattern_summary": patterns["summary"],
        "probabilities": {
            "Win A": win_a,
            "Draw": 0.0,
            "Win B": win_b
        }
    }

def get_team_stats(team_name):
    # Replace with actual stats lookup later
    return {
        "starter_skill": 8.0,
        "bench_depth": 7.0,
        "defensive_efficiency": 7.5,
        "motivation": 4.0,
        "h2h_win_percent": 0.5,
        "turnover_rate": 13.0,
        "rebound_margin": 3.0,
        "key_player_impact": 7.8,
        "injury_status": 0.1,
        "coach_strategy": 7.2
    }