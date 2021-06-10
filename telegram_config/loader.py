import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.parts import paginate

from .data import config
from salecars.bot.keyboard import (
    start_keyboard, register_keyboard, paginations_keyboard,
    region_keyboard, models_keyboard
)
# from parsing import schema as sh
from salecars.bot.states import UserState
# from db.models import User
# from parsing.tasks import test

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start', 'help'], state='*')
async def start(message: types.Message):
    msg = """
    Привет, Это SalecarsBot для поиска автомобилей! \n 
    """
    await bot.send_message(
        message.chat.id,
        text=msg,
        reply_markup=start_keyboard(),
        disable_web_page_preview=True
    )


@dp.callback_query_handler(text='send')
async def register_start(callback_data: types.CallbackQuery):
    chat_id = callback_data.from_user.id
    await bot.send_message(
        chat_id=chat_id,
        text='Пожалуйста выберите регион',
        reply_markup=region_keyboard()
                           )
    await UserState.region.set()


@dp.callback_query_handler(state=UserState.region)
async def register_region(callback_data: types.CallbackQuery, state: FSMContext):
    data = callback_data.data
    region_id = data.get('data')
    async with state.proxy() as state_data:
        state_data['region_id'] = region_id
    await bot.send_message(
        chat_id=data.get('from').get('id'),
        text='Пожалуйста выберите модель автомобиля',
        reply_markup=models_keyboard()
    )
    await UserState.models.set()


@dp.callback_query_handler(state=UserState.models)
async def register_models(callback_data: types.CallbackQuery, state: FSMContext):
    data = callback_data.data
    model_id = data.get('data')
    async with state.proxy() as state_data:
        state_data['model_id'] = model_id
    await bot.send_message(
        chat_id=data.get('from').get('id'),
        text='Пожалуйста введите цену ОТ:',
    )
    await UserState.price_from.set()


@dp.message_handler(state=UserState.price_from)
async def register_price_from(message: types.Message, state: FSMContext):
    price_from = message.text
    async with state.proxy() as state_data:
        state_data['price_from'] = price_from
    await bot.send_message(
        chat_id=message.chat.id,
        text='Введите цену ДО:'
    )
    await UserState.price_to.set()


# @dp.message_handler(state=UserState.price_to)
# async def register_price_to(message: types.Message, state: FSMContext):
#     price_to = message.text
#     async with state.proxy() as state_data:
#         state_data['price_to'] = price_to
#
#     info = await state.get_data()
#     info['username'] = message.from_user.username
#     info['first_name'] = message.from_user.first_name
#     info['telegram_id'] = message.from_user.id
#     User().add(**info)
#     await state.finish()
#     await bot.send_message(
#         chat_id=message.chat.id,
#         text='Начнем!',
#         reply_markup=start_keyboard()
#     )
#
#
# @dp.callback_query_handler(text='search')
# async def search(callback: types.CallbackQuery, state: FSMContext):
#     data = sh.CallbackDataSchema().dump(callback)
#     instance_id = data.get('from').get('id')
#     auto = test(instance_id)
#     objects = paginate(auto, page=0, limit=1)
#     objects = objects[0]
#     count_pages = len(auto)
#     async with state.proxy() as state_data:
#         state_data['page'] = 1
#         state_data['auto'] = auto
#         state_data['count_pages'] = count_pages
#
#     msg = 'Марка: {}\n Год: {} \n Цена: {}\n '.format(*objects.values())
#     image = objects.get('image_url')
#     await bot.send_photo(
#         chat_id=instance_id,
#         caption=msg,
#         photo=image,
#         reply_markup=paginations_keyboard(count_pages=count_pages)
#     )
#     await UserState.view.set()
#
#
# @dp.callback_query_handler(state=UserState.view)
# async def view(callback: types.CallbackQuery, state: FSMContext):
#     message_id = callback.message.message_id
#     data = sh.CallbackDataSchema().dump(callback)
#     instance_id = data.get('from').get('id')
#     page = await state.get_data()
#     count = page['page']
#     count_pages = page['count_pages']
#     if callback.data == 'next':
#         count += 1
#         async with state.proxy() as state_data:
#             state_data['page'] = count
#     if callback.data == 'prev':
#         count -= 1
#         async with state.proxy() as state_data:
#             state_data['page'] = count
#     objects = paginate(page['auto'], page=count, limit=1)
#     objects = objects[0]
#     image = objects.get('image_url')
#     msg = 'Марка: {}\n Год: {} \n Цена: {}\n '.format(*objects.values())
#     await bot.edit_message_media(
#         chat_id=instance_id,
#         message_id=message_id,
#         inline_message_id=callback.inline_message_id,
#         media=types.InputMediaPhoto(
#             type='photo',
#             caption=msg,
#             media=image
#         ),
#         reply_markup=paginations_keyboard(count=count, count_pages=count_pages)
#     )
#
#
# @dp.callback_query_handler(text='filter')
# async def filter(callback_data: types.CallbackQuery):
#     data = sh.CallbackDataSchema().dump(callback_data)
#
#
# @dp.callback_query_handler(text='hits')
# async def hits(callback_data: types.CallbackQuery):
#     data = sh.CallbackDataSchema().dump(callback_data)
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)
