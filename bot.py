import telegram
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import yt_dlp
import os

TOKEN = '7707789333:AAE_50ihmybcFPRbkhRvaNBEHlsufZfXOs8'

async def handle_message(update: Update, context):
    chat_id = update.message.chat_id
    message_text = update.message.text
    print(f"پیام دریافت شد: {message_text}")

    if "http" in message_text and "pornhub.com" in message_text:
        await update.message.reply_text("لینک رو گرفتم، آماده‌ام برای دانلود!")
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                await update.message.reply_text("در حال دانلود ویدیو...")
                print("دانلود شروع شد...")
                info = ydl.extract_info(message_text, download=True)
                video_file = ydl.prepare_filename(info)
                print(f"فایل دانلود شد: {video_file}")

            with open(video_file, 'rb') as video:
                await context.bot.send_video(chat_id=chat_id, video=video)
            os.remove(video_file)
            await update.message.reply_text("دانلود تموم شد! ویدیو برات فرستاده شد.")

        except Exception as e:
            error_msg = f"یه مشکلی پیش اومد: {str(e)}"
            print(error_msg)
            await update.message.reply_text(error_msg)
    else:
        await update.message.reply_text("لطفاً یه لینک از PornHub بفرست!")

def main():
    print("ربات داره شروع می‌کنه...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()