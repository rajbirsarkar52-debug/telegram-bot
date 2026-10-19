import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("8571063350:AAFqB3pDPxcS3_UJSSjKBAIeSYDAokEWkmo")
OWNER_ID = int(os.environ.get("OWNER_ID", "8945771818"))

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Welcome to Bangla Hub Video Vault!\n\n"
        "Send me a video to create a private video link."
    )


async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message

    if not user or user.id != OWNER_ID:
        await message.reply_text("⛔ Only the bot owner can upload videos.")
        return

    video = message.video
    if not video:
        return

    await message.reply_text(
        "✅ Video received!\n"
        f"File ID: {video.file_id}\n"
        "Next step: connect secure video storage and link generation."
    )


def main():
    if not TOKEN or OWNER_ID == 0:
        raise RuntimeError("Set BOT_TOKEN and OWNER_ID first.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.VIDEO, receive_video)
    )
    app.run_polling()


if __name__ == "__main__":
    main()
    
