
# from flask import Flask, request
# import telebot
import time
# import random
# import string
from config import bot, db
# from config import URL
from markups import main_markup
from branches.main_branch import main_operation_step


# secret = ''.join(random.choice(string.ascii_letters) for x in range(20))

# bot.remove_webhook()
# time.sleep(1)
# bot.set_webhook(url="https://{}.pythonanywhere.com/{}".format(URL, secret))

# app = Flask(__name__)

# @app.route('/{}'.format(secret), methods=["POST"])
# def webhook():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     print("Message")
#     return "ok", 200


@bot.message_handler(commands=['start'])
def first_step(message):
    try:
        chat_id = message.chat.id
        db.create_tables()
        if (not db.check_user(message.from_user.id)):
            bot.send_message(
                chat_id,
                'Сообщение для незарегистрированных пользователей. \n'
                'Добро пожаловать в КО-2 бот.\n'
                f'Ваш id: {chat_id}.\n'
                f'Ваше имя: {message.from_user.first_name} '
                f'{message.from_user.last_name}\n'
                'После введения ключа доступа вы будете внесены '
                'в базу данных.\n'
                'Убедитесь в коррекности имени и фамилии.\n'
                'При необходимости измените данные в настройках телеграм.'
                )
            time.sleep(2)
            bot.send_message(
                chat_id,
                'Введите ключ доступа:'
                )
        else:
            msg = bot.send_message(
                chat_id,
                'Главное меню.',
                reply_markup=main_markup()
                )
            bot.register_next_step_handler(msg, main_operation_step)
    except Exception:
        bot.reply_to(
            message,
            f'Функция: {first_step.__name__} \n'
            f'{Exception} \n'
            'Главное меню - /start'
            )


@bot.message_handler(commands=['CHMZAP'])
def register_step(message):
    try:
        chat_id = message.chat.id
        if db.check_user(chat_id):
            msg = bot.send_message(
                chat_id,
                'Главное меню.',
                reply_markup=main_markup()
                )
            bot.register_next_step_handler(msg, main_operation_step)
        else:
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            db.create_user(chat_id, first_name, last_name)
            bot.send_message(
                message.chat.id,
                'Регистрация успешна. Вы внесены в базу данных.'
                'Главное меню - /start'
                )
    except Exception:
        bot.reply_to(
            message,
            f'Функция: {register_step.__name__} \n'
            f'{Exception} \n'
            'Главное меню - /start'
            )


@bot.message_handler(commands=['count'])
def count_troubles(message):
    try:
        chat_id = message.chat.id
        if db.check_user(chat_id):
            troubles = db.count_troubles()
            bot.send_message(
                chat_id,
                f'Количество записей в базе данных: {troubles[0]}',
                )
    except Exception:
        bot.reply_to(
            message,
            f'Функция: {register_step.__name__} \n'
            f'{Exception} \n'
            'Главное меню - /start'
            )


@bot.message_handler(
    content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video'])
def text_filter(message):
    try:
        bot.send_message(
            message.chat.id,
            'Бот не поддерживает работу с текстом. \n'
            'Для дальнейшей работы вызовите главное меню \n'
            'Главное меню - /start'
            )
    except Exception:
        bot.reply_to(
            message,
            f'Функция: {text_filter.__name__} \n'
            f'{Exception} \n'
            'Главное меню - /start'
            )


bot.polling(non_stop=True)
