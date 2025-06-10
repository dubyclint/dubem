# bot.py

import telebot
import os
from predictor import predict_match_enhanced

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "⚽ Welcome to the Football Match Predictor Bot!\n\n"
        "📥 Just send me a match query like:\n"
        "- \"Adelaide Raiders vs FK Beograd\"\n"
        "- \"Team1 vs Team2 on 2025-06-09\"\n"
        "- \"Real Madrid at Camp Nou vs Barcelona\""
    )

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        result = predict_match_enhanced(message.text.strip())
        if isinstance(result, dict) and "error" in result:
            bot.reply_to(message, result["error"])
        else:
            output = format_prediction_output(result)
            bot.reply_to(message, output)
    except Exception as e:
        bot.reply_to(message, "⚠️ Error processing request.")
        print("Prediction error:", str(e))

def format_prediction_output(data):
    return (
        f"🔮 Prediction for {data['match']} ({data['date']})\n"
        f"📍 Location: {data['location']}\n\n"
        f"🔴 Motivation: {data['home_team_analysis']['motivation']['statement']}\n"
        f"🟡 Injuries: {data['home_team_analysis']['injury_impact']['statement']}\n"
        f"🔵 Environment: {data['home_team_analysis']['environment']['statement']}\n"
        f"🟣 Astrology: {data['home_team_analysis']['astrology']['statement']}\n\n"
        f"📊 Outcome Probabilities:\n"
        f"Win {data['match'].split(' vs ')[0]}: {data['prediction']['Win1']:.0%}\n"
        f"Draw: {data['prediction']['Draw']:.0%}\n"
        f"Win {data['match'].split(' vs ')[1]}: {data['prediction']['Win2']:.0%}"
    )

print("🚀 Bot started...")
bot.infinity_polling()