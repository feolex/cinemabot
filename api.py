import asyncio
import logging
import os
import sys

from aiogram import Bot, types, html
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import F

from dotenv import load_dotenv

nested_dir = os.path.join(os.path.dirname(__file__), 'controllerLayer')
sys.path.append(nested_dir)

from controllerLayer import MainController  # noqa: E402

load_dotenv()
BOT_TOKEN = os.environ['BOT_TOKEN']
dp = Dispatcher()

mainController = MainController()

GREETING_STRING: str = ("\nI am simple cinemabot"
                        " to search direct links to watch movies\n"
                        "and main info about them!")
HELP_STRING: str = (
    "\n /start or /help - to show this help-message"
    "\n just send film name(without any \'\' or \"\") to search link"
    "\n /history - show your searching history"
    "\n /stats - show your searching stats"
    "\n /clear - clear your searching history")


@dp.message(F.text == "/help")
async def help_line(message: types.Message):
    await message.answer(HELP_STRING)


@dp.message(CommandStart())
@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer(f"Hello, {html.bold(message.from_user.username)}!\n"
                         + GREETING_STRING)
    await message.answer(HELP_STRING)


@dp.message(F.text == "/history")
async def history(message: types.Message):
    await message.answer(
        await mainController.get_history(message.from_user.id))


@dp.message(F.text == "/stats")
async def stats(message: types.Message):
    await message.answer(await mainController.get_stats(message.from_user.id))


@dp.message(F.text == "/clear")
async def clear(message: types.Message) -> None:
    await message.answer(
        await mainController.clear_history(message.from_user.id))


@dp.message()
async def search(message: types.Message) -> None:
    """
    @param message: message with text to film to search
    @return link to search film
    """
    await message.answer(
        await mainController.get_film(message.text, message.from_user.id))


async def main() -> None:
    bot = Bot(token=BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
