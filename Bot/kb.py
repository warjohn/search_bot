# coding=windows-1251
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackGame

number = [
    [KeyboardButton(text = "поделиться контактом", request_contact = True)],
    
]
number_key = ReplyKeyboardMarkup(keyboard = number, resize_keyboard=True)

keyboard_to_delete = ReplyKeyboardRemove()

show_more = [
        [InlineKeyboardButton(text = "Ещё..", callback_data='show_more')]
]
show_more_kb = InlineKeyboardMarkup(inline_keyboard = show_more)