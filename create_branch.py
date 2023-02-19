

from datetime import datetime
from config import bot, db
from markups import choose_markup, choose_causer, step_back, create_markup, no_btn
from telebot import types
from transform import transform_to_1c

user_dict = {}


class Trouble:
    def __init__(self, column):
        self.column = column
        self.date = None
        self.order_num = None
        self.problem = None
        self.document = None
        self.status = None
        self.trailer_id = None
        self.causer_id = None
        self.user_id = None


class Trailer:
    def __init__(self, column):
        self.column = column
        self.designation = None


def process_operation_step(message):
    if message.text == 'Шаг назад':
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


# Прицеп есть в доступном списке--> Либо есть либо нет.
def create_operation_step(message):
    # Прицеп есть в списке.
    if message.text == 'Да':
        try:
            # markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                message.chat.id,
                'Для дальнейшего создания записи введите \n'
                'порядковый номер прицепа \n'
                '(из списка: первый параметр в скобках без кавычек - число) \n',
                reply_markup=step_back()
            )
            bot.register_next_step_handler(msg, create_operation_trailer_step)
        except Exception:
            bot.reply_to(message,
                         'Критическая ошибка! \n'
                         'Главное меню - /start'
                         )
    # Прицеп отсутствует в списке.
    elif message.text == 'Нет':
        try:
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                message.chat.id,
                'Введите обозначение прицепа \n'
                'Обозначение будет автоматически переведено как в 1С',
                reply_markup=markup
            )
            bot.register_next_step_handler(msg, intermediate_func)
        except Exception:
            bot.reply_to(message,
                         'Критическая ошибка! \n'
                         'Главное меню - /start'
                         )
    elif message.text == 'Главное меню':
        try:
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                message.chat.id,
                'Для возврата используйте команду - /start',
                reply_markup=markup
            )
        except Exception:
            bot.reply_to(message,
                         'Критическая ошибка! \n'
                         'Главное меню - /start'
                         )
    else:
        bot.reply_to(message,
                     'Ошибка! Используйте кнопки под строкой ввода \n'
                     'Прицеп уже есть в доступном списке ?',
                     reply_markup=choose_markup()
                     )
        bot.register_next_step_handler(message, create_operation_step)


# Прицеп отсутствует в доступном списке --> Создание прицепа
def intermediate_func(message):
    try:
        chat_id_trailer = message.chat.id
        user_dict[chat_id_trailer] = Trailer(message.chat.id)
        trailer = user_dict[chat_id_trailer]
        trailer.designation = transform_to_1c(message.text)
        bot.send_message(
            message.chat.id,
            'Подтвердите ввод обозначения прицепа'
            )
        msg = bot.send_message(
            message.chat.id,
            f'Вы ввели: {trailer.designation}',
            reply_markup=choose_markup()
            )
        bot.register_next_step_handler(msg, confirm_intermediate_func)
    except Exception:
        bot.reply_to(message,
                     'Ошибка! \n'
                     'Не забывай про тире \n'
                     'Например 99064-100-01 \n'
                     'Вводи по новой, я жду'
                     )
        bot.register_next_step_handler(message, intermediate_func)


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
            # СЮДА ДОПИСАТЬ ДВА ОБРАБОТЧИКА
            # ОДИН НА ЛОГИКУ ПРОВЕРКИ ВВОДА НОМЕРА ПРИЦЕПА
            # ВТОРОЙ НА ЛОГИКУ ПРОВЕРКИ НАЛИЧИЯ ТАКОГО ПРИЦЕПА В БАЗЕ
            bot.reply_to(message,
                         'Прицеп не может быть создан \n'
                         'Вероятная причина - такой прицеп уже есть',
                         )
            chat_id = message.chat.id
            bot.send_message(
                chat_id,
                'Загружаю список прицепов...'
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
    elif message.text == 'Нет':
        try:
            bot.send_message(
                message.chat.id,
                'Для возврата на шаг "ввод обозначения прицепа" \n'
                'Нажмите кнопку "Нет" повторно.',
                reply_markup=no_btn()
            )
            bot.register_next_step_handler(message, create_operation_step)
        except Exception:
            bot.reply_to(message, 'Что то пошло не так...')
    elif message.text == 'Шаг назад':
        try:
            bot.send_message(
                message.chat.id,
                'Нажмите кнопку "Шаг назад"',
                reply_markup=step_back()
            )
            bot.register_next_step_handler(message, process_operation_step)
        except Exception:
            bot.reply_to(message, 'Что то пошло не так...')
    elif message.text == 'Главное меню':
        try:
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                message.chat.id,
                'Для возврата используйте команду - /start',
                reply_markup=markup
            )
        except Exception:
            bot.reply_to(message,
                         'Критическая ошибка! \n'
                         'Главное меню - /start'
                         )
    else:
        bot.reply_to(message,
                     'Ошибка! Используйте кнопки под строкой ввода \n'
                     'Подтвердите ввод обозначения прицепа',
                     reply_markup=choose_markup()
                     )
        bot.register_next_step_handler(message, confirm_intermediate_func)


# Выбор виновника --> Внесение данных для записи
def create_operation_trailer_step(message):
    if message.text == 'Шаг назад':
        try:
            bot.send_message(
                message.chat.id,
                'Для возврата на шаг "список прицепов" \n'
                'Нажмите кнопку "Шаг назад" повторно.',
                reply_markup=step_back()
            )
            bot.register_next_step_handler(message, process_operation_step)
        except Exception:
            bot.reply_to(message,
                         'Критическая ошибка! \n'
                         'Главное меню - /start'
                         )
    else:
        try:
            if message.text == 'Нет':
                chat_id = message.chat.id
                trouble = user_dict[chat_id]
                if trouble.trailer_id:
                    trailer = db.search_trailer(trouble.trailer_id)
                    markup = types.ReplyKeyboardRemove(selective=False)
                    msg = bot.send_message(
                        message.chat.id,
                        f'Вы выбрали прицеп: {trailer[0]} \n'
                        'Введите проблему \n',
                        reply_markup=markup
                    )
                    bot.register_next_step_handler(msg, create_trouble_to_database)
            else:
                chat_id = message.chat.id
                user_dict[chat_id] = Trouble(message.chat.id)
                trouble = user_dict[chat_id]
                trailer = db.search_trailer(message.text)
                trouble.trailer_id = message.text
                markup = types.ReplyKeyboardRemove(selective=False)
                msg = bot.send_message(
                    message.chat.id,
                    f'Вы выбрали прицеп: {trailer[0]} \n'
                    'Введите проблему \n',
                    reply_markup=markup
                )
                bot.register_next_step_handler(msg, create_trouble_to_database)
            # list_causers = db.read_causers()
            # for causer in list_causers:
            #     bot.send_message(
            #         message.chat.id,
            #         f'{causer}'
            #     )
        except Exception:
            bot.reply_to(message,
                         'Ошибка! \n'
                         'Введите порядковый номер прицепа из списка \n'
                         'Либо вернитесь на шаг назад с помощью кнопки \n',
                         reply_markup=step_back())
            bot.register_next_step_handler(message, create_operation_trailer_step)


def create_trouble_to_database(message):
    try:
        chat_id = message.chat.id
        trouble = user_dict[chat_id]
        trouble.user_id = chat_id
        problem = message.text
        trouble.problem = problem
        bot.send_message(
            message.chat.id,
            'Подтвердите ввод проблемы'
            )
        msg = bot.send_message(
            message.chat.id,
            f'Вы ввели: {trouble.problem}',
            reply_markup=choose_markup()
            )
        bot.register_next_step_handler(msg, confirm_trouble_to_database)
    except Exception:
        bot.reply_to(message,
                     'Критическая ошибка! \n'
                     'Главное меню - /start'
                     )


def confirm_trouble_to_database(message):
    if message.text == 'Да':
        try:
            chat_id = message.chat.id
            trouble = user_dict[chat_id]
            trailer = db.search_trailer(trouble.trailer_id)
            trouble.date = str(datetime.now().date())
            if trouble.status is None:
                status = None
            elif trouble.status == 0:
                status = 'Требует решения'
            else:
                status = 'Проблема решена'
            if trouble.causer_id is None:
                causer = None
            bot.send_message(
                message.chat.id,
                'Запись для внесения в базу данных: \n'
                f'Дата: {trouble.date} \n'
                f'Номер заказа: {trouble.order_num} \n'
                f'Проблема: {trouble.problem} \n'
                f'Документ: {trouble.document} \n'
                f'Статус проблемы: {status} \n'
                f'Прицеп: {trailer[0]} \n'
                f'Виновник: {causer} \n'
                f'Смена: {message.from_user.last_name} \n'
                'Чтобы дополнить запись выберите соответствующую кнопку для ввода. \n'
                'Чтобы внести запись в базу данных нажмите "Внести запись" \n',
                reply_markup=create_markup()
            )
            bot.register_next_step_handler(message, write_trouble_to_database)
        except Exception:
            bot.reply_to(message,
                         'Критическая ошибка! \n'
                         'Главное меню - /start'
                         )
    elif message.text == 'Нет':
        try:
            bot.send_message(
                message.chat.id,
                'Для возврата на шаг "ввод проблемы" \n'
                'Нажмите кнопку "Нет" повторно.',
                reply_markup=no_btn()
            )
            bot.register_next_step_handler(message, create_operation_trailer_step)
        except Exception:
            bot.reply_to(message,
                         'Критическая ошибка! \n'
                         'Главное меню - /start'
                         )
    else:
        bot.reply_to(message,
                     'Ошибка! \n'
                     'Подтвердите ввод проблемы \n'
                     'Используйте кнопки под клавиатурой',
                     reply_markup=choose_markup()
                     )
        bot.register_next_step_handler(message, confirm_trouble_to_database)

# ===================================================================================================================


def write_trouble_to_database(message):
    if message.text == 'Внести запись':
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
                'Запись успешно внесена \n'
                'Главное меню - /start',
                reply_markup=markup
            )
        except Exception:
            bot.reply_to(message,
                         'Запись не внесена \n'
                         'Попробуйте еще раз \n'
                         'Главное меню - /start'
                         )
    elif message.text == 'Номер заказа':
        try:
            bot.send_message(
                message.chat.id,
                'Введите номер заказа',
            )
            bot.register_next_step_handler(message, create_order_num)
        except Exception:
            pass


def create_order_num(message):
    try:
        chat_id = message.chat.id
        trouble = user_dict[chat_id]
        trouble.order_num = message.text
        bot.send_message(
            message.chat.id,
            'Подтвердите ввод заказа'
            )
        msg = bot.send_message(
            message.chat.id,
            f'Вы ввели: {trouble.order_num}',
            reply_markup=choose_markup()
        )
        if msg.text == 'Да':
            bot.send_message(
                message.chat.id,
                'kek'
                )
    except Exception:
        bot.reply_to(message,
                     'Критическая ошибка! \n'
                     'Главное меню - /start'
                     )


# Внесение данных для записи --> Внесение в базу данных
def create_operation_causer_step(message):
    try:
        chat_id = message.chat.id
        trouble = user_dict[chat_id]
        causer = db.search_causer(message.text)
        trouble.causer_id = message.text
        bot.send_message(
            message.chat.id,
            f'Вы выбрали виновника: {causer[0]} \n'
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
