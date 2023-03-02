
from telebot import types


def main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itempbtn1 = types.KeyboardButton('Создание')
    itempbtn2 = types.KeyboardButton('Чтение')
    itempbtn3 = types.KeyboardButton('Редактирование')
    itempbtn4 = types.KeyboardButton('Удаление')
    markup.add(itempbtn1, itempbtn2, itempbtn3, itempbtn4)
    return markup


def choose_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    itempbtn1 = types.KeyboardButton('Да')
    itempbtn2 = types.KeyboardButton('Нет')
    itempbtn3 = types.KeyboardButton('Главное меню')
    markup.add(itempbtn1, itempbtn2, itempbtn3)
    return markup


def choose_causer():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    itempbtn1 = types.KeyboardButton('КО')
    itempbtn2 = types.KeyboardButton('Производство')
    itempbtn3 = types.KeyboardButton('Снабжение')
    markup.add(itempbtn1, itempbtn2, itempbtn3)
    return markup


def create_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itempbtn1 = types.KeyboardButton('Номер заказа')
    itempbtn2 = types.KeyboardButton('Документ (СЗ)')
    itempbtn3 = types.KeyboardButton('Статус проблемы')
    itempbtn4 = types.KeyboardButton('Виновник')
    itempbtn5 = types.KeyboardButton('Внести запись')
    markup.add(itempbtn1, itempbtn2, itempbtn3, itempbtn4, itempbtn5)
    return markup


def main_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itempbtn1 = types.KeyboardButton('Главное меню')
    markup.add(itempbtn1)
    return markup


def search_create_trailer_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itempbtn1 = types.KeyboardButton('Найти прицеп')
    itempbtn2 = types.KeyboardButton('Создать прицеп')
    itempbtn3 = types.KeyboardButton('Главное меню')
    markup.add(itempbtn1, itempbtn2, itempbtn3)
    return markup


def main_trouble_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itempbtn1 = types.KeyboardButton('Внести проблему')
    itempbtn2 = types.KeyboardButton('Главное меню')
    markup.add(itempbtn1, itempbtn2)
    return markup


def yes_main_menu_btns():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    itempbtn1 = types.KeyboardButton('Да')
    itempbtn2 = types.KeyboardButton('Главное меню')
    markup.add(itempbtn1, itempbtn2)
    return markup


def status_trouble_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itempbtn1 = types.KeyboardButton('Решена')
    itempbtn2 = types.KeyboardButton('Требует решения')
    markup.add(itempbtn1, itempbtn2)
    return markup


def email_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itempbtn1 = types.KeyboardButton('Внести адрес почты')
    markup.add(itempbtn1)
    return markup


def read_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    itempbtn1 = types.KeyboardButton('Выбрать прицеп')
    itempbtn2 = types.KeyboardButton('Выбрать отчет')
    itempbtn3 = types.KeyboardButton('Главное меню')
    markup.add(itempbtn1, itempbtn2, itempbtn3)
    return markup


def main_search_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    itempbtn1 = types.KeyboardButton('Главное меню')
    itempbtn2 = types.KeyboardButton('Повторить поиск')
    markup.add(itempbtn1, itempbtn2)
    return markup


def trailer_report():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itempbtn1 = types.KeyboardButton('Все ошибки')
    itempbtn2 = types.KeyboardButton('Главное меню')
    markup.add(itempbtn1, itempbtn2)
    return markup


def abort_trailer_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    itempbtn1 = types.KeyboardButton('Выбрать прицеп')
    itempbtn2 = types.KeyboardButton('Главное меню')
    markup.add(itempbtn1, itempbtn2)
    return markup


def update_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itempbtn1 = types.KeyboardButton('Дата')
    itempbtn2 = types.KeyboardButton('Номер заказа')
    itempbtn3 = types.KeyboardButton('Проблема')
    itempbtn4 = types.KeyboardButton('Документ (СЗ)')
    itempbtn5 = types.KeyboardButton('Статус проблемы')
    itempbtn6 = types.KeyboardButton('Прицеп')
    itempbtn7 = types.KeyboardButton('Виновник')
    itempbtn8 = types.KeyboardButton('Применить изменения')
    markup.add(itempbtn1, itempbtn2, itempbtn3, itempbtn4,
               itempbtn5, itempbtn6, itempbtn7, itempbtn8,)
    return markup
