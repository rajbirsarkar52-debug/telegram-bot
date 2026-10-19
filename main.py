import os
import telebot

TOKEN = "8571063350:AAH95ipjXuplUW7AZGk1B-1iL85I1bVDrqY"
OWNER_ID = 8945771818

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_name = message.from_user.first_name
    
    # লিংকে কোনো ভিডিওর কোড (payload) আছে কি না তা চেক করা
    command_args = message.text.split()
    if len(command_args) > 1 and command_args[1].startswith("video_"):
        file_id = command_args[1].replace("video_", "")
        try:
            # লিংকে ক্লিক করলে সরাসরি সেই ভিডিওটি ইউজারের কাছে পাঠিয়ে দেওয়া
            bot.send_video(message.chat.id, file_id, caption="🎥 আপনার কাঙ্ক্ষিত ভিডিওটি:")
        except Exception as e:
            bot.reply_to(message, "⚠️ দুঃখিত, ভিডিওটি লোড করতে সমস্যা হয়েছে বা লিংকটি মেয়াদোত্তীর্ণ।")
    else:
        bot.reply_to(message, f"হ্যালো {user_name}! 👋\nআমাদের ভিডিও বটে আপনাকে স্বাগতম।")

@bot.message_handler(content_types=['video'])
def video_handler(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⛔ দুঃখিত, শুধুমাত্র বট ওনার এই বটে ভিডিও আপলোড করতে পারবেন।")
        return

    file_id = message.video.file_id
    bot_username = bot.get_me().username
    
    # ইউনিক ভিডিও লিংক তৈরি
    watch_link = f"https://t.me/{bot_username}?start=video_{file_id}"

    response_text = (
        "✅ আপনার ভিডিওটি সফলভাবে সেভ হয়েছে!\n\n"
        f"🔗 **ভিডিও দেখার লিংক:**\n{watch_link}\n\n"
        f"📌 **File ID:**\n`{file_id}`"
    )

    bot.reply_to(message, response_text, parse_mode="Markdown")

if __name__ == "__main__":
    print("বট সফলভাবে চালু হচ্ছে...")
    bot.infinity_polling()
    
