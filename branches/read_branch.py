
from config import bot, db
import send_email as se
import with_excel as we
from markups import (
    main_btn,
    main_search_btn,
    read_markup,
    trailer_report,
    abort_trailer_search
)
from telebot import types
from constains import (
    TOO_LONG,
    IS_EMPTY
)
from designation_functions import transform_to_1c
from telebot.apihelper import ApiTelegramException

user_dict = {}


class Trouble:
    def __init__(self, column):
        self.column = column
        self.trailer_id = None


def read_operation(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if db.check_email(chat_id) is None:
            msg = bot.send_message(
                chat_id,
                'Мне нужно знать куда направлять отчет \n'
                'Для дальнейшей работы введите адрес '
                'рабочей электронной почты. \n'
                '\n'
                '<i>Ожидание ввода...</i>',
                parse_mode='HTML',
                reply_markup=main_btn()
            )
            bot.register_next_step_handler(msg, email_operation_to_db)
        else:
            if user_text == 'Выбрать прицеп':
                msg = bot.send_message(
                    chat_id,
                    'Введите обозначение прицепа для поиска. \n'
                    '\n'
                    '<i>Ожидание ввода...</i>',
                    parse_mode='HTML',
                    reply_markup=main_btn()
                )
                bot.register_next_step_handler(msg, search_operation_step)
            elif user_text == 'Выбрать отчет':
                min_date = db.min_date()
                max_date = db.max_date()
                msg = bot.send_message(
                    chat_id,
                    'Отчет формируется по дате возникновения проблемы \n'
                    'Дату нужно вводить в формате ГГГГ-ММ-ДД, '
                    'соответственно такой запрос вернет отчет '
                    'за конкретный день, а запрос ГГГГ-ММ вернет '
                    'отчет за конкретный месяц в году. \n'
                    'Для обработки пользовательского запроса '
                    'необходимо указать период через двоеточие, '
                    'например 2022-05:2022-06 вернет '
                    'отчет за май-июнь 2022 года. \n'
                    'За какой период сформировать отчет ? \n'
                    '<tg-spoiler><b>Доступный период: '
                    f'{min_date[0]}:{max_date[0]}</b></tg-spoiler> \n'
                    '\n'
                    '<i>Ожидание ввода...</i>',
                    parse_mode='HTML',
                    reply_markup=main_btn()
                )
                bot.register_next_step_handler(msg, send_excel_date_operation)
            elif user_text == 'Главное меню':
                markup = types.ReplyKeyboardRemove(selective=False)
                msg = bot.send_message(
                    chat_id,
                    'Для возврата в главное меню используйте команду - /start',
                    reply_markup=markup
                )
            else:
                msg = bot.send_message(
                    chat_id,
                    'Функция, в которой вы находитесь, ожидает на вход '
                    'команду с кнопок под клавиатурой. \n'
                    '\n'
                    '<i>Выберите действие:</i>',
                    parse_mode='HTML',
                    reply_markup=read_markup()
                )
                bot.register_next_step_handler(msg, read_operation)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {read_operation.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def email_operation_to_db(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text == 'Главное меню':
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                chat_id,
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        else:
            chat_id = message.chat.id
            user_text = message.text
            if '@' in user_text:
                mail = user_text.strip()
                db.create_email(mail, chat_id)
                msg = bot.send_message(
                    chat_id,
                    'Адрес электронной почты успешно внесен в базу данных ! \n'
                    f'Ваш адрес: {mail} \n'
                    'Для продолжения работы в ветке чтения выберите действие:',
                    reply_markup=read_markup()
                )
                bot.register_next_step_handler(msg, read_operation)
            else:
                msg = bot.send_message(
                    chat_id,
                    'Введите адрес электронной почты! \n'
                    '\n'
                    '<i>Ожидание ввода...</i>',
                    parse_mode='HTML',
                    reply_markup=main_btn()
                )
                bot.register_next_step_handler(msg, email_operation_to_db)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {email_operation_to_db.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def search_operation_step(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text == 'Главное меню':
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(
                chat_id,
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        else:
            bot.reply_to(
                message,
                'Начинаю процесс поиска по запросу.'
                )
            designation = user_text
            if len(designation.split('-')) >= 2:
                designation = transform_to_1c(message.text)
            list_trailers = db.search_designation_trailer(designation)
            find_trailers = ''
            for trailer in list_trailers:
                srt_trailer = (str(trailer) + ' \n')
                find_trailers += srt_trailer
            bot.send_message(
                chat_id,
                f'{find_trailers}'
            )
            msg = bot.send_message(
                chat_id,
                'Поиск завершен. \n'
                'Для создания запроса в базу данных введите '
                'порядковый номер прицепа \n'
                '<i>(из списка: первый параметр в '
                'скобках без кавычек - число)</i> \n'
                'Либо повторите поиск \n'
                '\n'
                '<i>Ожидание ввода или действия...</i>',
                parse_mode='HTML',
                reply_markup=main_search_btn()
            )
            bot.register_next_step_handler(msg, search_operation_next_step)
    except ApiTelegramException as err:
        err = err.result_json['description']
        if err == TOO_LONG:
            bot.reply_to(
                message,
                'Длинна ответа на поиск по запросу превысила 4096 символов! \n'
            )
        elif err == IS_EMPTY:
            bot.reply_to(
                message,
                'Ничего не найдено'
            )
        msg = bot.send_message(
            message.chat.id,
            'Уточните поиск \n'
            '\n'
            '<i>Ожидание ввода...</i>',
            parse_mode='HTML',
            reply_markup=main_btn()
        )
        bot.register_next_step_handler(msg, search_operation_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {search_operation_step.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def search_operation_next_step(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text.isdigit():
            user_dict[chat_id] = Trouble(chat_id)
            trouble = user_dict[chat_id]
            try:
                trailer = db.search_trailer(user_text)
                trouble.trailer_id = user_text
                msg = bot.send_message(
                    message.chat.id,
                    'Поиск ошибок по прицепу \n'
                    f'Вы выбрали прицеп: {trailer[0]} \n'
                    'Бот находится в разработке, '
                    'список функций будет пополняться... \n'
                    '\n'
                    '<i>Выберите действие:</i>',
                    parse_mode='HTML',
                    reply_markup=trailer_report()
                )
                bot.register_next_step_handler(
                    msg,
                    send_excel_trailer_operation
                )
            except IndexError:
                msg = bot.send_message(
                    message.chat.id,
                    'Прицепа с таким номером нет в базе \n'
                    'Для повторного поиска нажмите "Повторить поиск"'
                    'или введите порядковый номер из списка \n'
                    '\n'
                    '<i>Ожидание ввода или действия...</i>',
                    parse_mode='HTML',
                    reply_markup=main_search_btn()
                )
                bot.register_next_step_handler(msg, search_operation_next_step)
            except Exception as err:
                bot.reply_to(
                    message,
                    'Ошибка! \n'
                    f'Функция: {search_operation_step.__name__} \n'
                    f'{err} \n'
                    'Вернитесь в главное меню - /start'
                    )
        elif user_text == 'Повторить поиск':
            msg = bot.send_message(
                message.chat.id,
                'Для повторного поиска нажмите "Выбрать прицеп" \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=abort_trailer_search()
            )
            bot.register_next_step_handler(msg, read_operation)
        elif user_text == 'Главное меню':
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(
                chat_id,
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        else:
            msg = bot.send_message(
                chat_id,
                'Функция, в которой вы находитесь, ожидает на вход '
                'порядковый номер прицепа из списка \n'
                '\n'
                '<i>Ожидание ввода...</i>',
                parse_mode='HTML',
                reply_markup=main_btn()
            )
            bot.register_next_step_handler(msg, search_operation_next_step)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {search_operation_next_step.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def send_excel_trailer_operation(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        if user_text == 'Все ошибки':
            trouble = user_dict[chat_id]
            trailer = db.search_trailer(trouble.trailer_id)
            output_str = f'{user_text} {trailer[0]}'
            bot.send_message(
                chat_id,
                'Формирую запрос: \n'
                f'{output_str}\n'
                'Ожидайте сообщения об успешной отправке отчета'
            )
            folder = we.create_user_folder(chat_id)
            troubles = db.search_by_trailer_in_troubles(
                trouble.trailer_id
            )
            if we.create_excel(troubles, folder):
                mail = db.check_email(chat_id)
                if se.send_email_from_db(mail, folder, output_str):
                    markup = types.ReplyKeyboardRemove(selective=False)
                    bot.send_message(
                        chat_id,
                        'Сформирован запрос к базе данных \n'
                        'Проверьте почту \n'
                        'Для возврата в главное меню используйте '
                        'команду - /start',
                        reply_markup=markup
                    )
                else:
                    bot.send_message(
                        chat_id,
                        'Произошла ошибка \n'
                        'Отчет не отправлен \n'
                        'Попробуйте еще раз',
                        reply_markup=main_btn()
                    )
            else:
                bot.send_message(
                    chat_id,
                    'Произошла ошибка \n'
                    'Проблемы на стороне сервера, не создается отчет \n'
                    'Попробуйте еще раз',
                    reply_markup=main_btn()
                )
        elif user_text == 'Главное меню':
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(
                chat_id,
                'Для возврата в главное меню используйте команду - /start',
                reply_markup=markup
            )
        else:
            msg = bot.send_message(
                chat_id,
                'Функция, в которой вы находитесь, ожидает на вход '
                'команду с кнопок под клавиатурой. \n'
                '\n'
                '<i>Выберите действие:</i>',
                parse_mode='HTML',
                reply_markup=trailer_report()
            )
            bot.register_next_step_handler(msg, send_excel_trailer_operation)
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {send_excel_trailer_operation.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )


def send_excel_date_operation(message):
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
        else:
            flag = False
            output_str = f'Отчет по дате {user_text}'
            bot.send_message(
                chat_id,
                'Формирую запрос: \n'
                f'{output_str}\n'
                'Ожидайте сообщения об успешной отправке отчета'
            )
            for sign in user_text:
                if sign == ':':
                    flag = True
            if flag:
                period = user_text.split(':')
                period_troubles = db.search_by_period_in_troubles(
                    period[0],
                    period[1]
                )
            else:
                period_troubles = db.search_by_date_in_troubles(user_text)
            folder = we.create_user_folder(chat_id)
            if we.create_excel(period_troubles, folder):
                mail = db.check_email(chat_id)
                if se.send_email_from_db(mail, folder, output_str):
                    markup = types.ReplyKeyboardRemove(selective=False)
                    bot.send_message(
                        chat_id,
                        'Сформирован запрос к базе данных \n'
                        'Проверьте почту \n'
                        'Для возврата в главное меню используйте '
                        'команду - /start',
                        reply_markup=markup
                    )
                else:
                    markup = types.ReplyKeyboardRemove(selective=False)
                    bot.send_message(
                        chat_id,
                        'Произошла ошибка \n'
                        'Отчет не отправлен \n'
                        'Вернитесь в главное меню - /start',
                        reply_markup=markup
                    )
            else:
                markup = types.ReplyKeyboardRemove(selective=False)
                bot.send_message(
                    chat_id,
                    'Произошла ошибка \n'
                    'Проблемы на стороне сервера, не создается отчет \n'
                    'Вернитесь в главное меню - /start',
                    reply_markup=markup
                )
    except Exception as err:
        bot.reply_to(
            message,
            'Ошибка! \n'
            f'Функция: {send_excel_date_operation.__name__} \n'
            f'{err} \n'
            'Вернитесь в главное меню - /start'
            )
