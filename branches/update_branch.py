
from config import bot, db
from markups import (
    choose_markup,
    main_btn
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
            
            if trouble.status == 0:
                status = 'Требует решения'
            else:
                status = 'Проблема решена'
                
            trailer = db.search_trailer(trouble.trailer_id)
            
            if trouble.trailer_id is None:
                causer = None
            else:
                causer = db.search_causer_name(trouble_db[7])[0]
            trouble_user = db.search_user_last_name(trouble_db[8])[0]
            bot.send_message(
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


# def confirm_update_step(message):
#     try:
#         chat_id = message.chat.id
#         user_text = message.text
#         if user_text == 'Главное меню':
#             markup = types.ReplyKeyboardRemove(selective=False)
#             bot.send_message(
#                 chat_id,
#                 'Для возврата в главное меню используйте команду - /start',
#                 reply_markup=markup
#             )
#         elif user_text == 'Нет':
#             markup = types.ReplyKeyboardRemove(selective=False)
#             bot.send_message(
#                 chat_id,
#                 'Уточните номер записи из отчета для редактирования '
#                 'и возвращайтесь \n'
#                 'Для возврата в главное меню используйте команду - /start',
#                 reply_markup=markup
#             )
#         elif user_text == 'Да':
            
#             bot.send_message(
#                 chat_id,
#                 'Уточните номер записи из отчета для редактирования '
#                 'и возвращайтесь \n'
#                 'Для возврата в главное меню используйте команду - /start',
#                 reply_markup=markup
#             )