
from flask import Flask, request
import telebot
import time
import random
import string
from markups import main_markup, choose_markup
import config
import database
from datetime import datetime
from telebot import types
from create_branch import create_operation_step

from config import bot, db


# secret = ''.join(random.choice(string.ascii_letters) for x in range(20))
# bot = telebot.TeleBot(config.TOKEN, threaded=False)

# db = database.Database('chmzap_sq.sqlite')

# bot.remove_webhook()
# time.sleep(1)
# bot.set_webhook(url="https://{}.pythonanywhere.com/{}".format(config.URL, secret))

# app = Flask(__name__)

# Часть кода для pythonanywhere


# @app.route('/{}'.format(secret), methods=["POST"])
# def webhook():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     print("Message")
#     return "ok", 200


@bot.message_handler(commands=['start'])
def first_step(message):
    db.create_tables()
    if (not db.check_user(message.from_user.id)):
        bot.send_message(
            message.chat.id,
            'Сообщение для незарегистрированных пользователей. \n'
            'Добро пожаловать в КО-2 бот.\n'
            f'Ваш id: {message.from_user.id}.\n'
            f'Ваше имя: {message.from_user.first_name} '
            f'{message.from_user.last_name}\n'
            'После введения ключа доступа вы будете внесены в базу данных.\n'
            'Убедитесь в коррекности имени и фамилии.\n'
            'При необходимости измените данные в настройках телеграм.'
            )
        time.sleep(2)
        bot.send_message(
            message.chat.id,
            'Введите ключ доступа:'
            )
    else:
        msg = bot.send_message(
            message.chat.id,
            'Главное меню.',
            reply_markup=main_markup()
            )
        bot.register_next_step_handler(msg, process_operation_step)


@bot.message_handler(commands=['CHMZAP'])
def register_step(message):
    if db.check_user(message.from_user.id):
        msg = bot.send_message(
            message.chat.id,
            'Главное меню.',
            reply_markup=main_markup()
            )
        bot.register_next_step_handler(msg, process_operation_step)
    else:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        db.create_user(user_id, first_name, last_name)
        bot.send_message(
            message.chat.id,
            'Регистрация успешна. Вы внесены в базу данных.',
            reply_markup=main_markup()
            )


def process_operation_step(message):
    if message.text == 'Создание':
        try:
            chat_id = message.chat.id
            bot.send_message(
                chat_id,
                'Вы выбрали создание записи. Загружаю список прицепов...'
            )
            list_trailers = db.read_trailers()
            for trailer in list_trailers:
                bot.send_message(
                    chat_id,
                    f'{trailer}'
                )
            # markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                chat_id,
                'Прицеп уже есть в доступном списке ?',
                reply_markup=choose_markup()
            )
            bot.register_next_step_handler(msg, create_operation_step)
        except Exception:
            bot.reply_to(message, 'На этапе создания записи произошла ошибка.')
    elif message.text == 'Чтение':
        try:
            chat_id = message.chat.id
            # user_dict[chat_id] = User(message.chat.id)
            bot.send_message(
                chat_id,
                'Вы выбрали чтение записей из базы данных.'
            )
            # Место для следующего шага по чтению записей.
        except Exception:
            bot.reply_to(message, 'На этапе чтения записей произошла ошибка.')
    elif message.text == 'Редактирование':
        try:
            chat_id = message.chat.id
            # user_dict[chat_id] = User(message.chat.id)
            bot.send_message(
                chat_id,
                'Вы выбрали редактирование записей в базе данных.'
            )
            # Место для следующего шага по редактированию записей.
        except Exception:
            bot.reply_to(message, 'На этапе редактирования записей произошла ошибка.')
    elif message.text == 'Удаление':
        try:
            chat_id = message.chat.id
            # user_dict[chat_id] = User(message.chat.id)
            bot.send_message(
                chat_id,
                'Вы выбрали удаление записей из базы данных.'
            )
            # Место для следующего шага по удалению записей.
        except Exception:
            (message, 'На этапе удаления записей произошла ошибка.')
    else:
        bot.send_message(
            message.chat.id,
            'Для работы с ботом пользуйтесь кнопками под строкой ввода \n'
            'Если после ввода комманды /start кнопки не появились \n'
            'Используйте команду повторно'
            )


@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video'])
def text_filter(message):
    try:
        chat_id = message.chat.id
        db.check_user(chat_id)
        bot.send_message(
            chat_id,
            'Бот не поддерживает работу с текстом. \n'
            'Для дальнейшей работы вызовите главное меню \n'
            'Главное меню - /start'
        )
    except Exception:
        (message,
         'Вы не прошли процесс регистрации \n'
         '/start')


bot.polling(non_stop=True)
