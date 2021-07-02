import os

from django.conf import settings
from aiogram.types import BotCommand

# from dotenv import load_dotenv
# load_dotenv()

BOT_TOKEN = settings.BOT_TOKEN

admins = [
    settings.ADMIN_ID,
]

ip = settings.IP

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

commands = [
        BotCommand(command="/send", description="Подать объявление"),
        BotCommand(command="/search", description="Найти авто по вашему фильтру"),
        BotCommand(command="/settings", description="Перейти в настройки вашего профиля"),
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/help", description="Получить справку о методах")
    ]
