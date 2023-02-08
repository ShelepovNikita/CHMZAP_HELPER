
from flask import Flask, request
import telebot
import time
import random
import string
from markups import gen_main_markup, answer_markup
import config
import database
from datetime import datetime

# CREATE = 0
# READ = 0
# UPDATE = 0
# DELETE = 0
# CAUSERS = 0

# secret = ''.join(random.choice(string.ascii_letters) for x in range(20))
bot = telebot.TeleBot(config.TOKEN, threaded=False)

db = database.Database('chmzap_sq.sqlite')

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


# Часть кода для локального запуска


# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.headers.get('content-type') == 'application/json':
#         update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
#         bot.process_new_updates([update])
#         return ''
#     else:
#         abort(403)
#     if request.method == 'POST':
#         return Response('OK', status=200)
#     else:
#         return ' '

REGISTER = False
# Ветка создания проблемы.
FIND_TRAILER = False
FIND_CAUSER = False
CREATE_TROUBLE = False
LIST_TO_PUSH = []


@bot.message_handler(commands=['start'])
def first_step(message):
    db.create_tables()
    global REGISTER
    if (not db.check_user(message.from_user.id)):
        REGISTER = True
        bot.send_message(
            message.chat.id,
            'Сообщение для незарегистрированных пользователей.'
            )
        bot.send_message(
            message.chat.id,
            'Добро пожаловать в КО-2 бот.'
            )
        bot.send_message(
            message.chat.id,
            f'Ваш id: {message.from_user.id}. '
            f'Ваше имя: {message.from_user.first_name} '
            f'{message.from_user.last_name}.'
            )
        bot.send_message(
            message.chat.id,
            'После введения ключа доступа вы будете внесены в базу данных. '
            'Убедитесь в коррекности имени и фамилии. '
            'При необходимости измените данные в настройках телеграм.'
            )
        bot.send_message(
            message.chat.id,
            'Введите ключ доступа:'
            )
    else:
        bot.send_message(
            message.chat.id,
            'Главное меню.',
            reply_markup=gen_main_markup()
            )


@bot.message_handler(commands=['CHMZAP'])
def register_step(message):
    global REGISTER
    if REGISTER:
        if message.text == '/CHMZAP':
            user_id = message.from_user.id
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            db.create_user(user_id, first_name, last_name)
            bot.send_message(
                message.chat.id,
                'Регистрация успешна. Вы внесены в базу данных.',
            )
            REGISTER = False
        else:
            bot.send_message(
                message.chat.id,
                'Ключ доступа не верный.',
            )


@bot.message_handler(content_types=['text'])
def input_key_word(message):
    global FIND_TRAILER
    global FIND_CAUSER
    global CREATE_TROUBLE
    global LIST_TO_PUSH
    if FIND_TRAILER:
        trailer_id = message.text
        trailer = db.search_trailer(trailer_id)
        bot.send_message(
            message.chat.id,
            f'Вы выбрали прицеп {trailer}. '
            'Выберите порядковый номер виновника '
            '(из списка: первый параметр в скобках без кавычек - число)'
        )
        FIND_TRAILER = False
        FIND_CAUSER = True
        LIST_TO_PUSH.append(trailer_id)
        list_causers = db.read_causers()
        for causer in list_causers:
            bot.send_message(
                message.chat.id,
                f'{causer}'
            )

    elif FIND_CAUSER:
        causer_id = message.text
        causer = db.search_causer(causer_id)
        bot.send_message(
            message.chat.id,
            f'Вы выбрали виновника {causer}. '
            'Для внесения записи необходимо внести данные в формате: '
        )
        bot.send_message(
            message.chat.id,
            'Заказ.Описание проблемы.СЗ для решения.'
            'Статус проблемы'
        )
        bot.send_message(
            message.chat.id,
            'Пояснение по статусу проблемы, если СЗ решает проблему '
            'и она больше не повторится вносим цифру 1, если проблема требует '
            'дальнейшего изменения в КД и не решена то вносим цифру 0. '
            'Пример ввода записи:'
        )
        bot.send_message(
            message.chat.id,
            '460/1.Не заложили в ЗИП ручку от трамвая.Без СЗ, '
            'выдали со склада.0'
        )
        bot.send_message(
            message.chat.id,
            'Ожидание ввода ...'
        )
        FIND_CAUSER = False
        CREATE_TROUBLE = True
        LIST_TO_PUSH.append(causer_id)

    elif CREATE_TROUBLE:
        problem = message.text
        problem_split = problem.split('.')
        current_date = str(datetime.now().date())
        finish_list = []
        finish_list.append(current_date)
        finish_list = finish_list + problem_split + LIST_TO_PUSH
        user = db.search_user(message.from_user.id)
        finish_list.append(*user)
        bot.send_message(
            message.chat.id,
            'Запись для внесения в базу данных: '
            f' {finish_list}'
        )
        db.create_trouble(finish_list)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == '/create':
        list_trailers = db.read_trailers()
        bot.send_message(
            call.message.chat.id,
            'Вы выбрали создание записи. Загружаю список прицепов...'
        )
        for trailer in list_trailers:
            bot.send_message(
                call.message.chat.id,
                f'{trailer}'
            )
        bot.send_message(
                call.message.chat.id,
                'Прицеп уже есть в доступном списке ?',
                reply_markup=answer_markup()
            )

    elif call.data == '/yes':
        global FIND_TRAILER
        FIND_TRAILER = True
        bot.send_message(
            call.message.chat.id,
            'Для дальнейшего создания записи введите порядковый номер прицепа '
            '(из списка: первый параметр в скобках без кавычек - число)'
        )

    elif call.data == '/no':
        bot.send_message(
            call.message.chat.id,
            'Вы выбрали создание нового прицепа.'
        )

    elif call.data == '/read':
        bot.send_message(
            call.message.chat.id,
            'Вы выбрали чтение записей. Эта функция никуда не ведет, пока что...',
            # reply_markup=gen_edit_markup()
        )

    elif call.data == '/update':
        bot.send_message(
            call.message.chat.id,
            'Вы выбрали редактирование записи. Эта функция никуда не ведет, пока что...',
            # reply_markup=gen_edit_markup()
        )
    elif call.data == '/delete':
        bot.send_message(
            call.message.chat.id,
            'Вы выбрали удаление записи. Эта функция никуда не ведет, пока что...',
            # reply_markup=gen_edit_markup()
        )

bot.polling()
# if __name__ == '__main__':
#     app.run()
