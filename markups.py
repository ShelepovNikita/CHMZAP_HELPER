
from telebot import types


#Главное меню
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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itempbtn1 = types.KeyboardButton('Да')
    itempbtn2 = types.KeyboardButton('Нет')
    markup.add(itempbtn1, itempbtn2)
    return markup
