# bot.py

import telebot
import os
import html
from predictor import predict_sports_match

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Telegram bot token not found in environment — set TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "<b>🏀⚽🎾 Welcome to Sports Match Predictor Bot!</b>\n\n"
        "📥 Just send me a match query like:\n"
        "- <code>Crvena Zvezda vs Partizan</code>\n"
        "- <code>PSG vs Botafogo</code>\n"
        "- <code>Rafael Nadal vs Novak Djokovic</code>"
    )
    bot.reply_to(message, welcome_text, parse_mode='html')

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        result = predict_sports_match(message.text.strip())
        if isinstance(result, dict) and "error" in result:
            bot.reply_to(message, f"⚠️ {html.escape(result['error'])}", parse_mode='html')
        else:
            output = format_prediction_output(result)
            bot.reply_to(message, output, parse_mode='html')
    except Exception as e:
        bot.reply_to(message, "🚨 Error processing request.", parse_mode='html')
        print("Prediction error:", str(e))

def format_prediction_output(data):
    return (
        f"<b>🔮 Prediction for {html.escape(data['match'])} ({data['date']})</b>\n"
        f"<b>🏆 Winner:</b> {html.escape(data['winner'])} (<i>{data['win_percent']*100:.0f}%</i>)\n"
        f"<b>🔢 Score Range:</b> {data['score_range']['home_min']}–{data['score_range']['home_max']} vs {data['score_range']['away_min']}–{data['score_range']['away_max']}\n"
        f"<b>🔁 Reoccurring Patterns:</b> {html.escape(data['pattern_summary'])}"
    )

if __name__ == "__main__":
    print("🚀 Starting bot...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print("❌ Bot failed to start:", str(e))