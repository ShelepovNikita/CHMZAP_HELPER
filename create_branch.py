

from datetime import datetime
from config import bot, db
from markups import (
    choose_markup,
    choose_causer,
    create_markup,
    main_btn,
    search_create_trailer_btn,
    main_trouble_btn,
    yes_main_menu_btns,
    status_trouble_btn
)
from telebot import types
from transform import transform_to_1c
from telebot.apihelper import ApiTelegramException
from constains import (
    TOO_LONG,
    IS_EMPTY
)
import sqlite3

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


# Начало первого блока создания. Поиск или создание прицепа
# =================================================================================================================================================
def new_create_operation_step(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text == 'Найти прицеп':
            msg = bot.send_message(
                chat_id,
                'Введите обозначение прицепа для поиска.',
                reply_markup=main_btn()
            )
            bot.register_next_step_handler(msg, search_operation_step)
        elif user_text == 'Создать прицеп':
            msg = bot.send_message(
                chat_id,
                'Введите обозначение прицепа для создания. \n'
                'Обозначение будет автоматически переведено как в 1С \n'
                'Ожидание ввода...',
                reply_markup=main_btn()
            )
            bot.register_next_step_handler(msg, intermediate_creation_step)
        elif user_text == 'Главное меню':
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                chat_id,
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        elif user_text.isdigit():
            user_dict[chat_id] = Trouble(chat_id)
            trouble = user_dict[chat_id]
            trailer = db.search_trailer(user_text)
            trouble.trailer_id = message.text
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                message.chat.id,
                f'Вы выбрали прицеп: {trailer[0]} \n'
                'Для внесения проблемы выберите соответствующую '
                'кнопку под клавиатурой \n',
                reply_markup=main_trouble_btn()
            )
            bot.register_next_step_handler(msg, create_trouble_step)
        else:
            msg = bot.send_message(
                chat_id,
                'Функция, в которой вы находитесь, ожидает на вход \n'
                'либо порядковый номер прицепа из списка, '
                'либо команду с кнопок под клавиатурой. \n'
                'Воспользуйтесь кнопкой найти чтобы узнать порядковый номер. \n'
                'Выберите действие:',
                reply_markup=search_create_trailer_btn()
                )
            bot.register_next_step_handler(msg, new_create_operation_step)
    except IndexError:
        msg = bot.send_message(
            message.chat.id,
            'Прицепа с таким номером нет в списке \n'
            'Воспользуйтесь кнопками ввода для выбор действия \n'
            'Или введите номер прицепа',
            reply_markup=search_create_trailer_btn()
            )
        bot.register_next_step_handler(msg, new_create_operation_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {new_create_operation_step.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def search_operation_step(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text == 'Главное меню':
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                chat_id,
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        else:
            bot.reply_to(
                message,
                'Начинаю процесс поиска по запросу.'
                )
            designation = user_text
            if len(designation.split('-')) > 2:
                designation = transform_to_1c(message.text)
            list_trailers = db.search_designation_trailer(designation)
            find_trailers = ''
            for trailer in list_trailers:
                srt_trailer = (str(trailer) + ' \n')
                find_trailers += srt_trailer
            bot.send_message(
                chat_id,
                f'{find_trailers}'
            )
            msg = bot.send_message(
                chat_id,
                'Поиск завершен. \n'
                'Для создания записи по прицепу из списка введите '
                'порядковый номер прицепа \n'
                '(из списка: первый параметр в скобках без кавычек - число) \n'
                'Либо повторите поиск или создайте новый прицеп с помощью '
                'кнопок.',
                reply_markup=search_create_trailer_btn()
            )
            bot.register_next_step_handler(msg, new_create_operation_step)
    except ApiTelegramException as err:
        err = err.result_json['description']
        bot.send_message(
            message.chat.id,
            'Ошибка! \n'
            f'Функция: {search_operation_step.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )
        if err == TOO_LONG:
            bot.reply_to(
                message,
                'Длинна ответа на поиск по запросу превысила 4096 символов! \n'
                'Уточните поиск'
            )
        elif err == IS_EMPTY:
            bot.reply_to(
                message,
                'Ничего не найдено \n'
                'Уточните поиск'
            )
        msg = bot.send_message(
            message.chat.id,
            'Уточните поиск или создайте новый прицеп',
            reply_markup=search_create_trailer_btn()
        )
        bot.register_next_step_handler(msg, new_create_operation_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {search_operation_step.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def intermediate_creation_step(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text == 'Главное меню':
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                chat_id,
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        else:
            user_dict[chat_id] = Trailer(chat_id)
            trailer = user_dict[chat_id]
            trailer.designation = transform_to_1c(user_text)
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
    except IndexError:
        bot.send_message(
            message.chat.id,
            'Скорее всего при внесении обозначения прицепа вы '
            'забыли про знак "-" \n'
            'Попробуйте еще раз. \n'
            )
        msg = bot.send_message(
            message.chat.id,
            'Введите обозначение прицепа для создания. \n'
            'Обозначение будет автоматически переведено как в 1С',
        )
        bot.register_next_step_handler(msg, intermediate_creation_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {intermediate_creation_step.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def confirm_intermediate_func(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text == 'Да':
            markup1 = types.ReplyKeyboardRemove(selective=False)
            trailer = user_dict[chat_id]
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
            bot.register_next_step_handler(msg, new_create_operation_step)
        elif user_text == 'Главное меню':
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                chat_id,
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        elif user_text == 'Нет':
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                chat_id,
                'Выберите действие с помощью кнопок под клавиатурой',
                reply_markup=search_create_trailer_btn()
            )
            bot.register_next_step_handler(msg, new_create_operation_step)
    except (
        sqlite3.Error,
        sqlite3.Warning,
        sqlite3.IntegrityError
    ) as err:
        msg = bot.send_message(
            message.chat.id,
            f'{err} \n'
            'Такой прицеп есть в базе данных \n'
            'Уточните поиск или создайте новый прицеп \n',
            reply_markup=search_create_trailer_btn()
        )
        bot.register_next_step_handler(msg, new_create_operation_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {confirm_intermediate_func.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )
# =================================================================================================================================================
# Конец первого блока создания. Прицеп либо создан а потом выбран, либо просто выбран.
# Из первого блока выходит команда на внесение проблемы


# Начало второго блока создания. Создание проблемы. На вход приходит команда на проблему
# =================================================================================================================================================
def create_trouble_step(message):
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
            msg = bot.send_message(
                message.chat.id,
                'Сейчас можно внести проблему по выбранному прицепу \n'
                'Ожидание ввода...',
                reply_markup=main_btn()
            )
            bot.register_next_step_handler(msg, create_trouble_to_database)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {create_trouble_step.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def create_trouble_to_database(message):
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
            trouble = user_dict[chat_id]
            trouble.user_id = chat_id
            trouble.problem = user_text
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
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {create_trouble_to_database.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def confirm_trouble_to_database(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text == 'Да':
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
            else:
                causer = db.search_causer_name(trouble.causer_id)[0]
            bot.send_message(
                chat_id,
                'Запись для внесения в базу данных: \n'
                f'Дата: {trouble.date} \n'
                f'Номер заказа: {trouble.order_num} \n'
                f'Проблема: {trouble.problem} \n'
                f'Документ: {trouble.document} \n'
                f'Статус проблемы: {status} \n'
                f'Прицеп: {trailer[0]} \n'
                f'Виновник: {causer} \n'
                f'Смена: {message.from_user.last_name} \n'
            )
            bot.send_message(
                chat_id,
                'Чтобы дополнить запись выберите соответствующую '
                'кнопку для ввода. \n'
                'Чтобы внести запись в базу данных нажмите "Внести запись" \n',
                reply_markup=create_markup()
            )
            bot.register_next_step_handler(message, write_trouble_to_database)
        elif user_text == 'Нет':
            msg = bot.send_message(
                message.chat.id,
                'Для возврата на шаг "ввод проблемы" \n'
                'Нажмите кнопку "Внести проблему"',
                reply_markup=main_trouble_btn()
            )
            bot.register_next_step_handler(msg, create_trouble_step)
        elif user_text == 'Главное меню':
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(
                chat_id,
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        else:
            bot.reply_to(
                message,
                'Ошибка! \n'
                'Подтвердите ввод проблемы \n'
                'Используйте кнопки под клавиатурой',
                reply_markup=choose_markup()
            )
            bot.register_next_step_handler(message, confirm_trouble_to_database)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {confirm_trouble_to_database.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )
# Конец второго блока создания. Создана проблема и прицеп
# =================================================================================================================================================


# Начало третьего блока создания. Корретировка записи
# =================================================================================================================================================
def write_trouble_to_database(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        trouble = user_dict[chat_id]
        if user_text == 'Внести запись':
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
        elif user_text == 'Номер заказа':
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(
                message.chat.id,
                'Введите номер заказа \n'
                'Ожидание ввода...',
                reply_markup=markup
            )
            bot.register_next_step_handler(message, create_order_num)
        elif user_text == 'Документ (СЗ)':
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(
                message.chat.id,
                'Введите документ(СЗ) \n'
                'Ожидание ввода...',
                reply_markup=markup
            )
            bot.register_next_step_handler(message, create_document)
        elif user_text == 'Статус проблемы':
            bot.send_message(
                message.chat.id,
                'Для выбора статуса проблемы воспользуйтесь кнопками ввода',
                reply_markup=status_trouble_btn()
            )
            bot.register_next_step_handler(message, create_status)
        elif user_text == 'Виновник':
            bot.send_message(
                message.chat.id,
                'Для выбора виновника воспользуйтесь кнопками ввода',
                reply_markup=choose_causer()
            )
            bot.register_next_step_handler(message, create_causer)
        else:
            msg = bot.send_message(
                chat_id,
                'Функция, в которой вы находитесь, ожидает на вход: \n'
                '1. Либо варианты добавления в запись различных полей: '
                'Номер заказа, Документ (СЗ), Статус проблемы, Виновник, '
                'Внести запись. \n'
                '2. Либо внесение записи в базу данных, так же с помощью '
                'соответствующей команды. '
                'Воспользуйтесь кнопками под клавиатурой чтобы выбрать '
                'действие. \n'
                'Выберите действие:',
                reply_markup=create_markup()
                )
            bot.register_next_step_handler(msg, write_trouble_to_database)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {write_trouble_to_database.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def create_order_num(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        trouble = user_dict[chat_id]
        trouble.order_num = user_text
        msg = bot.send_message(
            chat_id,
            f'Номер заказа: {trouble.order_num} \n'
            'Для возврата на этап формирования записи нажмите "Да" '
            'или вернитесь в главное меню.',
            reply_markup=yes_main_menu_btns()
        )
        bot.register_next_step_handler(msg, confirm_trouble_to_database)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {create_order_num.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def create_document(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        trouble = user_dict[chat_id]
        trouble.document = user_text
        msg = bot.send_message(
            chat_id,
            f'Документ: {trouble.document} \n'
            'Для возврата на этап формирования записи нажмите "Да" '
            'или вернитесь в главное меню.',
            reply_markup=yes_main_menu_btns()
        )
        bot.register_next_step_handler(msg, confirm_trouble_to_database)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {create_document.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def create_status(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text == 'Решена' or user_text == 'Требует решения':
            if user_text == 'Решена':
                status = 1
            elif user_text == 'Требует решения':
                status = 0
            trouble = user_dict[chat_id]
            trouble.status = status
            msg = bot.send_message(
                chat_id,
                f'Статус проблемы: {user_text} \n'
                'Для возврата на этап формирования записи нажмите "Да" '
                'или вернитесь в главное меню.',
                reply_markup=yes_main_menu_btns()
            )
            bot.register_next_step_handler(msg, confirm_trouble_to_database)
        else:
            msg = bot.send_message(
                chat_id,
                'Функция, в которой вы находитесь, ожидает на вход '
                'команду с кнопок под клавиатурой \n'
                'Выберите действие:',
                reply_markup=status_trouble_btn()
            )
            bot.register_next_step_handler(msg, create_status)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {create_status.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def create_causer(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        causer_id = db.search_causer_id(user_text)[0]
        trouble = user_dict[chat_id]
        trouble.causer_id = causer_id
        causer = db.search_causer_name(trouble.causer_id)[0]
        msg = bot.send_message(
            chat_id,
            f'Виновник: {causer} \n'
            'Для возврата на этап формирования записи нажмите "Да" '
            'или вернитесь в главное меню.',
            reply_markup=yes_main_menu_btns()
        )
        bot.register_next_step_handler(msg, confirm_trouble_to_database)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {create_causer.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )
# Конец третьего блока.
# =================================================================================================================================================
