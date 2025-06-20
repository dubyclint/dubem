# bot.py

import telebot
import os
from predictor import predict_sports_match

# Only load token when needed
TELEGRAM_BOT_TOKEN = os.getenv("8146384369:AAE-JQsC9M9ysYFhCTsUQqOlb8F3vGP4d_I")

try:
    if TELEGRAM_BOT_TOKEN:
        bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    else:
        bot = None
except Exception as e:
    bot = None
    print("🚨 Bot failed to initialize:", str(e))

@bot.message_handler(commands=['start', 'help']) if bot else lambda m: None
def send_welcome(message):
    if not TELEGRAM_BOT_TOKEN:
        bot.reply_to(message, "⚠️ Bot is missing TELEGRAM_BOT_TOKEN — please set it in environment.")
        return

    bot.reply_to(
        message,
        "🏀⚽🎾 Welcome to mazi chidubem Sports Match Predictor Bot!\n\n"
        "📥 Just send me a match query like:\n"
        "- \"PSG vs Botafogo\"\n"
        "- \"Crvena Zvezda vs Partizan\"\n"
        "- \"Man Utd vs Liverpool\""
    )

@bot.message_handler(func=lambda m: True) if bot else lambda m: None
def handle_message(message):
    if not TELEGRAM_BOT_TOKEN:
        bot.reply_to(message, "⚠️ Bot is missing TELEGRAM_BOT_TOKEN — please set it in environment.")
        return

    try:
        result = predict_sports_match(message.text.strip())
        if isinstance(result, dict) and "error" in result:
            bot.reply_to(message, f"⚠️ {result['error']}")
        else:
            output = format_prediction_output(result)
            bot.reply_to(message, output)
    except Exception as e:
        bot.reply_to(message, "🚨 Error processing request.")
        print("Prediction error:", str(e))

def format_prediction_output(data):
    return (
        f"🔮 Prediction for {data['match']} ({data['date']})\n"
        f"🏆 Winner: {data['winner']} ({data['win_percent']*100:.0f}%)\n"
        f"🔢 Score Range: {data['score_range']['home_min']}–{data['score_range']['home_max']} vs {data['score_range']['away_min']}–{data['score_range']['away_max']}\n"
        f"🔁 Reoccurring Patterns: {data['pattern_summary']}"
    )

if __name__ == "__main__":
    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        print("⚠️ TELEGRAM_BOT_TOKEN not set — bot will respond with error until defined.")
        exit()

    print("🚀 Starting bot...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print("❌ Bot failed to start:", str(e))
