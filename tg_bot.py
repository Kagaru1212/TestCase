import asyncio
import os
import pandas as pd

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from datetime import datetime
from database.models import async_main, async_session, VacancyRequestHistory
from aiogram.filters import CommandStart, Command
from sqlalchemy import select
from aiogram.types import FSInputFile

# Loading environment variables from an .env file
load_dotenv()

# Obtaining a token from an environment variable
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

# Initialization of bot and dispatcher
bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()
SAVE_DIR = './saved_files'


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Hi. Use the /get_today_statistic command to get today's stats.")


@dp.message(Command('get_today_statistic'))
async def handle_get_today_statistic(message: types.Message):
    await send_excel_file(message.chat.id)


async def get_today_statistics():
    """This function takes all the records from the database for today and creates an Excel table from them."""

    async with async_session() as session:
        async with session.begin():
            # Getting today's data
            today = datetime.utcnow().date()
            result = await session.execute(select(VacancyRequestHistory).where(VacancyRequestHistory.timestamp >= today))
            data = result.scalars().all()

            # Create DataFrame
            df = pd.DataFrame([{
                'id': entry.id,
                'timestamp': entry.timestamp,
                'vacancy_count': entry.vacancy_count,
                'change': entry.change
            } for entry in data])

            if not os.path.exists(SAVE_DIR):
                os.makedirs(SAVE_DIR)

            excel_path = os.path.join(SAVE_DIR, 'today_statistics.xlsx')
            df.to_excel(excel_path, index=False)

            return excel_path


async def send_excel_file(chat_id):
    """This function sends an Exel table to the user."""

    excel_path = await get_today_statistics()

    # Create FSInputFile object from the file path
    input_file = FSInputFile(excel_path)

    # Sending the document to the user
    await bot.send_document(chat_id, document=input_file)

    # Deleting the temporary file
    os.remove(excel_path)


async def main():
    await async_main()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot shut down')
