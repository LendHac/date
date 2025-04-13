from aiogram import types, F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, callback_query
from aiogram.filters import Command
import kb

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Какой ты курс?",reply_markup=kb.create_start_kb())

    


