# openai_helper.py

import openai
import os

openai.api_key = os.getenv( "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")

def extract_match_details(user_query):
    prompt = (
        "You are a football match assistant. From the following message, extract:\n"
        "- Home team name\n"
        "- Away team name\n"
        "- Optional match date (e.g., 'next Saturday', '2025-06-09')\n"
        "- Optional location/stadium\n\n"
        f"User says: {user_query}\n\n"
        "Respond strictly in JSON format with keys: home_team, away_team, date, location."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        return eval(content)  # Convert string JSON to dict
    except Exception as e:
        print("OpenAI error:", str(e))
        return {"error": "Could not parse input"}
