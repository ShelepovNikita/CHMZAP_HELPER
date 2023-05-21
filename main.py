
import os
from flask import Flask, request
import telebot
import time
import random
import string
from config import bot, db
from config import URL
from markups import main_markup, main_btn
from branches.main_branch import main_operation_step
from telebot import types
from dotenv import load_dotenv

load_dotenv()


secret = ''.join(random.choice(string.ascii_letters) for x in range(20))

bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url="https://{}.pythonanywhere.com/{}".format(URL, secret))

app = Flask(__name__)

app.config['TOKEN'] = os.getenv('BOT_TOKEN')
app.config['URL'] = os.getenv('URL')
app.config['GROUP_ID'] = os.getenv('GROUP_ID')
app.config['SENDER'] = os.getenv('SENDER')
app.config['PASSWORD'] = os.getenv('PASSWORD')

@app.route('/{}'.format(secret), methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    print("Message")
    return "ok", 200


@bot.message_handler(commands=['start'])
def first_step(message):
    try:
        if message.chat.type == 'private':
            chat_id = message.chat.id
            db.create_tables()
            if (not db.check_user(message.from_user.id)):
                bot.send_message(
                    chat_id,
                    '<i>Сообщение для незарегистрированных '
                    'пользователей.</i> \n'
                    '\n'
                    'Добро пожаловать в КО-2 бот.\n'
                    f'Ваш id: {chat_id}.\n'
                    f'Ваше имя: {message.from_user.first_name} '
                    f'{message.from_user.last_name}\n'
                    'После введения ключа доступа вы будете внесены '
                    'в базу данных.\n'
                    'Убедитесь в коррекности имени и фамилии.\n'
                    'При необходимости измените данные в настройках телеграм.',
                    parse_mode='HTML'
                    )
                time.sleep(1)
                bot.send_message(
                    chat_id,
                    'Введите ключ доступа: \n'
                    '\n'
                    '<i>Ожидание ввода...</i>',
                    parse_mode='HTML'
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
        if message.chat.type == 'private':
            chat_id = message.chat.id
            if db.check_user(chat_id):
                msg = bot.send_message(
                    chat_id,
                    'Главное меню.',
                    reply_markup=main_markup()
                    )
                bot.register_next_step_handler(msg, main_operation_step)
            else:
                data = (
                    chat_id,
                    message.from_user.first_name,
                    message.from_user.last_name,
                )
                db.create_user(data)
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
            f'Функция: {count_troubles.__name__} \n'
            f'{Exception} \n'
            'Главное меню - /start'
            )


@bot.message_handler(commands=['help'])
def help(message):
    try:
        chat_id = message.chat.id
        bot.send_message(
            chat_id,
            'Бот создан для удобного обращения '
            'к базе данных для контроля качества продукции '
            'ПАО "УралАвтоПрицеп". \n'
            'Для работы с базой данных необходим ключ доступа.'
        )
    except Exception:
        bot.reply_to(
            message,
            f'Функция: {help.__name__} \n'
            f'{Exception} \n'
            'Главное меню - /start'
            )


@bot.message_handler(commands=['check_trouble'])
def check_trouble(message):
    try:
        if message.chat.type == 'private':
            chat_id = message.chat.id
            if db.check_user(message.from_user.id):
                msg = bot.send_message(
                    chat_id,
                    'Для вывода интересующией записи в базе данных '
                    'введите её порядковый номер \n'
                    '\n'
                    '<i>Ожидание ввода...</i>',
                    parse_mode='HTML',
                    reply_markup=main_btn()
                )
                bot.register_next_step_handler(msg, check_trouble_next_step)
    except Exception:
        bot.reply_to(
            message,
            f'Функция: {check_trouble.__name__} \n'
            f'{Exception} \n'
            'Главное меню - /start'
            )


def check_trouble_next_step(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text == 'Главное меню':
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(
                chat_id,
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        else:
            if user_text.isdigit():
                trouble_db = db.search_by_id_in_troubles(user_text)
                id = trouble_db[0]
                date = trouble_db[1]
                order_num = trouble_db[2]
                problem = trouble_db[3]
                document = trouble_db[4]
                status = trouble_db[5]
                trailer_id = trouble_db[6]
                causer_id = trouble_db[7]
                user_id = trouble_db[8]

                if status is None:
                    status = None
                elif status == 0:
                    status = 'Требует решения'
                else:
                    status = 'Проблема решена'

                trailer = db.search_trailer(trailer_id)[0]

                if causer_id is None:
                    causer = None
                else:
                    causer = db.search_causer_name(trouble_db[7])[0]
                trouble_user = db.search_user_last_name(user_id)[0]
                markup = types.ReplyKeyboardRemove(selective=False)
                bot.send_message(
                    chat_id,
                    f'id: {id} \n'
                    f'Дата: {date} \n'
                    f'Номер заказа: {order_num} \n'
                    f'Проблема: {problem} \n'
                    f'Документ: {document} \n'
                    f'Статус проблемы: {status} \n'
                    f'Прицеп: {trailer} \n'
                    f'Виновник: {causer} \n'
                    f'Смена: {trouble_user} \n',
                    reply_markup=markup
                )
    except Exception:
        bot.reply_to(
            message,
            f'Функция: {check_trouble_next_step.__name__} \n'
            f'{Exception} \n'
            'Главное меню - /start'
            )


@bot.message_handler(commands=['change_mail'])
def change_mail(message):
    try:
        chat_id = message.chat.id
        if db.check_user(chat_id):
            email = db.search_user_emal(chat_id)[0]
            msg = bot.send_message(
                chat_id,
                f'Ваш адрес email в базе данных: {email} \n'
                'Введите новый адрес email для пользователя: '
                f'{message.from_user.first_name} '
                f'{message.from_user.last_name} \n'
                '\n'
                '<i>Ожидание ввода:</i>',
                parse_mode='HTML',
            )
            bot.register_next_step_handler(msg, update_email)
    except Exception:
        bot.reply_to(
            message,
            f'Функция: {change_mail.__name__} \n'
            f'{Exception} \n'
            'Главное меню - /start'
            )


def update_email(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if '@' in user_text:
            mail = user_text.strip()
            db.create_email(mail, chat_id)
            msg = bot.send_message(
                chat_id,
                'Адрес электронной почты успешно внесен в базу данных ! \n'
                f'Ваш адрес: {mail} \n'
                'Для возврата в главное меню используйте команду - /start'
            )
        else:
            msg = bot.send_message(
                chat_id,
                'Введите адрес электронной почты! \n'
                '\n'
                '<i>Ожидание ввода...</i>',
                parse_mode='HTML',
                reply_markup=main_btn()
            )
            bot.register_next_step_handler(msg, update_email)
    except Exception:
        bot.reply_to(
            message,
            f'Функция: {update_email.__name__} \n'
            f'{Exception} \n'
            'Главное меню - /start'
            )


@bot.message_handler(
    content_types=['text', 'audio', 'document', 'animation',
                   'game', 'photo', 'sticker', 'video',
                   'video_note', 'voice', 'contact', 'location',
                   'venue', 'dice', 'invoice', 'successful_payment',
                   'connected_website', 'poll', 'passport_data',
                   'web_app_data'])
def text_filter(message):
    try:
        if message.chat.type == 'private':
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(
                message.chat.id,
                'Бот не поддерживает работу с данными \n'
                'Используйте команды! \n'
                'Главное меню - /start',
                reply_markup=markup
                )
    except Exception:
        bot.reply_to(
            message,
            f'Функция: {text_filter.__name__} \n'
            f'{Exception} \n'
            'Главное меню - /start'
            )


if __name__ == '__main__':
    app.run()
