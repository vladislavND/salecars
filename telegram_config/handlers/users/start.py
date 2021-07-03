from aiogram import types
from aiogram.dispatcher import FSMContext
from telegram_config.loader import dp, bot


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    msg = "Привет, это SalecarsBot для поиска автомобилей!🚗\n\n" \
          "Вот список доступных команд:\n\n" \
          "/send - Подать объявление о продаже авто 🚙\n\n" \
          "/search - Настроить фильтр и найти авто\n\n" \
          "/settings - Настроить свой профиль ⚙\n\n" \
          "/filter - Добавить или удалить фильтр\n\n"
    await bot.send_message(
        message.chat.id,
        text=msg,
        disable_web_page_preview=True
    )
