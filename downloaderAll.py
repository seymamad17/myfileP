from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن ربات رو اینجا بذار
TOKEN = "7707789333:AAE_50ihmybcFPRbkhRvaNBEHlsufZfXOs8"

# وقتی /start فرستاده میشه
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! خوش اومدی 😊")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
