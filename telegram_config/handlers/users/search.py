import logging
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram_config.keyboards.inline.search_keyboards import (
   search_keyboard
)
from telegram_config.states.states import UserState
from salecars.models import Users, Auto
from telegram_config.loader import dp, bot

filters = [
    {'region': 'Карагандинская область', 'marks': 'ford', 'price_to': '100000', 'price_from': '175000'},
    {'region': 'Карагандинская область', 'marks': 'Москвич', 'price_to': '100000', 'price_from': '175000'}
]


@dp.message_handler(commands=['search'], state='*')
async def start_search(message: types.Message, state: FSMContext):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Выберите ваш фильтр',
        reply_markup=search_keyboard()
    )

