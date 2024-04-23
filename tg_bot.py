import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.formatting import Text, Spoiler, Bold

from dotenv import load_dotenv

# Load .env and get the value of "TOKEN"
load_dotenv()
TOKEN = os.getenv("TOKEN")

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot):

    # Use aiogram formatting classes and .as_kwargs() method
    content = Text("Hi, ", Bold(message.from_user.full_name), " 👋\n\n" "I am INSTABOT. Send me reels from Instagram, and I'll get you it here as video 😏\n\nInstructions:\n", 
                   Spoiler("I only work with links that look like this https://www.instagram.com/reel/abcd/?igsh=abcd==\n\n"))
    await bot.send_message(message.from_user.id, **content.as_kwargs())
            
@dp.message()
async def echo_handler(message: types.Message):
    given_link = message.text
    if 'instagram' in given_link:
        first_part = given_link.split('instagram')[0]
        third_part = given_link.split('instagram')[1]
        new_link = first_part + 'ddinstagram' + third_part
        
        # Use markdown_v2 markup for formatting
        await message.answer(f"[Video from INSTABOT]({new_link})")
        print(f"\nGenerated this link for {message.from_user.full_name}: {new_link}")
    
    else:
        await message.answer(f"This one does not look like a valid Instagram link 😳")
        print(f"\nFailed to generate a link for {message.from_user.full_name} from this: {given_link}")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    # Don't need pending updates so drop them:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())