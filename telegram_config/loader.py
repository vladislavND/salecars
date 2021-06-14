import logging
from pathlib import Path

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


from .data import config
from telegram_config.keyboards.inline.keyboard import (
    start_keyboard, register_keyboard, paginations_keyboard,
    region_keyboard, models_keyboard, city_keyboard, marks_keyboard,
    true_and_false_keyboard, wheel_choices_keyboard, engine_keyboard,
    phone_keyboard
)
from telegram_config.states.states import UserState
from salecars.models import User, Auto, Models, Region

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start', 'help'], state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    msg = """
    Привет, Это SalecarsBot для поиска автомобилей!
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
    region_id = callback_data.data
    async with state.proxy() as state_data:
        state_data['region_id'] = region_id
    await bot.send_message(
        chat_id=callback_data.from_user.id,
        text='Выберите город',
        reply_markup=city_keyboard(region_id)
    )
    await UserState.city.set()


@dp.callback_query_handler(state=UserState.city)
async def register_city(callback_data: types.CallbackQuery, state: FSMContext):
    city_id = callback_data.data
    async with state.proxy() as state_data:
        state_data['city_id'] = city_id
    await bot.send_message(
        chat_id=callback_data.from_user.id,
        text='Выберите марку',
        reply_markup=marks_keyboard()
    )
    await UserState.marks.set()


@dp.callback_query_handler(state=UserState.marks)
async def register_marks(callback_data: types.CallbackQuery, state: FSMContext):
    mark_id = callback_data.data
    async with state.proxy() as state_data:
        state_data['mark_id'] = mark_id
    await bot.send_message(
        chat_id=callback_data.from_user.id,
        text='Выберите модель',
        reply_markup=models_keyboard(mark_id)
    )
    await UserState.models.set()


@dp.callback_query_handler(state=UserState.models)
async def register_models(callback_data: types.CallbackQuery, state: FSMContext):
    model_id = callback_data.data
    async with state.proxy() as state_data:
        state_data['model_id'] = model_id
    await bot.send_message(
        chat_id=callback_data.from_user.id,
        text='Растаможен в Казахстане?',
        reply_markup=true_and_false_keyboard()
    )
    await UserState.resident.set()


@dp.callback_query_handler(state=UserState.resident)
async def register_resident(callback_data: types.CallbackQuery, state: FSMContext):
    resident_bool = callback_data.data
    async with state.proxy() as state_data:
        state_data['resident_bool'] = bool(resident_bool)
    await bot.send_message(
        chat_id=callback_data.from_user.id,
        text='Аварийная / Не на ходу?',
        reply_markup=true_and_false_keyboard()
    )
    await UserState.crash.set()


@dp.callback_query_handler(state=UserState.crash)
async def register_crash(callback_data: types.CallbackQuery, state: FSMContext):
    crash_bool = callback_data.data
    async with state.proxy() as state_data:
        state_data['crash_bool'] = bool(crash_bool)
    await bot.send_message(
        chat_id=callback_data.from_user.id,
        text='Руль',
        reply_markup=wheel_choices_keyboard()
    )
    await UserState.steering_wheel.set()


@dp.callback_query_handler(state=UserState.steering_wheel)
async def register_steering_wheel(callback_data: types.CallbackQuery, state:FSMContext):
    wheel = callback_data.data
    async with state.proxy() as state_data:
        state_data['wheel'] = wheel
    await bot.send_message(
        chat_id=callback_data.from_user.id,
        text='Тип топлива',
        reply_markup=engine_keyboard()
    )
    await UserState.engine.set()


@dp.callback_query_handler(state=UserState.engine)
async def register_engine(callback_data: types.CallbackQuery, state:FSMContext):
    engine = callback_data.data
    async with state.proxy() as state_data:
        state_data['engine'] = engine
    await bot.send_message(
        chat_id=callback_data.from_user.id,
        text='Введите объем двигателя',
    )
    await UserState.value.set()


@dp.message_handler(state=UserState.value)
async def register_value(message: types.Message, state: FSMContext):
    value = message.text
    async with state.proxy() as state_data:
        state_data['value'] = value
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Введите год:'
    )
    await UserState.year.set()


@dp.message_handler(state=UserState.year)
async def register_year(message: types.Message, state: FSMContext):
    year = message.text
    async with state.proxy() as state_data:
        state_data['year'] = year
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Введите цену'
    )
    await UserState.price.set()


@dp.message_handler(state=UserState.price)
async def register_price(message: types.Message, state: FSMContext):
    try:
        price = message.text
        price = int(price)
        async with state.proxy() as state_data:
            state_data['price'] = price
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Отправьте фото автомобиля'
        )
        await UserState.image.set()
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Цена должна состоять только из цифр'
        )
        await UserState.price.set()


@dp.message_handler(content_types=['photo'], state=UserState.image)
async def register_image(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await state.get_data()
    Path(f'image/{user_id}_folder/').mkdir(parents=True, exist_ok=True)
    for photo in message.photo:
        await photo.download(destination=f'image/{user_id}_folder/{user_id}{user.get("mark_id")}.jpg')
    image = f'image/{user_id}_folder/{user_id}{user.get("mark_id")}.jpg'
    async with state.proxy() as state_data:
        state_data['image'] = image
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Введите описание. (Необязательно)'
    )
    await UserState.description.set()


@dp.message_handler(state=UserState.description)
async def register_description(message: types.Message, state: FSMContext):
    description = message.text
    async with state.proxy() as state_data:
        state_data['description'] = description
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Ваш номер телефона (Нажмите поделиться номером или введите номер телефона в формате 77777777777)',
        reply_markup=phone_keyboard()
    )
    await UserState.phone.set()


@dp.message_handler(state=UserState.phone, content_types=types.ContentTypes.CONTACT | types.ContentTypes.TEXT)
async def register_phone(message: types.Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text
    async with state.proxy() as state_data:
        state_data['phone'] = phone

    state_user = await state.get_data()
    auto = Auto(
        model=Models.objects.get(id=state_user.get('model_id')),
        region=Region.objects.get(id=state_user.get('region_id')),
        resident=state_user.get('resident_bool'), crash=state_user.get('crash_bool'),
        engine=state_user.get('engine'), steering_wheel=state_user.get('wheel'),
        value=state_user.get('value'), price=state_user.get('price'),
        image=state_user.get('image'), description=state_user.get('description'),
        year=state_user.get('year'))
    auto.save()
    if User.objects.filter(telegram_id=message.from_user.id).exists():
        User.objects.filter(telegram_id=message.from_user.id).add(auto)
    else:
        user = User(
            region=Region.objects.get(id=state_user.get('region_id')),
            username=message.from_user.username, mobile_phone=state_user.get('phone'),
            telegram_id=message.from_user.id, first_name=message.from_user.first_name
        )
        user.save()
        user.auto.add(auto)
    await bot.send_message(
        chat_id=message.chat.id,
        text='Ваше объявление передано модератору, как только объявление пройдет проверку вы получите уведомление'
    )







# @dp.message_handler(state=UserState.price)
# async def register_price_to(message: types.Message, state: FSMContext):
#     price = message.text
#     async with state.proxy() as state_data:
#         state_data['price'] = price
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
