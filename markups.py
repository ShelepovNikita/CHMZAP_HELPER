
from telebot import types


# Главное меню
def main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itempbtn1 = types.KeyboardButton('Создание')
    itempbtn2 = types.KeyboardButton('Чтение')
    itempbtn3 = types.KeyboardButton('Редактирование')
    itempbtn4 = types.KeyboardButton('Удаление')
    markup.add(itempbtn1, itempbtn2, itempbtn3, itempbtn4)
    return markup


# Есть ли прицеп в списке?
def choose_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    itempbtn1 = types.KeyboardButton('Да')
    itempbtn2 = types.KeyboardButton('Нет')
    itempbtn3 = types.KeyboardButton('Главное меню')
    markup.add(itempbtn1, itempbtn2, itempbtn3)
    return markup


# Выбор виновника
def choose_causer():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    itempbtn1 = types.KeyboardButton('КО')
    itempbtn2 = types.KeyboardButton('Производство')
    itempbtn3 = types.KeyboardButton('Снабжение')
    itempbtn4 = types.KeyboardButton('Шаг назад')
    markup.add(itempbtn1, itempbtn2, itempbtn3, itempbtn4)
    return markup


# Создание записи
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
