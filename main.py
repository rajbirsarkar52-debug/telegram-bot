import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = "8571063350:AAFqB3pDPxcS3_UJSSjKBAIeSYDAokEWkmo"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ১. /start কমান্ড দিলে ক্যাটাগরি বাটন দেখাবে
@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ Premium Video", callback_data="cat_premium")],
        [InlineKeyboardButton(text="🌍 English Video", callback_data="cat_english")],
        [InlineKeyboardButton(text="🔥 Exclusive Movie", callback_data="cat_exclusive")]
    ])
    await message.answer(
        "🎬 **Video Hub-এ স্বাগতম!**\n\nনিচের ক্যাটাগরি থেকে আপনার পছন্দের অপشنটি সিলেক্ট করুন:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# ২. ইউজার যেকোনো ক্যাটাগরিতে ক্লিক করলে যা হবে
@dp.callback_query(F.data.startswith("cat_"))
async def category_handler(callback: types.CallbackQuery):
    cat_type = callback.data.split("_")[1]
    
    if cat_type == "premium":
        text = "⭐ আপনি **Premium Video** সিলেক্ট করেছেন। আপনার পছন্দের ভিডিও পেতে নিচের লিংকে ক্লিক করুন:"
    elif cat_type == "english":
        text = "🌍 আপনি **English Video** সিলেক্ট করেছেন। ভিডিও দেখতে নিচের লিংকে ক্লিক করুন:"
    else:
        text = "🔥 আপনি **Exclusive Movie** সিলেক্ট করেছেন। ভিডিও দেখতে নিচের লিংকে ক্লিক করুন:"

    # এখানে আপনার শর্টনার বা অ্যাড লিংক দিতে পারেন
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Click Here to Watch/Download", url="https://t.me/+HaiN5CNmsHExMDk1")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
