
import os
import telebot
import database
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
URL = os.getenv('URL')
GROUP_ID = os.getenv('GROUP_ID')
# key = ['CHMZAP']

SENDER = os.getenv('SENDER')
PASSWORD = os.getenv('PASSWORD')

bot = telebot.TeleBot(TOKEN, threaded=False)
bot.set_my_commands([
    telebot.types.BotCommand("/start", "Главное меню"),
    telebot.types.BotCommand("/help", "Описание"),
    telebot.types.BotCommand("/count", "Количество записей"),
    telebot.types.BotCommand("/change_mail", "Смена почты"),
    telebot.types.BotCommand("/check_trouble", "Вывести запись"),
])

db = database.Database('chmzap_sq.sqlite')
