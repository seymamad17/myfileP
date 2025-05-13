import telegram
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import yt_dlp
import os
import asyncio  # برای تاخیر 60 ثانیه‌ای

TOKEN = '7707789333:AAE_50ihmybcFPRbkhRvaNBEHlsufZfXOs8'

# متغیر برای ذخیره پیام درصد دانلود
progress_message = None

# تابع برای آپدیت درصد دانلود
async def download_progress(d, update, context):
    global progress_message
    chat_id = update.message.chat_id

    if d['status'] == 'downloading':
        # محاسبه درصد دانلود
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
        message_text = f"در حال دانلود: {percent:.2f}%"

        # اگه پیام قبلی وجود داره، ویرایشش کن، وگرنه یه پیام جدید بفرست
        if progress_message:
            try:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=progress_message.message_id,
                    text=message_text
                )
            except:
                # اگه خطایی توی ویرایش بود، پیام جدید بفرست
                progress_message = await context.bot.send_message(chat_id=chat_id, text=message_text)
        else:
            progress_message = await context.bot.send_message(chat_id=chat_id, text=message_text)

    elif d['status'] == 'finished':
        # وقتی دانلود تموم شد، پیام درصد رو پاک کن
        if progress_message:
            await context.bot.delete_message(chat_id=chat_id, message_id=progress_message.message_id)

async def handle_message(update: Update, context):
    global progress_message
    chat_id = update.message.chat_id
    message_text = update.message.text
    print(f"پیام دریافت شد: {message_text}")

    if "http" in message_text and "pornhub.com" in message_text:
        await update.message.reply_text("لینک رو گرفتم، آماده‌ام برای دانلود!")
        try:
            # ریست کردن پیام درصد
            progress_message = None

            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.%(ext)s',
                'progress_hooks': [lambda d: asyncio.run_coroutine_threadsafe(download_progress(d, update, context), asyncio.get_event_loop())],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("دانلود شروع شد...")
                info = ydl.extract_info(message_text, download=True)
                video_file = ydl.prepare_filename(info)
                print(f"فایل دانلود شد: {video_file}")

            # ارسال ویدیو
            with open(video_file, 'rb') as video:
                video_message = await context.bot.send_video(chat_id=chat_id, video=video)
            os.remove(video_file)

            # اطلاع‌رسانی به کاربر
            await update.message.reply_text("ویدیو فرستاده شد! 60 ثانیه وقت داری سیوش کنی، وگرنه حذف می‌شه.")

            # صبر کردن 60 ثانیه و بعد حذف پیام و ویدیو
            await asyncio.sleep(60)
            await context.bot.delete_message(chat_id=chat_id, message_id=video_message.message_id)
            await update.message.reply_text("ویدیو حذف شد! اگه سیو نکردی، دوباره لینک رو بفرست.")

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


