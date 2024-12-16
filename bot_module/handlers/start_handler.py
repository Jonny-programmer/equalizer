import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery, FSInputFile, Audio

from bot_module.keyboards import generate_yes_no_kb
from search import search_music
from bot_module.keyboards import *
from search.search_music import get_track, download_track

router = Router()  # [1]


# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.answer(
        "Привет :)\nЯ бот для преобразования звуков в красивую картинку\n⚙️ Пришли мне название песни или текст и я "
        "тебе отправлю её")


@router.message()
async def track_search(msg: Message):
    filename, text_for_person = get_track(msg.text)
    if text_for_person:
        await msg.answer(f"🎉 Нашлось \'{filename}\'.\nХотите скачать этот трек? Да/Нет\n>>> ",
                         reply_markup=generate_yes_no_kb())
    else:
        await msg.answer("😶‍🌫️Ничего не найдено")


@router.callback_query(F.data == "yes")
async def callback_query(msg: CallbackQuery):
    await msg.answer("Этот маленький маневр может вам стоить 51 год")
    text_track, filename = download_track()
    audio_from_pc = FSInputFile(filename+".mp3")
    await msg.message.answer_audio(audio_from_pc, caption=text_track[:1000])
    os.remove(filename+".mp3")


@router.callback_query(F.data == "no")
async def callback_query(msg: CallbackQuery):
    await msg.answer()
    await msg.message.answer("🎲 Возвращайтесь! \nЯ найду все что вы захотите)")
