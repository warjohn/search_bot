# coding=windows-1251
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackGame

number = [
    [KeyboardButton(text = "���������� ���������", request_contact = True)],
    
]
number_key = ReplyKeyboardMarkup(keyboard = number, resize_keyboard=True)

keyboard_to_delete = ReplyKeyboardRemove()

show_more = [
        [InlineKeyboardButton(text = "���..", callback_data='show_more')]
]
show_more_kb = InlineKeyboardMarkup(inline_keyboard = show_more)