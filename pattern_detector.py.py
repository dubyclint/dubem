# pattern_detector.py

import numpy as np

def detect_repeating_pattern(h2h_matches):
    """
    Detect reoccurring score patterns in first/second half.
    For football, analyze goals per half.
    """
    home_first_half_goals = [m["home"]["first_half"] for m in h2h_matches]
    away_first_half_goals = [m["away"]["first_half"] for m in h2h_matches]

    home_second_half_goals = [m["home"]["second_half"] for m in h2h_matches]
    away_second_half_goals = [m["away"]["second_half"] for m in h2h_matches]

    count_home_strong_start = sum(1 for g in home_first_half_goals if g >= 1)
    count_away_strong_start = sum(1 for g in away_first_half_goals if g >= 1)

    count_home_strong_finish = sum(1 for g in home_second_half_goals if g >= 1)
    count_away_strong_finish = sum(1 for g in away_second_half_goals if g >= 1)

    summary = []

    if count_home_strong_start >= 4:
        summary.append("Strong starters (Home)")
    if count_away_strong_start >= 4:
        summary.append("Strong starters (Away)")

    if count_home_strong_finish >= 4:
        summary.append("Late-game finishers (Home)")
    if count_away_strong_finish >= 4:
        summary.append("Late-game finishers (Away)")

    max_diff = max(abs(m["home"]["total"] - m["away"]["total"]) for m in h2h_matches)

    return {
        "start_trend": "Strong start" if count_home_strong_start >= 4 else ("Balanced" if count_home_strong_start == count_away_strong_start else "Weak start"),
        "finish_trend": "Strong finish" if count_home_strong_finish > count_away_strong_finish else ("Balanced" if count_home_strong_finish == count_away_strong_finish else "Weak finish"),
        "max_goal_diff": max_diff,
        "pattern_summary": " | ".join(summary) if summary else "No strong trend"
    }