from aiogram import types, F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, callback_query
from aiogram.filters import Command
import kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import json
router = Router()

CONFIG_PATH = "config.json"
#button = KeyboardButton("Профиль")
#button2 = KeyboardButton("Сделать запрос")
with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = json.load(file)
AUTHORIZED_USERS = config["authorized_users"]
print(AUTHORIZED_USERS)
if 5192937856 in AUTHORIZED_USERS:
    print("cvfhgndfghmn")
def get_keyboard(user_id):
    if str(user_id) in AUTHORIZED_USERS:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Профиль")],
                [KeyboardButton(text="Сделать запрос")]
            ],
            resize_keyboard=True
        )
        return keyboard
    return ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)
    
@router.message(Command("start"))
async def start_handler(msg: Message):

    keyboard = get_keyboard(msg.chat.id)
    
    if keyboard:
        await msg.answer("Добро пожаловать!", reply_markup=keyboard)
    else:
        await msg.answer("Привет! Какой ты курс?",reply_markup=kb.create_start_kb())

    


