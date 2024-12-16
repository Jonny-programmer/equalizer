from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def generate_yes_no_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="yes")
    builder.button(text="Нет", callback_data="no")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
