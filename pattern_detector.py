# pattern_detector.py

import numpy as np

def detect_repeating_pattern(h2h_matches):
    q3_scores_a = [m["scores"]["home"]["third"] for m in h2h_matches]
    q3_scores_b = [m["scores"]["away"]["third"] for m in h2h_matches]

    count_a_high_q3 = sum(1 for s in q3_scores_a if s >= 20)
    count_b_high_q3 = sum(1 for s in q3_scores_b if s >= 20)

    std_a_q3 = np.std(q3_scores_a)
    std_b_q3 = np.std(q3_scores_b)

    summary = []
    if count_a_high_q3 >= 5:
        summary.append("Strong Q3 play (Home)")
    if count_b_high_q3 >= 5:
        summary.append("Strong Q3 play (Away)")
    if std_a_q3 <= 2:
        summary.append("Consistent Q3 scoring (Home)")
    if std_b_q3 <= 2:
        summary.append("Consistent Q3 scoring (Away)")

    return {
        "q3_trend": "High Q3 output" if count_a_high_q3 >= 5 else ("Consistent Q3" if std_a_q3 < 2 else "Balanced Q3 play"),
        "max_point_diff": max(abs(m["scores"]["home"]["total"] - m["scores"]["away"]["total"]) for m in h2h_matches),
        "pattern_summary": " | ".join(summary) if summary else "No strong trend"
    }

def detect_tennis_pattern(h2h_matches):
    set_wins_a = sum(1 for m in h2h_matches if m["winner"] == m["home"])
    set_wins_b = sum(1 for m in h2h_matches if m["winner"] == m["away"])

    serve_a = sum(1 for m in h2h_matches if m["home"]["aces"] > m["away"]["aces"])
    serve_b = sum(1 for m in h2h_matches if m["away"]["aces"] > m["home"]["aces"])

    return {
        "summary": f"Set dominance: {set_wins_a}:{set_wins_b}, Serve edge: {serve_a}:{serve_b}"
    }

def detect_hockey_pattern(h2h_matches):
    powerplay_a = sum(m["home"]["powerplays"] for m in h2h_matches)
    penalty_kill_b = sum(m["away"]["penalty_kills"] for m in h2h_matches)
    return {
        "summary": f"Powerplay edge: {powerplay_a} vs Penalty kills: {penalty_kill_b}"
    }

def detect_volleyball_pattern(h2h_matches):
    aces_a = sum(m["home"]["aces"] for m in h2h_matches)
    blocks_b = sum(m["away"]["blocks"] for m in h2h_matches)
    return {
        "summary": f"Ace serves: {aces_a}, Blocks: {blocks_b}"
    }

def detect_cricket_pattern(h2h_matches):
    run_rate_a = sum(m["home"]["run_rate"] for m in h2h_matches) / len(h2h_matches)
    wickets_b = sum(m["away"]["wickets"] for m in h2h_matches) / len(h2h_matches)

    return {
        "summary": f"Run rate: {run_rate_a:.1f}, Wickets: {wickets_b:.1f}"
    }