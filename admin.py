from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import sqlite3
from config import AdminID
router = Router()

def get_chat_ids_by_group(group_name: str):
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT chat_id FROM users WHERE group_name = ?", (group_name,))
    chat_ids = cursor.fetchall()
    
    conn.close()
    
    return [chat_id[0] for chat_id in chat_ids]

@router.message(Command('send'))
async def send_message_to_group(message: types.Message):
    if message.chat.id not in AdminID:
        await message.reply("У вас нет прав на использование этой команды.")
        return
    command_text = message.text[len('/send '):].strip()  # Убираем команду /send и пробел после нее

    # Проверяем, что сообщение не пустое
    if not command_text:
        await message.reply("Используйте формат: /send [группа] [сообщение]")
        return

    
    parts = command_text.split(' ', 2)  

    
    if len(parts) < 2:
        await message.reply("Используйте формат: /send [группа] [сообщение]")
        return

    group_name = parts[0] + ' ' + parts[1] 
    message_text = parts[2] if len(parts) > 2 else ''
    chat_ids = get_chat_ids_by_group(group_name)

    if not chat_ids:
        await message.reply(f"Группа '{group_name}' не найдена или не содержит участников.")
        return

    # Отправляем сообщение всем пользователям в группе
    for chat_id in chat_ids:
        try:
            await message.bot.send_message(chat_id, message_text)  # Изменено на send_message
        except Exception as e:
            print(f"Не удалось отправить сообщение в {chat_id}: {e}")

    await message.reply(f"Сообщение успешно отправлено в группу '{group_name}'.")