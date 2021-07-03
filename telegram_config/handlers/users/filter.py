import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram_config.states.states import FilterState
from salecars.models import Users, Auto, Region, City, Marks, Models
from telegram_config.loader import dp, bot
from telegram_config.keyboards.inline.filter_keyboards import (
    region_keyboard, models_keyboard, city_keyboard, marks_keyboard,
    true_and_false_keyboard, wheel_choices_keyboard, engine_keyboard,
    start_filter_keyboard, delete_filters_keyboard
)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['filter'], state='*')
async def start_filter(message: types.Message):
    chat_id = message.from_user.id
    await bot.send_message(
        chat_id=chat_id,
        text="Выберите что вы хотите сделать",
        reply_markup=start_filter_keyboard()
    )
    await FilterState.choice.set()


@dp.callback_query_handler(state=FilterState.choice)
async def filter_choice(callback: types.CallbackQuery, state=FSMContext):
    chat_id = callback.from_user.id
    if callback.data == 'add':
        await bot.send_message(
            chat_id=chat_id,
            text='Выберите регион',
            reply_markup=region_keyboard()
        )
        await FilterState.region.set()
    if callback.data == 'delete':
        if Users.get_filters(chat_id):
            await bot.send_message(
                chat_id=chat_id,
                text='Нажмите на фильтр который хотите удалить',
                reply_markup=delete_filters_keyboard(chat_id)
            )
            await FilterState.delete.set()
        else:
            await bot.send_message(
                chat_id=chat_id,
                text='У вас еще нет настроенных фильтров',
                reply_markup=start_filter_keyboard()
            )
            await FilterState.choice.set()


@dp.callback_query_handler(state=FilterState.region)
async def filter_region(callback_data: types.CallbackQuery, state: FSMContext):
    region_id = callback_data.data
    async with state.proxy() as state_data:
        state_data['region'] = Region.objects.get(id=region_id)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Выберите город',
        reply_markup=city_keyboard(region_id)
    )
    await FilterState.city.set()


@dp.callback_query_handler(state=FilterState.city)
async def filter_city(callback_data: types.CallbackQuery, state: FSMContext):
    city_id = callback_data.data
    async with state.proxy() as state_data:
        state_data['city'] = City.objects.get(id=city_id)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Выберите марку',
        reply_markup=marks_keyboard()
    )
    await FilterState.marks.set()


@dp.callback_query_handler(state=FilterState.marks)
async def filter_marks(callback_data: types.CallbackQuery, state: FSMContext):
    mark_id = callback_data.data
    async with state.proxy() as state_data:
        state_data['marks'] = Marks.objects.get(id=mark_id)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Выберите модель',
        reply_markup=models_keyboard(mark_id)
    )
    await FilterState.models.set()


@dp.callback_query_handler(state=FilterState.models)
async def filter_models(callback_data: types.CallbackQuery, state: FSMContext):
    model_id = callback_data.data
    async with state.proxy() as state_data:
        state_data['model'] = Models.objects.get(id=model_id)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Растаможен в Казахстане?',
        reply_markup=true_and_false_keyboard()
    )
    await FilterState.resident.set()


@dp.callback_query_handler(state=FilterState.resident)
async def filter_resident(callback_data: types.CallbackQuery, state: FSMContext):
    resident_bool = callback_data.data
    async with state.proxy() as state_data:
        state_data['resident'] = bool(resident_bool)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Аварийная / Не на ходу?',
        reply_markup=true_and_false_keyboard()
    )
    await FilterState.crash.set()


@dp.callback_query_handler(state=FilterState.crash)
async def filter_crash(callback_data: types.CallbackQuery, state: FSMContext):
    crash_bool = callback_data.data
    async with state.proxy() as state_data:
        state_data['crash'] = bool(crash_bool)
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Руль',
        reply_markup=wheel_choices_keyboard()
    )
    await FilterState.steering_wheel.set()


@dp.callback_query_handler(state=FilterState.steering_wheel)
async def filter_steering_wheel(callback_data: types.CallbackQuery, state: FSMContext):
    wheel = callback_data.data
    async with state.proxy() as state_data:
        state_data['steering_wheel'] = wheel
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Тип топлива',
        reply_markup=engine_keyboard()
    )
    await FilterState.engine.set()


@dp.callback_query_handler(state=FilterState.engine)
async def filter_engine(callback_data: types.CallbackQuery, state: FSMContext):
    engine = callback_data.data
    async with state.proxy() as state_data:
        state_data['engine'] = engine
    await bot.edit_message_text(
        message_id=callback_data.message.message_id,
        chat_id=callback_data.from_user.id,
        text='Введите объем двигателя: Например (2.0)',
    )
    await FilterState.value.set()


@dp.message_handler(state=FilterState.value)
async def filter_value(message: types.Message, state: FSMContext):
    try:
        value = message.text
        value = float(value)
        async with state.proxy() as state_data:
            state_data['value'] = value
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Введите год:'
        )
        await FilterState.year.set()
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Обьем должен состоять только из цифр! Например (2.0)'
        )
        await FilterState.value.set()


@dp.message_handler(state=FilterState.year)
async def filter_year(message: types.Message, state: FSMContext):
    try:
        year = message.text
        if len(year) < 4 or len(year) > 4:
            raise ValueError
        year = int(year)
        async with state.proxy() as state_data:
            state_data['year'] = year
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Введите цену от'
        )
        await FilterState.price_to.set()
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Год должен состоять только из 4 цифр! (Введите год еше раз)'
        )
        await FilterState.year.set()


@dp.message_handler(state=FilterState.price_to)
async def filter_price_to(message: types.Message, state: FSMContext):
    try:
        price = message.text
        price = int(price)
        async with state.proxy() as state_data:
            state_data['price_to'] = price
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Введите цену до'
        )
        await FilterState.price_from.set()
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Цена должна состоять только из цифр! (Введите цену еще раз)',
        )
        await FilterState.price_to.set()


@dp.message_handler(state=FilterState.price_from)
async def filter_price_from(message: types.Message, state: FSMContext):
    try:
        price = message.text
        price = int(price)
        async with state.proxy() as state_data:
            state_data['price_from'] = price
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Ваш фильтр сохранен'
        )
        async with state.proxy() as state_data:
            state_data['telegram_id'] = message.from_user.id
            state_data['first_name'] = message.from_user.first_name
            state_data['username'] = message.from_user.username
        state_filter = await state.get_data()
        Users().add_filter(**state_filter)
        await state.finish()
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Цена должна состоять только из цифр! (Введите цену еще раз)'
        )
        await FilterState.price_from.set()


@dp.callback_query_handler(state=FilterState.delete)
async def delete_filter(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    auto_filter_id = callback.data
    Users.objects.get(telegram_id=telegram_id).auto_filter.get(id=auto_filter_id).delete()
    await bot.send_message(
        chat_id=telegram_id,
        text='Фильтр удален',
        reply_markup=start_filter_keyboard()
    )
    await FilterState.choice.set()
