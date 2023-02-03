
from flask import Flask, request
import telebot
import time
import random
import string
from markups import gen_main_markup, gen_edit_markup
import config


secret = ''.join(random.choice(string.ascii_letters) for x in range(20))
bot = telebot.TeleBot(config.TOKEN, threaded=False)

bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url="https://{}.pythonanywhere.com/{}".format(config.URL, secret))

app = Flask(__name__)

# Часть кода для pythonanywhere


@app.route('/{}'.format(secret), methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    print("Message")
    return "ok", 200


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


@bot.message_handler(commands=['start'])
def first_step(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в CHMZAP HELPER бот. "
        "Введите ключ доступа:"
        )


@bot.message_handler(content_types=['text'])
def input_keys_words(message):
    # user_id = message.from_user.id
    # add_into_users(user_id)
    if message.text in config.keys_list:
        bot.send_message(
            message.chat.id,
            "Верный ключ доступа. Действия с базой данных:",
            reply_markup=gen_main_markup()
        )
    else:
        bot.send_message(
            message.chat.id,
            'Ключ не верный, запросите ключ у администратора.'
        )


# Обработчик нажатия на кнопки. Именно здесь заключена основная логика бота.


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "/read":
        bot.send_message(
            call.message.chat.id,
            "Эта функция никуда не ведет, пока что..."
        )

    elif call.data == "/write":
        bot.send_message(
            call.message.chat.id,
            'Вы выбрали запись. Выберите действие:',
            reply_markup=gen_edit_markup()
        )

    elif call.data == "/edit":
        bot.send_message(
            call.message.chat.id,
            'Раздел редактирования отвалился нахуй по причине отсутствия подключения к базе данных',
            reply_markup=gen_edit_markup()
        )
    elif call.data == "/delete":
        bot.send_message(
            call.message.chat.id,
            'Удалять нечего, ничего итак не работает',
            reply_markup=gen_edit_markup()
        )


if __name__ == '__main__':
    app.run()
