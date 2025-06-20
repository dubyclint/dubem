import numpy as np

def predict_tennis_match(player_a, player_b, match_date):
    h2h_matches = get_last_five_sets(player_a, player_b)
    if not h2h_matches:
        return default_tennis_prediction(player_a, player_b, match_date)

    # Simulated logic – use real stats later
    serve_a = get_player_serve_stats(player_a)
    serve_b = get_player_serve_stats(player_b)

    strength_a = 0.3 * serve_a["ace%"] + 0.2 * serve_a["serve%"] + 0.15 * serve_a["break%"] + 0.1 * len(h2h_matches)
    strength_b = 0.3 * serve_b["ace%"] + 0.2 * serve_b["serve%"] + 0.15 * serve_b["break%"] + 0.1 * len(h2h_matches)

    delta = strength_a - strength_b
    win_a = 1 / (1 + np.exp(-0.9 * delta))
    win_b = 1 - win_a

    return {
        "match": f"{player_a} vs {player_b}",
        "date": match_date,
        "sport": "Tennis",
        "winner": player_a if win_a > win_b else player_b,
        "win_percent": win_a if win_a > win_b else win_b,
        "set_scores": {
            "a_sets": 2,
            "b_sets": 1,
            "most_likely": "2–1"
        },
        "pattern_summary": "Player A dominates service games"
    }