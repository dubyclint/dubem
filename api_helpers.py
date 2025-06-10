# api_helpers.py

def assess_environment(location, date):
    if not location:
        return {"score": 3.5, "statement": "Location unknown, using average conditions"}
    # Fetch weather/pitch quality based on location/date
    return {"score": 4.0, "statement": "Good playing conditions"}

def calculate_astro_score(team1, team2, date):
    # Use current date if none provided
    actual_date = date or datetime.now().strftime("%Y-%m-%d")
    # Perform zodiac, moon phase, planetary alignment here
    return {"score": 4.7, "statement": "Favorable cosmic alignment"}