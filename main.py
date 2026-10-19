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
            # লিংকে ক্লিক করলে ইউজারকে ভিডিওটি পাঠানো হবে (ফরোয়ার্ড বা ডাউনলোড সুরক্ষা সহ)
            bot.send_video(
                message.chat.id, 
                file_id, 
                caption="🎥 আপনার কাঙ্ক্ষিত ভিডিওটি:",
                protect_content=True
            )
        except Exception as e:
            bot.reply_to(message, "⚠️ দুঃখিত, ভিডিওটি লোড করতে সমস্যা হয়েছে বা লিংকটি কাজ করছে না।")
    else:
        bot.reply_to(message, f"হ্যালো {user_name}! 👋\nআমাদের ভিডিও বটে আপনাকে স্বাগতম।")

@bot.message_handler(content_types=['video'])
def video_handler(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⛔ দুঃখিত, শুধুমাত্র বট ওনার এই বটে ভিডিও আপলোড করতে পারবেন।")
        return

    file_id = message.video.file_id
    bot_username = bot.get_me().username
    
    # চ্যানেলে পেস্ট করার জন্য ইউনিক লিংক তৈরি
    watch_link = f"https://t.me/{bot_username}?start=video_{file_id}"

    response_text = (
        "✅ ভিডিও সফলভাবে প্রসেস করা হয়েছে!\n\n"
        f"🔗 **চ্যানেলে দেওয়ার জন্য লিংক:**\n{watch_link}\n\n"
        "*(এই লিংকটি কপি করে আপনার টেলিগ্রাম চ্যানেলে পেস্ট করে দিন।)*"
    )

    bot.reply_to(message, response_text, parse_mode="Markdown")

if __name__ == "__main__":
    print("বট সফলভাবে চালু হচ্ছে...")
    bot.infinity_polling()
    
