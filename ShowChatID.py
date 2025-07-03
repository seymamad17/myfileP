import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest
from telegram.error import TelegramError

# توکن ربات و آیدی ادمین (به‌صورت مستقیم در کد)
TOKEN = "8122143072:AAGdRlT8O7HaZXNpQLApp7ZeuoYWtx0T1is"
ADMIN_ID = 7507284671  # آیدی عددی شما

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    try:
        chat_id = update.message.chat_id
        await update.message.reply_text(
            f"سلام! آیدی چت شما: {chat_id}\n"
            "برای گرفتن لینک چت یه کاربر، از این دستور استفاده کنید:\n"
            "/getlink <chat_id>\n"
            "مثال: /getlink 987654321"
        )
    except TelegramError as e:
        print(f"خطا در ارسال پیام: {e}")
        await context.bot.send_message(chat_id=chat_id, text="خطا در ارتباط با تلگرام. لطفاً دوباره امتحان کنید.")

# /getlink
async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    chat_id = update.message.chat_id

    if chat_id != ADMIN_ID:
        await update.message.reply_text("فقط ادمین می‌تونه از این دستور استفاده کنه!")
        return

    args = context.args
    if len(args) != 1:
        await update.message.reply_text("لطفاً دستور رو درست وارد کنید:\n/getlink <chat_id>")
        return

    try:
        target_chat_id = int(args[0])
        chat_link = f"tg://user?id={target_chat_id}"
        await update.message.reply_text(
            f"لینک چت برای آیدی {target_chat_id}:\n{chat_link}\n"
            "این لینک رو تو تلگرام باز کنید تا چت با کاربر شروع بشه."
        )
    except ValueError:
        await update.message.reply_text("آیدی چت باید یه عدد باشه!")
    except TelegramError as e:
        print(f"خطا در ارسال پیام: {e}")
        await update.message.reply_text("خطا در ارتباط با تلگرام. لطفاً دوباره امتحان کنید.")

# اجرای ربات
async def main():
    print("ربات داره شروع می‌کنه...")
    try:
        request = HTTPXRequest(connection_timeout=30, read_timeout=30, write_timeout=30)
        application = Application.builder().token(TOKEN).http_request(request).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("getlink", get_link))

        await application.run_polling()
    except TelegramError as e:
        print(f"خطا در راه‌اندازی ربات: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
