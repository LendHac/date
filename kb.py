import schedule # type: ignore
from aiogram import types, F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, callback_query
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import pandas as pd
from aiogram.types import CallbackQuery
from datetime import datetime
from bd import data_set
import sqlite3
import re
import threading
import time
import asyncio
from main import bot
from datetime import date
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import json
from g4f.client import Client

days_of_week = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Воскресенье'
}

file_loc = 'sheldure.xlsx'
df = pd.read_excel(file_loc, index_col=None,  usecols="C:X")
data =df.iloc[[4]]
but = data.values.flatten()

def split_subjects(subject):
    
    if not isinstance(subject, str):
        return [{"subject": subject}]  
    
    parts = re.split(r'\n? ?Ауд\. \d+', subject)  
    subjects = []
    
    for i, part in enumerate(parts):
        if i == 0:
            subjects.append({"subject": part.strip()})  
        else:
            subjects.append({"subject2": part.strip()})  

    return subjects

def get_schedule_for_today(excel_file, day_column, group_column):

    df = pd.read_excel(excel_file)
    df.columns = df.columns.str.strip()
    today = datetime.now().weekday()
    
   
    
    today_schedule = df[df[day_column] == days_of_week[today]]
    if not today_schedule.empty:
        start_index = today_schedule.index[0]  
        end_index = min(start_index + 20, len(df))  
        
        schedule_array = []  

        pattern = re.compile(r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ].[А-ЯЁ].\sАуд.\s\d{3}')

        for index, row in df.iloc[start_index:end_index].iterrows():
            time_slot = row['Unnamed: 1']  
            subjects = row[group_column]  
            
            if pd.isna(subjects):
                continue
            
            subjects_list = [subject.strip() for subject in str(subjects).split(',')]
           
            for subject in subjects_list:
                if pd.isna(time_slot):                                      
                    if schedule_array:
                        schedule_array[-1]['subject'] += f" {subject}"
                else:
                    schedule_array.append({'time': time_slot, 'subject': subject})

    
    current_date = date.today()
    week_number = current_date.isocalendar()[1]
    choice = 0 if week_number % 2 == 1 else 1  

    
    schedule_list = []
    for entry in schedule_array:
        split_result = split_subjects(entry["subject"])
        subject_main = split_result[0]["subject"]
        subject_alternate = split_result[1]["subject2"] if len(split_result) > 1 else None
        
        selected_subject = subject_alternate if choice == 1 and subject_alternate else subject_main
        schedule_list.append({'time': entry["time"], 'subject': selected_subject})
    
    return schedule_list if schedule_list else []
async def user_exists(chat_id):
  
    conn = sqlite3.connect('users.db')  
    cursor = conn.cursor()
    
   
    cursor.execute("SELECT COUNT(*) FROM users WHERE chat_id = ?", (chat_id,))
    count = cursor.fetchone()[0]
    
   
    conn.close()
    
    return count > 0

kb_router = Router()
class quest(StatesGroup):    
    course = State()
    group = State()
CONFIG_PATH = "config.json"
class req(StatesGroup):    
    req = State()

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = json.load(file)
AUTHORIZED_USERS = config["authorized_users"]


@kb_router.message(lambda message: message.text == "Профиль")
async def profile(message: types.Message):
    user_id = str(message.chat.id)
    
    if user_id in AUTHORIZED_USERS:
        name = AUTHORIZED_USERS[user_id]["name"]
        await message.answer(f"Ваш профиль:\nИмя: {name}\nID: {user_id}")
    else:
        await message.answer("Профиль не найден.")


@kb_router.message(lambda message: message.text == "Сделать запрос")
async def request_action(message: types.Message,state: FSMContext):
    await message.answer("Введите ваш запрос: ")
    await state.set_state(req.req)
@kb_router.message(req.req)  
async def process_request(message: types.Message, state: FSMContext):
    await state.update_data(req=message.text)  
    user_data = await state.get_data()
    print(user_data['req'])
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content":user_data['req'] }],
        web_search=False
    )
    await message.answer(response.choices[0].message.content)




@kb_router.callback_query(lambda c: c.data=='back')
async def back_menu(callabck: callback_query):    
     await callabck.message.edit_text(text='Привет! Какой ты курс?',reply_markup=create_start_kb())


def create_start_kb() -> InlineKeyboardMarkup:
    buttons = [        [InlineKeyboardButton(text="1", callback_data="1")],
        [            InlineKeyboardButton(text="2", callback_data="2")],
        [            InlineKeyboardButton(text="3", callback_data="3")],
        [            InlineKeyboardButton(text="4", callback_data="4")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons, )


def create_keyboard_group(course_id: int) -> InlineKeyboardMarkup:
    buttons = []
    if course_id == 1:
        start_index, end_index = 0, 6
    elif course_id == 2:
        start_index, end_index = 6, 11
    elif course_id == 3:
        start_index, end_index = 11, 16
    elif course_id == 4:
        start_index, end_index = 16, 22
    else:
        raise ValueError("а как ")

   
    for j in but[start_index:end_index]:
        button = InlineKeyboardButton(text=str(j), callback_data=j)
        buttons.append([button])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_return_menu() -> InlineKeyboardMarkup:
    butn = [        [InlineKeyboardButton(text='назад', callback_data='back')],
    ]    
    return InlineKeyboardMarkup(inline_keyboard=butn,)


# Обработчики
@kb_router.callback_query(lambda c: c.data in ['1', '2', '3', '4'])
async def select_course(call: CallbackQuery, state: FSMContext):
    
    await state.update_data(course=call.data)
    await call.message.edit_text('Выберите свою группу:', reply_markup=create_keyboard_group(int(call.data)))
    await call.message.answer("Вернуться назад", reply_markup=create_return_menu())   
    await state.set_state(quest.group)

@kb_router.callback_query(lambda c: c.data in
    ['ТМ 1119', 'МТОРЭПУ 1120', 'МТОЭРПО 1121', 'ЭОЭО 1122', 'СЭЗ 1123',
    'ОНМС 1124', 'ТМ 2114', 'ТМ 2115', 'МТОРЭПУ 2116', 'МТОРПО 2117', 
    'ТЭОЭО 2118', 'ТМП 3109', 'МТОРЭПУ 3110', 'МТОРПО 3111', 
    'ТЭОЭО 3112', 'СЭЗ 3113', 'ТМП 4105', 'МТОРЭПУ 4106', 
    'МТОРПО 4107', 'ТЭОЭО 4108', 'ТМП 5100', 'МТОРЭПУ 5101'])
async def select_course(call: CallbackQuery, state: FSMContext):   
    await state.update_data(group=call.data)  
    user_data = await state.get_data()
    course = user_data.get('course')  
    chat_id = call.from_user.id 
    group_mapping = {
        'ТМ 1119': 'Unnamed: 2',
        'МТОРЭПУ 1120': 'Unnamed: 3',
        'МТОЭРПО 1121': 'Unnamed: 4',
        'ЭОЭО 1122': 'Unnamed: 5',
        'СЭЗ 1123': 'Unnamed: 6',
        'ОНМС 1124': 'Unnamed: 7',
        'ТМ 2114': 'Unnamed: 8',
        'ТМ 2115': 'Unnamed: 9',
        'МТОРЭПУ 2116': 'Unnamed: 10',
        'МТОРПО 2117': 'Unnamed: 11',
        'ТЭОЭО 2118': 'Unnamed: 12',
        'ТМП 3109': 'Unnamed: 13',
        'МТОРЭПУ 3110': 'Unnamed: 14',
        'МТОРПО 3111': 'Unnamed: 15',
        'ТЭОЭО 3112': 'Unnamed: 16',
        'СЭЗ 3113': 'Unnamed: 17',
        'ТМП 4105': 'Unnamed: 18',
        'МТОРЭПУ 4106': 'Unnamed: 19',
        'МТОРПО 4107': 'Unnamed: 20',
        'ТЭОЭО 4108': 'Unnamed: 21',
        'ТМП 5100': 'Unnamed: 22',
        'МТОРЭПУ 5101': 'Unnamed: 23'
    }

    group_column = group_mapping.get(call.data)

    excel_file_path = 'sheldure2.xlsx'  
    day_column = 'Unnamed: 0'  
    schedule_today = get_schedule_for_today(excel_file_path, day_column, group_column) 
    
    if schedule_today:
        message = "Расписание на сегодня:\n" + "\n".join([entry["subject"] for entry in schedule_today])
    else:
        message = "Расписание на сегодня отсутствует."
    
    await call.message.edit_text(message)
    if not await user_exists(chat_id):
        data_set(chat_id, course, call.data)
async def send_message(chat_id: int, message: str):
    await bot.send_message(chat_id, message) 
async def send_shedule():
    excel_file_path = 'sheldure2.xlsx'  
    day_column = 'Unnamed: 0'  
    group_mapping = {
        'ТМ 1119': 'Unnamed: 2',
        'МТОРЭПУ 1120': 'Unnamed: 3',
        'МТОЭРПО 1121': 'Unnamed: 4',
        'ЭОЭО 1122': 'Unnamed: 5',
        'СЭЗ 1123': 'Unnamed: 6',
        'ОНМС 1124': 'Unnamed: 7',
        'ТМ 2114': 'Unnamed: 8',
        'ТМ 2115': 'Unnamed: 9',
        'МТОРЭПУ 2116': 'Unnamed: 10',
        'МТОРПО 2117': 'Unnamed: 11',
        'ТЭОЭО 2118': 'Unnamed: 12',
        'ТМП 3109': 'Unnamed: 13',
        'МТОРЭПУ 3110': 'Unnamed: 14',
        'МТОРПО 3111': 'Unnamed: 15',
        'ТЭОЭО 3112': 'Unnamed: 16',
        'СЭЗ 3113': 'Unnamed: 17',
        'ТМП 4105': 'Unnamed: 18',
        'МТОРЭПУ 4106': 'Unnamed: 19',
        'МТОРПО 4107': 'Unnamed: 20',
        'ТЭОЭО 4108': 'Unnamed: 21',
        'ТМП 5100': 'Unnamed: 22',
        'МТОРЭПУ 5101': 'Unnamed: 23'
    }
    curr = sqlite3.connect('users.db')
    conn = curr.cursor()
    conn.execute('SELECT group_name,chat_id FROM users ')
    rows = conn.fetchall()
    for row in rows:
        group_name,chat_id = row
        group_column = group_mapping.get(group_name) 
        schedule_today = get_schedule_for_today(excel_file_path, day_column, group_column) 
        if schedule_today:
            message = "Расписание на сегодня:\n" + "\n".join([entry["subject"] for entry in schedule_today])
        
        await send_message(chat_id, message)

def run_send_schedule():
    asyncio.run(send_shedule())
def schedule_jobs():
    schedule.every().monday.at("09:00").do(run_send_schedule)
    schedule.every().tuesday.at("09:00").do(run_send_schedule)
    schedule.every().wednesday.at("09:00").do(run_send_schedule)
    schedule.every().thursday.at("09:00").do(run_send_schedule)
    schedule.every().friday.at("09:00").do(run_send_schedule)
    schedule.every().saturday.at("09:00").do(run_send_schedule)


    while True:
        schedule.run_pending()
        time.sleep(1)


threading.Thread(target=schedule_jobs, daemon=True).start()




    

