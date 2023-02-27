
from config import bot
from markups import (
    search_create_trailer_btn,
    read_markup
    )
from branches.create_branch import create_operation
from branches.read_branch import read_operation


def main_operation_step(message):
    try:
        chat_id = message.chat.id
        if message.text == 'Создание':
            bot.send_message(
                chat_id,
                'Вы выбрали создание записи \n'
                'Для поиска прицепа в базе данных '
                'выберите кнопку "Найти". \n'
                'Для создания нового прицепа '
                'выберите кнопку "Создать". \n'
                'Если вам уже известен порядковый номер прицепа из базы то '
                'сейчас самое время его ввести.'
            )
            msg = bot.send_message(
                chat_id,
                'Выберите действие или введите порядковый номер прицепа:',
                reply_markup=search_create_trailer_btn()
            )
            bot.register_next_step_handler(msg, create_operation)
        elif message.text == 'Чтение':
            msg = bot.send_message(
                chat_id,
                'Вы выбрали чтение записей из базы данных. \n'
                'Для поиска проблем по конкретному прицепу '
                'выберите прицеп. \n'
                'Для формирования отчета за период выберите отчет. \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=read_markup()
            )
            bot.register_next_step_handler(msg, read_operation)
        elif message.text == 'Редактирование':
            # user_dict[chat_id] = User(message.chat.id)
            bot.send_message(
                chat_id,
                'Вы выбрали редактирование записей в базе данных. \n'
                'Раздел в разработке.'
                '/start'
            )
            # Место для следующего шага по редактированию записей.
        elif message.text == 'Удаление':
            # user_dict[chat_id] = User(message.chat.id)
            bot.send_message(
                chat_id,
                'Вы выбрали удаление записей из базы данных. \n'
                'Раздел в разработке.'
                '/start'
            )
            # Место для следующего шага по удалению записей.
        else:
            bot.send_message(
                message.chat.id,
                'Для работы с ботом пользуйтесь кнопками под строкой ввода \n'
                'Если после ввода комманды /start кнопки не появились \n'
                'Используйте команду повторно'
                )
    except Exception:
        bot.reply_to(
            message,
            f'Функция: {main_operation_step.__name__} \n'
            f'{Exception} \n'
            f'Главное меню - /start'
            )
