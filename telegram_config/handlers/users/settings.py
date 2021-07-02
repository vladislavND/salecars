from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram_config.keyboards.inline.keyboard import (
   edit_profile_keyboard
)
from telegram_config.states.states import UserState
from salecars.models import User
from telegram_config.loader import dp, bot


@dp.message_handler(commands=['settings'], state='*')
async def cabinet(message: types.Message):
    if User.check_user(message.from_user.id):
        user = User.get_user(message.from_user.id)
        messages = f'' \
                  f'Имя: {user.first_name}\n' \
                  f'Номер телефона: {user.mobile_phone}\nРегион: {user.region.name}'
        await bot.send_message(
            chat_id=message.from_user.id,
            text=messages,
            reply_markup=edit_profile_keyboard()
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Вы еще не подавали ни одного объявления'
        )
        await UserState.region.set()


@dp.callback_query_handler(text='edit_phone', state='*')
async def edit_phone(callback: types.CallbackQuery, state: FSMContext):
    pass
