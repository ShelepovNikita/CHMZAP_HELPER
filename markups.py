
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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itempbtn1 = types.KeyboardButton('1')
    itempbtn2 = types.KeyboardButton('2')
    itempbtn3 = types.KeyboardButton('3')
    itempbtn4 = types.KeyboardButton('Шаг назад')
    markup.add(itempbtn1, itempbtn2, itempbtn3, itempbtn4)
    return markup


# Кнопка Нет
def no_btn():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itempbtn1 = types.KeyboardButton('Нет')
    markup.add(itempbtn1)
    return markup


# Шаг назад
def step_back():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itempbtn1 = types.KeyboardButton('Шаг назад')
    markup.add(itempbtn1)
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
