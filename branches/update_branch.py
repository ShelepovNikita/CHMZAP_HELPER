
from config import bot, db, group_id
from markups import (
    choose_markup,
    main_btn,
    update_markup,
    yes_main_menu_btns,
    status_trouble_btn,
    choose_causer
)
from telebot import types

user_dict = {}


class Trouble:
    def __init__(self, column):
        self.column = column
        self.id = None
        self.date = None
        self.order_num = None
        self.problem = None
        self.document = None
        self.status = None
        self.trailer_id = None
        self.causer_id = None
        self.user_id = None


def update_operation(message):
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
        elif user_text.isdigit():
            trouble_db = db.search_by_id_in_troubles(user_text)
            user_dict[chat_id] = Trouble(chat_id)
            trouble = user_dict[chat_id]
            trouble.id = trouble_db[0]
            trouble.date = trouble_db[1]
            trouble.order_num = trouble_db[2]
            trouble.problem = trouble_db[3]
            trouble.document = trouble_db[4]
            trouble.status = trouble_db[5]
            trouble.trailer_id = trouble_db[6]
            trouble.causer_id = trouble_db[7]
            trouble.user_id = trouble_db[8]

            if trouble.status is None:
                status = None
            elif trouble.status == 0:
                status = 'Требует решения'
            else:
                status = 'Проблема решена'

            trailer = db.search_trailer(trouble.trailer_id)

            if trouble.causer_id is None:
                causer = None
            else:
                causer = db.search_causer_name(trouble_db[7])[0]
            trouble_user = db.search_user_last_name(trouble_db[8])[0]
            msg = bot.send_message(
                chat_id,
                'Вы выбрали запись: \n'
                f'id: {trouble.id} \n'
                f'Дата: {trouble.date} \n'
                f'Номер заказа: {trouble.order_num} \n'
                f'Проблема: {trouble.problem} \n'
                f'Документ: {trouble.document} \n'
                f'Статус проблемы: {status} \n'
                f'Прицеп: {trailer[0]} \n'
                f'Виновник: {causer} \n'
                f'Смена: {trouble_user} \n'
                '\n'
                'Редактируем эту запись? \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=choose_markup()
            )
            bot.register_next_step_handler(msg, confirm_update_step)
        else:
            msg = bot.send_message(
                chat_id,
                'Функция, в которой вы находитесь, ожидает на вход '
                'уникальный идентификатор - номер записи в базе данных, '
                'который можно получить из первой колонки отчета на почте. \n'
                'Введите номер записи. \n'
                '\n'
                '<i>Ожидание ввода...</i>',
                parse_mode='HTML',
                reply_markup=main_btn()
                )
            bot.register_next_step_handler(msg, update_operation)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {update_operation.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def confirm_update_step(message):
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
        elif user_text == 'Нет':
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(
                chat_id,
                'Уточните номер записи из отчета для редактирования '
                'и возвращайтесь \n'
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        elif user_text == 'Да':
            trouble = user_dict[chat_id]
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
            trailer = db.search_trailer(trouble.trailer_id)
            msg = bot.send_message(
                chat_id,
                'Выберите раздел для редактирования '
                f'записи {trouble.id}: \n'
                f'Дата: {trouble.date} \n'
                f'Номер заказа: {trouble.order_num} \n'
                f'Проблема: {trouble.problem} \n'
                f'Документ: {trouble.document} \n'
                f'Статус проблемы: {status} \n'
                f'Прицеп: {trailer[0]} \n'
                f'Виновник: {causer} \n'
                f'Смена: {message.from_user.last_name} \n'
                'Или выберите "Применить изменения" для подтверждения.'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=update_markup()
            )
            bot.register_next_step_handler(msg, update_trouble_to_database)
        else:
            msg = bot.send_message(
                chat_id,
                'Функция, в которой вы находитесь, ожидает на вход '
                'подтверждение редактирования записи \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=choose_markup()
            )
            bot.register_next_step_handler(msg, confirm_update_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {confirm_update_step.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def update_trouble_to_database(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text == 'Применить изменения':
            trouble = user_dict[chat_id]
            update_list = (
                trouble.date,
                trouble.order_num,
                trouble.problem,
                trouble.document,
                trouble.status,
                trouble.trailer_id,
                trouble.causer_id,
                trouble.user_id,
            )
            id = trouble.id
            if db.update_trouble(update_list, id):
                markup = types.ReplyKeyboardRemove(selective=False)
                bot.send_message(
                    chat_id,
                    'Запись успешно отредактирована \n'
                    'Для возврата в главное меню используйте команду - /start',
                    reply_markup=markup
                    )
                trailer = db.search_trailer(trouble.trailer_id)
                if trouble.status is None:
                    status = None
                elif trouble.status == 0:
                    status = 'Требует решения'
                else:
                    status = 'Проблема решена'
                count = db.count_troubles()[0]
                bot.send_message(
                    group_id,
                    f'<b>Пользователь {message.from_user.last_name} '
                    'отредактировал запись!</b> \n'
                    f'Прицеп: {trailer[0]} \n'
                    f'Проблема: {trouble.problem} \n'
                    f'Статус проблемы: {status} \n'
                    f'Общее количество записей в базе данных: {count}',
                    parse_mode='HTML',
                )
        elif user_text == 'Дата':
            trouble = user_dict[chat_id]
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                message.chat.id,
                'Введите новую дату в формате ГГГГ-ММ-ДД \n'
                '\n'
                '<i>Ожидание ввода...</i>',
                parse_mode='HTML',
                reply_markup=markup
            )
            bot.register_next_step_handler(msg, update_date)
        elif user_text == 'Номер заказа':
            trouble = user_dict[chat_id]
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                message.chat.id,
                'Введите новый номер заказа \n'
                '\n'
                '<i>Ожидание ввода...</i>',
                parse_mode='HTML',
                reply_markup=markup
            )
            bot.register_next_step_handler(msg, update_order_num)
        elif user_text == 'Проблема':
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                message.chat.id,
                'Введите новую проблему \n'
                '\n'
                '<i>Ожидание ввода...</i>',
                parse_mode='HTML',
                reply_markup=markup
            )
            bot.register_next_step_handler(msg, update_problem)
        elif user_text == 'Документ (СЗ)':
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                message.chat.id,
                'Введите новый документ(СЗ) \n'
                '\n'
                '<i>Ожидание ввода...</i>',
                parse_mode='HTML',
                reply_markup=markup
            )
            bot.register_next_step_handler(msg, update_document)
        elif user_text == 'Статус проблемы':
            msg = bot.send_message(
                message.chat.id,
                'Для изменения статуса проблемы воспользуйтесь '
                'кнопками ввода \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=status_trouble_btn()
            )
            bot.register_next_step_handler(msg, update_status)
        elif user_text == 'Прицеп':
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                message.chat.id,
                'Для изменения прицепа введите новый порядковый '
                'номер прицепа из базы данных \n'
                '\n'
                '<i>Ожидание ввода...</i>',
                parse_mode='HTML',
                reply_markup=markup
            )
            bot.register_next_step_handler(msg, update_trailer)
        elif user_text == 'Виновник':
            msg = bot.send_message(
                message.chat.id,
                'Для смены виновника воспользуйтесь кнопками ввода \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=choose_causer()
            )
            bot.register_next_step_handler(msg, update_causer)
        else:
            msg = bot.send_message(
                chat_id,
                'Функция, в которой вы находитесь, ожидает на вход: \n'
                '1. Либо варианты обновления в записи различных полей \n'
                '2. Либо обновление записи в базе данных, так же с помощью '
                'соответствующей команды. \n'
                'Воспользуйтесь кнопками под клавиатурой чтобы выбрать '
                'действие. \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=update_markup()
            )
            bot.register_next_step_handler(msg, update_trouble_to_database)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {update_trouble_to_database.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def update_date(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        trouble = user_dict[chat_id]
        trouble.date = user_text
        msg = bot.send_message(
            chat_id,
            f'Новая дата: {trouble.date} \n'
            'Для возврата на этап формирования записи нажмите "Да" '
            'или вернитесь в главное меню. \n'
            '\n'
            '<i>Выберите действие:</i>',
            parse_mode='HTML',
            reply_markup=yes_main_menu_btns()
        )
        bot.register_next_step_handler(msg, confirm_update_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {update_date.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def update_order_num(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        trouble = user_dict[chat_id]
        trouble.order_num = user_text
        msg = bot.send_message(
            chat_id,
            f'Новый номер заказа: {trouble.order_num} \n'
            'Для возврата на этап формирования записи нажмите "Да" '
            'или вернитесь в главное меню. \n'
            '\n'
            '<i>Выберите действие:</i>',
            parse_mode='HTML',
            reply_markup=yes_main_menu_btns()
        )
        bot.register_next_step_handler(msg, confirm_update_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {update_order_num.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def update_problem(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        trouble = user_dict[chat_id]
        trouble.problem = user_text
        msg = bot.send_message(
            chat_id,
            f'Новая проблема: {trouble.problem} \n'
            'Для возврата на этап формирования записи нажмите "Да" '
            'или вернитесь в главное меню. \n'
            '\n'
            '<i>Выберите действие:</i>',
            parse_mode='HTML',
            reply_markup=yes_main_menu_btns()
        )
        bot.register_next_step_handler(msg, confirm_update_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {update_problem.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def update_document(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        trouble = user_dict[chat_id]
        trouble.document = user_text
        msg = bot.send_message(
            chat_id,
            f'Новый документ: {trouble.document} \n'
            'Для возврата на этап формирования записи нажмите "Да" '
            'или вернитесь в главное меню. \n'
            '\n'
            '<i>Выберите действие:</i>',
            parse_mode='HTML',
            reply_markup=yes_main_menu_btns()
        )
        bot.register_next_step_handler(msg, confirm_update_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {update_document.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def update_status(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text in ('Решена', 'Требует решения'):
            if user_text == 'Решена':
                status = 1
            elif user_text == 'Требует решения':
                status = 0
            trouble = user_dict[chat_id]
            trouble.status = status
            msg = bot.send_message(
                chat_id,
                f'Новый статус проблемы: {user_text} \n'
                'Для возврата на этап формирования записи нажмите "Да" '
                'или вернитесь в главное меню. \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=yes_main_menu_btns()
            )
            bot.register_next_step_handler(msg, confirm_update_step)
        else:
            msg = bot.send_message(
                chat_id,
                'Функция, в которой вы находитесь, ожидает на вход '
                'команду с кнопок под клавиатурой \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=status_trouble_btn()
            )
            bot.register_next_step_handler(msg, update_status)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {update_status.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def update_trailer(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text.isdigit():
            trailer = db.search_trailer(user_text)
            trouble = user_dict[chat_id]
            trouble.trailer_id = user_text
            msg = bot.send_message(
                chat_id,
                f'Новый прицеп: {trailer[0]} \n'
                'Для возврата на этап формирования записи нажмите "Да" '
                'или вернитесь в главное меню. \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=yes_main_menu_btns()
            )
            bot.register_next_step_handler(msg, confirm_update_step)
        else:
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                chat_id,
                'Функция ожидает на вход порядковый номер прицепа из базы \n'
                '\n'
                '<i>Ожидание ввода...</i>',
                parse_mode='HTML',
                reply_markup=markup
            )
            bot.register_next_step_handler(message, update_trailer)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {update_trailer.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def update_causer(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text in ('КО', 'Производство', 'Снабжение'):
            causer_id = db.search_causer_id(user_text)[0]
            trouble = user_dict[chat_id]
            trouble.causer_id = causer_id
            causer = db.search_causer_name(trouble.causer_id)[0]
            msg = bot.send_message(
                chat_id,
                f'Виновник: {causer} \n'
                'Для возврата на этап формирования записи нажмите "Да" '
                'или вернитесь в главное меню. \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=yes_main_menu_btns()
            )
            bot.register_next_step_handler(msg, confirm_update_step)
        else:
            msg = bot.send_message(
                chat_id,
                'Функция, в которой вы находитесь, ожидает на вход '
                'команду с кнопок под клавиатурой \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=choose_causer()
            )
            bot.register_next_step_handler(msg, update_causer)
    except IndexError:
        msg = bot.send_message(
            message.chat.id,
            'Ошибка ввода \n'
            'Воспользуйтесь кнопками ввода для выбор действия \n'
            '\n'
            '<i>Выберите действие:</i>',
            parse_mode='HTML',
            reply_markup=choose_causer()
            )
        bot.register_next_step_handler(msg, update_causer)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {update_causer.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )
