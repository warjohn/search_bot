# -*- coding: utf-8 -*-
import csv
from datetime import datetime
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message

import kb as kb
import text as tt
from search.search import search

global response
PAGE_SIZE = 3
router_start = Router()

@router_start.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(tt.greeting)


@router_start.message(F.text)
async def start_help(msg: Message):
    question = msg.text
    chat_id = msg.from_user.id
    user_name = msg.from_user.username
    with open('stat.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['user_name', 'chat_id', 'question'])
        writer.writerow([user_name, chat_id, question])

    global response
    response = search(question)  # Выполняем поиск по запросу
    if not response:  # Если ответ пуст
        await msg.answer("По вашему запросу ничего не найдено.", parse_mode=ParseMode.MARKDOWN)
        return

    # Отправляем первые 3 элемента
    await send_results(msg, 0)

@router_start.callback_query(F.data.startswith("show_more"))
async def send_more_results(clbk: CallbackQuery):
    current_index = int(clbk.data.split(":")[1])  # Получаем текущий индекс из данных callback
    await send_results(clbk.message, current_index)

async def send_results(msg: Message, start_index: int):
    global response
    if start_index >= len(response):  # Если вышли за пределы списка
        await msg.answer("Список пуст.", parse_mode=ParseMode.MARKDOWN)
        return

    text = "Вот что я смог найти по вашему запросу:\n\n"
    for i, item in enumerate(response[start_index:start_index + PAGE_SIZE]):
        text += f"{start_index + i + 1}) **[{item['title'].upper()}]({item['link']})**\n*Описание*: _{item['text']}_\n\n"

    # Обновляем клавиатуру с новой кнопкой
    new_index = start_index + PAGE_SIZE
    kb_with_more = kb.show_more_kb
    kb_with_more.inline_keyboard[0][0].callback_data = f"show_more:{new_index}"

    await msg.answer(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb_with_more)