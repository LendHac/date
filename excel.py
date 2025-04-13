import pandas as pd
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from handlers import router
import asyncio
import logging
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
import handlers
import admin
import kb
API_TOKEN = '7208811563:AAEB952Om-IZ_pdT5ddry6kwMRR-bF2CIuM'  # Замените на токен вашего бота

days_of_week = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Воскресенье'
}

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Функция для получения расписания
# def get_schedule_for_today(excel_file, day_column, group_column):
#     df = pd.read_excel(excel_file)
#     df.columns = df.columns.str.strip()
    
#     today = datetime.now().weekday()  
#     today_schedule = df[df[day_column] == days_of_week[today]]

#     if not today_schedule.empty:
#         start_index = today_schedule.index[0]  
#         end_index = min(start_index + 20, len(df))  
        
#         groups = df.iloc[start_index:end_index][group_column].dropna().values.tolist()
#         return groups  
#     else:
#         return []  

# async def send_schedule(chat_id):
#     excel_file_path = 'sheldure.xlsx'  
#     day_column = 'Unnamed: 0'  
#     group_column = 'Unnamed: 3'  

#     schedule_today = get_schedule_for_today(excel_file_path, day_column, group_column)
    
#     if schedule_today:
#         message = "Расписание на сегодня:\n" + "\n".join(schedule_today)
#     else:
#         message = "Расписание на сегодня отсутствует."

#     await bot.send_message(chat_id, message)

# @router.message(Command("start"))
# async def start_command(message: Message):
#     await send_schedule(message.chat.id)
# async def main():
#     bot = Bot(token=config.BOT_TOKEN)
#     dp = Dispatcher(storage=MemoryStorage())
#     dp.include_routers(handlers.router, admin.router,kb.kb_router)
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(main())


# Функция для определения текущего урока
import pandas as pd
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.types import Message
from aiogram.utils import run
import asyncio

API_TOKEN = '7208811563:AAEB952Om-IZ_pdT5ddry6kwMRR-bF2CIuM'  # Замените на токен вашего бота

days_of_week = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Воскресенье'
}

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Функция для получения расписания
def get_schedule_for_today(excel_file, day_column, group_column):
    df = pd.read_excel(excel_file)
    df.columns = df.columns.str.strip()
    
    today = datetime.now().weekday()  
    today_schedule = df[df[day_column] == days_of_week[today]]

    return today_schedule

async def send_schedule(chat_id, day):
    excel_file_path = 'sheldure.xlsx'  
    day_column = 'Unnamed: 0'  
    group_column = 'Unnamed: 2'  
 # Предполагаем, что это колонка с временем начала уроков

    schedule_today = get_schedule_for_today(excel_file_path, day_column, group_column)
    
    
   


