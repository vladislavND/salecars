import logging
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram_config.keyboards.inline.keyboard import (
    region_keyboard, models_keyboard, city_keyboard, marks_keyboard,
    true_and_false_keyboard, wheel_choices_keyboard, engine_keyboard,
    phone_keyboard
)
from telegram_config.states.states import UserState
from salecars.models import User, Auto, Region, City, Marks, Models
from telegram_config.loader import dp, bot

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['send'])
async def register_start(message: types.Message):
    chat_id = message.from_user.id
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
        state_data['region'] = Region.objects.get(id=region_id)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Выберите город',
        reply_markup=city_keyboard(region_id)
    )
    await UserState.city.set()


@dp.callback_query_handler(state=UserState.city)
async def register_city(callback_data: types.CallbackQuery, state: FSMContext):
    city_id = callback_data.data
    async with state.proxy() as state_data:
        state_data['city'] = City.objects.get(id=city_id)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Выберите марку',
        reply_markup=marks_keyboard()
    )
    await UserState.marks.set()


@dp.callback_query_handler(state=UserState.marks)
async def register_marks(callback_data: types.CallbackQuery, state: FSMContext):
    mark_id = callback_data.data
    async with state.proxy() as state_data:
        state_data['marks'] = Marks.objects.get(id=mark_id)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Выберите модель',
        reply_markup=models_keyboard(mark_id)
    )
    await UserState.models.set()


@dp.callback_query_handler(state=UserState.models)
async def register_models(callback_data: types.CallbackQuery, state: FSMContext):
    model_id = callback_data.data
    async with state.proxy() as state_data:
        state_data['model'] = Models.objects.get(id=model_id)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Растаможен в Казахстане?',
        reply_markup=true_and_false_keyboard()
    )
    await UserState.resident.set()


@dp.callback_query_handler(state=UserState.resident)
async def register_resident(callback_data: types.CallbackQuery, state: FSMContext):
    resident_bool = callback_data.data
    async with state.proxy() as state_data:
        state_data['resident'] = bool(resident_bool)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Аварийная / Не на ходу?',
        reply_markup=true_and_false_keyboard()
    )
    await UserState.crash.set()


@dp.callback_query_handler(state=UserState.crash)
async def register_crash(callback_data: types.CallbackQuery, state: FSMContext):
    crash_bool = callback_data.data
    async with state.proxy() as state_data:
        state_data['crash'] = bool(crash_bool)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Руль',
        reply_markup=wheel_choices_keyboard()
    )
    await UserState.steering_wheel.set()


@dp.callback_query_handler(state=UserState.steering_wheel)
async def register_steering_wheel(callback_data: types.CallbackQuery, state:FSMContext):
    wheel = callback_data.data
    async with state.proxy() as state_data:
        state_data['steering_wheel'] = wheel
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Тип топлива',
        reply_markup=engine_keyboard()
    )
    await UserState.engine.set()


@dp.callback_query_handler(state=UserState.engine)
async def register_engine(callback_data: types.CallbackQuery, state: FSMContext):
    engine = callback_data.data
    async with state.proxy() as state_data:
        state_data['engine'] = engine
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Введите объем двигателя: Например (2.0)',
    )
    await UserState.value.set()


@dp.message_handler(state=UserState.value)
async def register_value(message: types.Message, state: FSMContext):
    try:
        value = message.text
        value = float(value)
        async with state.proxy() as state_data:
            state_data['value'] = value
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Введите год:'
        )
        await UserState.year.set()
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Обьем должен состоять только из цифр! Например (2.0)'
        )
        await UserState.value.set()


@dp.message_handler(state=UserState.year)
async def register_year(message: types.Message, state: FSMContext):
    try:
        year = message.text
        if len(year) < 4 or len(year) > 4:
            raise ValueError
        year = int(year)
        async with state.proxy() as state_data:
            state_data['year'] = year
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Введите цену'
        )
        await UserState.price.set()
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Год должен состоять только из 4 цифр! (Введите год еше раз)'
        )
        await UserState.year.set()


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
            text='Цена должна состоять только из цифр! (Введите цену еще раз)'
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
        state_data['mobile_phone'] = phone
        state_data['telegram_id'] = message.from_user.id
        state_data['first_name'] = message.from_user.first_name
        state_data['username'] = message.from_user.username
    state_user = await state.get_data()
    User.create_many_to_many(Auto, **state_user)
    await bot.send_message(
        chat_id=message.chat.id,
        text='Ваше объявление передано модератору, как только объявление пройдет проверку вы получите уведомление'
    )
    await state.finish()


