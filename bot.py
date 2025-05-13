from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import subprocess
import os
import asyncio

TOKEN = "7707789333:AAE_50ihmybcFPRbkhRvaNBEHlsufZfXOs8"

DOWNLOAD_DIR = "downloads"

async def handle_spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("🎧 در حال دریافت آهنگ... لطفاً صبر کن.")

    try:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        subprocess.run(["spotdl", url, "--output", DOWNLOAD_DIR], check=True)

        for file in os.listdir(DOWNLOAD_DIR):
            if file.endswith(".mp3"):
                filepath = os.path.join(DOWNLOAD_DIR, file)

                sent_msg = await update.message.reply_audio(
                    audio=open(filepath, 'rb'),
                    caption="⏳ این آهنگ بعد از 20 ثانیه پاک میشه! اگه می‌خوای سیوش کن."
                )

                await asyncio.sleep(20)
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=sent_msg.message_id)
                os.remove(filepath)
                break

    except Exception as e:
        await update.message.reply_text("❌ مشکلی در دریافت آهنگ پیش اومد.")
        print("خطا:", e)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'https?://open\.spotify\.com/track/.*'), handle_spotify))
    app.run_polling()

if __name__ == "__main__":
    main()

