# tennis_model.py

import numpy as np
from h2h_collector import search_tennis_player, get_last_five_sets

WEIGHTS = {
    "serve_rating": 0.3,
    "return_rating": 0.2,
    "form": 0.15,
    "head_to_head": 0.1,
    "surface_preference": 0.1,
    "fatigue_index": -0.05,
    "coach_strategy": 0.05,
    "pattern_confidence": 0.17
}

def calculate_strength_score(stats):
    return sum(w * stats.get(k, 0) for k, w in WEIGHTS.items())

def predict_tennis_match(player_a, player_b, match_date):
    api_home = search_tennis_player(player_a)
    api_away = search_tennis_player(player_b)

    if not api_home or not api_away:
        return {"error": f"Player not found: {player_a} vs {player_b}"}

    h2h_matches = get_last_five_sets(api_home, api_away)
    if not h2h_matches:
        return default_tennis_prediction(api_home, api_away, match_date)

    patterns = detect_tennis_pattern(h2h_matches)
    
    team_a_stats = get_player_stats(api_home)
    team_b_stats = get_player_stats(api_away)

    strength_a = calculate_strength_score(team_a_stats)
    strength_b = calculate_strength_score(team_b_stats)

    delta = strength_a - strength_b
    win_a = 1 / (1 + np.exp(-0.9 * delta))
    win_b = 1 - win_a

    return {
        "match": f"{api_home} vs {api_away}",
        "date": match_date,
        "sport": "Tennis",
        "winner": api_home if win_a > win_b else api_away,
        "win_percent": win_a if win_a > win_b else win_b,
        "set_scores": {
            "a_sets": int((strength_a - 0.5) * 3),
            "b_sets": int((strength_b - 0.5) * 3)
        },
        "pattern_summary": patterns["summary"],
        "probabilities": {
            "Win A": win_a,
            "Draw": 0.0,
            "Win B": win_b
        }
    }

def get_player_stats(player_name):
    return {
        "serve_rating": 8.0,
        "return_rating": 7.5,
        "form": 4.0,
        "head_to_head": 0.5,
        "surface_preference": 7.0,
        "fatigue_index": 0.1,
        "coach_strategy": 7.2
    }