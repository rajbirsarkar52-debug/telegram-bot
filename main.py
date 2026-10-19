import os
import telebot

TOKEN = "8571063350:AAH95ipjXuplUW7AZGk1B-1iL85I1bVDrqY"
OWNER_ID = 8945771818

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_name = message.from_user.first_name
    
    command_args = message.text.split()
    if len(command_args) > 1 and command_args[1].startswith("video_"):
        file_id = command_args[1].replace("video_", "")
        try:
            # protect_content=True er maddhome keu video ti forward ba download korte parbe na
            bot.send_video(
                message.chat.id, 
                file_id, 
                caption="🎥 Apnar kankkhito video ti (Protected Content):",
                protect_content=True
            )
        except Exception as e:
            bot.reply_to(message, "⚠️ Dukkito, video ti load korte somossa hoyeche ba link ti somoy shesh.")
    else:
        bot.reply_to(message, f"Hello {user_name}! 👋\nAmader video bot e apnake swagotom.")

@bot.message_handler(content_types=['video'])
def video_handler(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⛔ Dukkhito, shudhu bot owner ei bot e video upload korte parben.")
        return

    file_id = message.video.file_id
    bot_username = bot.get_me().username
    
    watch_link = f"https://t.me/{bot_username}?start=video_{file_id}"

    response_text = (
        "✅ Apnar video ti safolvabe save hoyeche!\n\n"
        f"🔗 **Video Dekhar Link:**\n{watch_link}\n\n"
        f"📌 **File ID:**\n`{file_id}`"
    )

    bot.reply_to(message, response_text, parse_mode="Markdown")

if __name__ == "__main__":
    print("Bot safolvabe cholche...")
    bot.infinity_polling()
                
