import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command

# এনভায়রনমেন্ট বা Render থেকে টোকেন ও ওনার আইডি নেওয়ার জন্য
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "8945771818"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"হ্যালো {user_name}! 👋\n"
        "আমাদের ভিডিও বটে আপনাকে স্বাগতম।"
    )

@dp.message(F.video)
async def video_handler(message: types.Message):
    # শুধু নির্দিষ্ট ওনার আইডি চেক করার সিকিউরিটি
    if message.from_user.id != OWNER_ID:
        await message.reply("⛔ দুঃখিত, শুধুমাত্র বট ওনার এই বটে ভিডিও আপলোড করতে পারবেন।")
        return

    file_id = message.video.file_id
    await message.reply(
        "✅ আপনার ভিডিওটি সফলভাবে টেলিগ্রাম সার্ভারে জমা হয়েছে!\n\n"
        f"📌 **File ID:**\n`{file_id}`",
        parse_mode="Markdown"
    )

async def main():
    print("বট সফলভাবে চালু হচ্ছে...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("বট বন্ধ করা হয়েছে।")
        
