import logging
import sqlite3
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# --- YOUR CONFIGURATION ---
BOT_TOKEN = "8895245187:AAHInautCUg8ZhRwRZUJxiA46Cwk9YrxT50"  # এখানে BotFather এর আসল টোকেন বসান
ADMIN_ID = 7214396585
CHANNEL_ID = -1004362017596
CHANNEL_LINK = "https://t.me/+HaiN5CNmsHExMDk1"
REQUIRED_REFERRALS = 2

# যে ভিডিওটি Unlock হলে ইউজার পাবে তার File ID
FULL_VIDEO_FILE_ID = "YOUR_VIDEO_FILE_ID_HERE" 

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            referrer_id INTEGER,
            joined_channel INTEGER DEFAULT 0,
            referral_count INTEGER DEFAULT 0,
            unlocked INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_user(user_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(user_id, referrer_id=None):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, referrer_id) VALUES (?, ?)', (user_id, referrer_id))
    conn.commit()
    conn.close()

# --- BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    referrer_id = None

    if args and args[0].isdigit():
        referrer_id = int(args[0])
        if referrer_id == user_id:
            referrer_id = None

    add_user(user_id, referrer_id)

    keyboard = [
        [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ CHECK JOIN", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome!\n\nভিডিওটি unlock করতে প্রথমে আমাদের channel-এ Join করুন।",
        reply_markup=reply_markup
    )

async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            
            user_data = get_user(user_id)
            if user_data and user_data[1] and user_data[2] == 0:
                referrer_id = user_data[1]
                conn = sqlite3.connect('bot_database.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET joined_channel = 1 WHERE user_id = ?', (user_id,))
                cursor.execute('UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?', (referrer_id,))
                conn.commit()
                
                cursor.execute('SELECT referral_count, unlocked FROM users WHERE user_id = ?', (referrer_id,))
                ref_data = cursor.fetchone()
                conn.close()

                if ref_data:
                    ref_count, ref_unlocked = ref_data
                    try:
                        await context.bot.send_message(
                            chat_id=referrer_id,
                            text=f"🎉 আপনার রেফারেল লিংকে একজন নতুন ইউজার যুক্ত হয়েছে!\nProgress: {ref_count}/{REQUIRED_REFERRALS}"
                        )
                    except Exception:
                        pass
                    
                    if ref_count >= REQUIRED_REFERRALS and not ref_unlocked:
                        await send_unlocked_video(context, referrer_id)

            await show_referral_status(query, context, user_id)
        else:
            await query.edit_message_text("❌ আগে channel-এ Join করুন। তারপর আবার CHECK JOIN চাপুন।", 
                                          reply_markup=query.message.reply_markup)
    except Exception as e:
        await query.message.reply_text("ERROR: Bot-কে চ্যানেলে Admin করতে হবে।")

async def show_referral_status(query, context, user_id):
    user_data = get_user(user_id)
    ref_count = user_data[3] if user_data else 0
    bot_info = await context.bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={user_id}"

    if ref_count >= REQUIRED_REFERRALS:
        await query.edit_message_text("🎉 আপনার Task ইতিমধ্যে সম্পন্ন হয়েছে!")
        await send_unlocked_video(context, user_id)
        return

    share_text = f"https://t.me/share/url?url={ref_link}&text=ভিডিওটি%20দেখতে%20বটটি%20স্টার্ট%20করুন!"
    keyboard = [[InlineKeyboardButton("📤 SHARE LINK", url=share_text)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = (
        f"🔓 ভিডিও Unlock করতে {REQUIRED_REFERRALS} জন নতুন user-কে আপনার referral link দিয়ে Bot-এ আনুন।\n\n"
        f"🔗 Your Link: {ref_link}\n"
        f"📊 Progress: {ref_count}/{REQUIRED_REFERRALS}"
    )
    await query.edit_message_text(msg, reply_markup=reply_markup)

async def send_unlocked_video(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET unlocked = 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

    caption = "🎉 Unlock Complete!\nআপনার ভিডিও নিচে দেওয়া হলো।\n⏰ ভিডিওটি ৩০ মিনিট পর স্বয়ংক্রিয়ভাবে মুছে যাবে।"
    
    msg = await context.bot.send_video(chat_id=user_id, video=FULL_VIDEO_FILE_ID, caption=caption)
    
    context.job_queue.run_once(
        delete_message_job, 
        when=1800, 
        data={'chat_id': user_id, 'message_id': msg.message_id}
    )

async def delete_message_job(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    try:
        await context.bot.delete_message(chat_id=job.data['chat_id'], message_id=job.data['message_id'])
    except Exception as e:
        print(f"Failed to delete message: {e}")

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM users WHERE unlocked = 1')
    unlocked_users = cursor.fetchone()[0]
    conn.close()

    await update.message.reply_text(
        f"📊 **Admin Statistics**\n\n"
        f"👥 Total Users: {total_users}\n"
        f"🔓 Video Unlocked: {unlocked_users}"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", admin_stats))
    app.add_handler(CallbackQueryHandler(check_join_callback, pattern="^check_join$"))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
