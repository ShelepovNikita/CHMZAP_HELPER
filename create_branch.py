

from datetime import datetime
from config import bot, db
from markups import choose_markup
from telebot import types

user_dict = {}


class Trouble:
    def __init__(self, column):
        self.column = column
        keys = [
            'date',
            'order_num',
            'problem',
            'document',
            'status',
            'trailer_id',
            'causer_id',
            'user_id'
        ]
        for key in keys:
            self.key = None


class Trailer:
    def __init__(self, column):
        self.column = column
        self.designation = None


# Прицеп есть в доступном списке--> Либо есть либо нет.
def create_operation_step(message):
    # Прицеп есть в списке.
    if message.text == 'Да':
        try:
            msg = bot.send_message(
                message.chat.id,
                'Для дальнейшего создания записи введите '
                'порядковый номер прицепа '
                '(из списка: первый параметр в скобках без кавычек - число)'
            )
            bot.register_next_step_handler(msg, create_operation_trailer_step)
        except Exception:
            bot.reply_to(message, 'Что то пошло не так...')
    # Прицеп отсутствует в списке.
    elif message.text == 'Нет':
        try:
            msg = bot.send_message(
                message.chat.id,
                'Введите номер прицепа в формате ХХХХХ-ХХХХХХХ-ХХ (как в 1С)'
            )
            bot.register_next_step_handler(msg, intermediate_func)
        except Exception:
            bot.reply_to(message, 'Что то пошло не так...')
    else:
        bot.send_message(
            message.chat.id,
            'Что то пошло не по плану, необходимо начать сначала.'
            )


# Прицеп отсутствует в доступном списке --> Создание прицепа
def intermediate_func(message):
    try:
        chat_id_trailer = message.chat.id
        user_dict[chat_id_trailer] = Trailer(message.chat.id)
        trailer = user_dict[chat_id_trailer]
        trailer.designation = message.text
        bot.send_message(
            message.chat.id,
            'Подтвердите ввод обозначения прицепа'
            )
        msg = bot.send_message(
            message.chat.id,
            f'Вы ввели: {message.text}',
            reply_markup=choose_markup()
            )
        bot.register_next_step_handler(msg, confirm_intermediate_func)
    except Exception:
        bot.reply_to(message, 'Что то пошло не так...')


# Создание прицепа --> Подтверждение создания
def confirm_intermediate_func(message):
    if message.text == 'Да':
        try:
            markup1 = types.ReplyKeyboardRemove(selective=False)
            chat_id_trailer = message.chat.id
            trailer = user_dict[chat_id_trailer]
            designation = trailer.designation
            db.create_trailer(designation)
            bot.send_message(
                message.chat.id,
                f'Прицеп {designation} создан!',
                reply_markup=markup1
            )
            trailer_to_markup = db.search_trailer_designation(designation)
            markup2 = types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=2
                )
            itempbtn1 = types.KeyboardButton(f'{trailer_to_markup[0]}')
            markup2.add(itempbtn1)
            msg = bot.send_message(
                message.chat.id,
                'Для продолжения нажмите кнопку с цифрой...',
                reply_markup=markup2
            )
            bot.register_next_step_handler(msg, create_operation_trailer_step)
        except Exception:
            bot.reply_to(message, 'Что то пошло не так...')
    elif message.text == 'Нет':
        try:
            bot.send_message(
                message.chat.id,
                'Вернитесь в главное меню \n'
                '/start'
            )
        except Exception:
            bot.reply_to(message, 'Что то пошло не так...')


# Выбор виновника --> Внесение данных для записи
def create_operation_trailer_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = Trouble(message.chat.id)
        trouble = user_dict[chat_id]
        trailer = db.search_trailer(message.text)
        trouble.trailer_id = message.text
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(
            message.chat.id,
            f'Вы выбрали прицеп {trailer[0]}. '
            'Выберите порядковый номер виновника '
            '(из списка: первый параметр в скобках без кавычек - число)',
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, create_operation_causer_step)
        list_causers = db.read_causers()
        for causer in list_causers:
            bot.send_message(
                message.chat.id,
                f'{causer}'
            )
    except Exception:
        bot.reply_to(message, 'Что то пошло не так...')


# Внесение данных для записи --> Внесение в базу данных
def create_operation_causer_step(message):
    try:
        chat_id = message.chat.id
        trouble = user_dict[chat_id]
        causer = db.search_causer(message.text)
        trouble.causer_id = message.text
        bot.send_message(
            message.chat.id,
            f'Вы выбрали виновника {causer}. \n'
            'Для внесения записи необходимо внести данные в формате: \n'
            'Заказ|Описание проблемы|СЗ для решения|'
            'Статус проблемы \n'
            'Пояснение по статусу проблемы, если СЗ решает проблему '
            'и она больше не повторится вносим цифру 1, если проблема требует '
            'дальнейшего изменения в КД и не решена то вносим цифру 0. \n'
            'Пример ввода записи: '
        )
        bot.send_message(
            message.chat.id,
            '460/1|Не заложили в ЗИП ручку от трамвая|Без СЗ, '
            'выдали со склада|0'
        )
        msg = bot.send_message(
            message.chat.id,
            'Ожидание ввода ...'
        )
        bot.register_next_step_handler(msg, final_create_operation)
    except Exception:
        bot.reply_to(message, 'Что то пошло не так...')


def final_create_operation(message):
    try:
        chat_id = message.chat.id
        trouble = user_dict[chat_id]
        trouble.date = str(datetime.now().date())
        trouble.user_id = chat_id
        problem = message.text
        problem_split = problem.split('|')
        trouble.order_num = problem_split[0]
        trouble.problem = problem_split[1]
        trouble.document = problem_split[2]
        trouble.status = problem_split[3]
        if trouble.status == 1:
            status = 'Проблема решена'
        else:
            status = 'Требует решения'
        trailer = db.search_trailer(trouble.trailer_id)
        causer = db.search_causer(trouble.causer_id)
        bot.send_message(
            message.chat.id,
            'Запись для внесения в базу данных: \n'
            f'Дата: {trouble.date} \n'
            f'Номер заказа: {trouble.order_num} \n'
            f'Проблема: {trouble.problem} \n'
            f'Документ: {trouble.document} \n'
            f'Статус проблемы: {status} \n'
            f'Прицеп: {trailer[0]} \n'
            f'Виновник: {causer[0]} \n'
            f'Смена: {message.from_user.last_name} \n'
        )
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=2
            )
        itempbtn1 = types.KeyboardButton('Подтвердить')
        itempbtn2 = types.KeyboardButton('/start')
        markup.add(itempbtn1, itempbtn2)
        msg = bot.send_message(
            chat_id,
            'Если данные верны нажмите подтвердить \n'
            'Если допущена ошибка, то пройдите процесс создания '
            'записи из главного меню с самого начала.',
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, confirm_final_create_operation)
    except Exception:
        bot.reply_to(message, 'Что то пошло не так...')


def confirm_final_create_operation(message):
    try:
        chat_id = message.chat.id
        trouble = user_dict[chat_id]
        create_list = [
            trouble.date,
            trouble.order_num,
            trouble.problem,
            trouble.document,
            trouble.status,
            trouble.trailer_id,
            trouble.causer_id,
            trouble.user_id,
        ]
        db.create_trouble(create_list)
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(
            message.chat.id,
            'Запись успешно внесена в базу данных!',
            reply_markup=markup
        )
        bot.send_message(
            message.chat.id,
            '/start'
        )
    except Exception:
        bot.reply_to(message, 'Что то пошло не так...')
