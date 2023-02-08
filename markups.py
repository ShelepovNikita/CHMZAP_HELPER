
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_main_markup():
    '''Отображение кнопок после ввода ключа доступа.'''
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton('Создание', callback_data='/create'),
        InlineKeyboardButton('Чтение', callback_data='/read'),
        InlineKeyboardButton('Редактирование', callback_data='/update'),
        InlineKeyboardButton('Удаление', callback_data='/delete')
        )
    return markup


def answer_markup():
    '''Выбор прицепа или создание нового.'''
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Да", callback_data="/yes"),
        InlineKeyboardButton("Нет", callback_data="/no")
        )
    return markup
