from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Your Telegram bot token (kept exactly as you provided)
import os
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# FAQ dictionary
faq = {
    "What is your name?": "I'm your friendly bot! 🤖",
    "How are you?": "I'm doing great, thanks for asking! 😄",
    "What can you do?": "I can answer a few questions. Try asking me about my name, or anything else listed in the FAQ.",
    "Who created you?": "I was created by a smart developer like you! 👨‍💻",
}

# Create keyboard layout (each question as a button)
faq_keyboard = [[q] for q in faq.keys()]

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(faq_keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text(
        "👋 Hi there! Choose a question from the list below:",
        reply_markup=keyboard
    )

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "Here's a list of questions you can ask me:\n\n"
    for question in faq:
        help_text += f"- {question}\n"
    await update.message.reply_text(help_text)

# Handle FAQ button presses / text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    if user_message in faq:
        response = faq[user_message]
    else:
        response = "❌ Sorry, I don't know that one. Please choose from the list."
    
    # Always re-show keyboard
    await update.message.reply_text(
        response,
        reply_markup=ReplyKeyboardMarkup(faq_keyboard, resize_keyboard=True, one_time_keyboard=False)
    )

# Handle unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👉 Please type /start to begin and see the FAQ menu.")

# Main
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.COMMAND, unknown))

print("Bot is running…")
app.run_polling()
