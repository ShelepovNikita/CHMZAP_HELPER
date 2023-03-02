
from config import bot, db, group_id
from markups import (
    choose_markup,
    main_btn,
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


def delete_operation(message):
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

            if trouble.status == 0:
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
                'Удаляем эту запись? \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=choose_markup()
            )
            bot.register_next_step_handler(msg, confirm_delete_step)
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
            bot.register_next_step_handler(msg, delete_operation)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {delete_operation.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def confirm_delete_step(message):
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
                'Уточните номер записи из отчета для удаления '
                'и возвращайтесь \n'
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        elif user_text == 'Да':
            markup = types.ReplyKeyboardRemove(selective=False)
            trouble = user_dict[chat_id]
            if db.delete_trouble(trouble.id):
                bot.send_message(
                    chat_id,
                    'Запись успешно удалена \n'
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
                'удалил запись!</b> \n'
                f'Прицеп: {trailer[0]} \n'
                f'Проблема: {trouble.problem} \n'
                f'Статус проблемы: {status} \n'
                f'Общее количество записей в базе данных: {count}',
                parse_mode='HTML',
            )
        else:
            msg = bot.send_message(
                chat_id,
                'Функция, в которой вы находитесь, ожидает на вход '
                'подтверждение удаления записи \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=choose_markup()
            )
            bot.register_next_step_handler(msg, confirm_delete_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {confirm_delete_step.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )
