from django.shortcuts import render
from salecars.bot import bot


def start_polling(request):
    executor = bot.executor
    dp = bot.dp
    print(__name__)
    if __name__ == 'salecars.views':
        executor.start_polling(dp, skip_updates=True)


