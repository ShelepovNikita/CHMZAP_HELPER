
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_main_markup():
    '''Отображение кнопок после ввода ключа доступа.'''
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Чтение", callback_data="/read"),
        InlineKeyboardButton("Запись", callback_data="/write")
        )
    return markup


def gen_edit_markup():
    '''Отображение кнопок после нажатия кнопки запись.'''
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Редактировать запись", callback_data="/edit"),
        InlineKeyboardButton("Удалить запись", callback_data="/delete")
        )
    return markup
