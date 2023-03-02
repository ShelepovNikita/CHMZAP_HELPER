
import pandas
import sqlite3
import os
# import sys
# For linux
# sys.path.append('..')
# For windows
# sys.path.append('C:/pet_Dev/CHMZAP_HELPER')
from transform import transform_to_1c
from config import db


# Добавление прицепов из списка.
def add_trailers_in_db(list_trailers_xlsx):
    try:
        xl = pandas.ExcelFile(list_trailers_xlsx)
        sheet_name = xl.sheet_names[0]
        excel_data_df = pandas.read_excel(
            list_trailers_xlsx,
            sheet_name=sheet_name
        )
        column_name = excel_data_df.columns.ravel()[0]
        list_trailers = excel_data_df[column_name].tolist()
        for trailer in list_trailers:
            x = transform_to_1c(trailer)
            try:
                db.create_trailer(x)
            except (sqlite3.Error, sqlite3.Warning) as err:
                print(f"Trailer {x} dublicate!", err)
        print('Done!')
    except Exception as err:
        print(err)


# Добавление проблем из таблиц в новый excel файл
def create_excel_troubles(file_with_truobles_xlsx):
    try:
        xl = pandas.ExcelFile(f'for_excel_files/{file_with_truobles_xlsx}')
        sheet_names = xl.sheet_names
        right_sheet_names = [
            'Январь',
            'Февраль',
            'Март',
            'Апрель',
            'Май',
            'Июнь',
            'Июль',
            'Август',
            'Сентябрь',
            'Октябрь',
            'Ноябрь',
            'Декабрь',
        ]
        sheet_names_filter = []
        for sheet in sheet_names:
            if sheet in right_sheet_names:
                sheet_names_filter.append(sheet)
        for she in sheet_names_filter:
            excel_data_df = pandas.read_excel(
                f'for_excel_files/{file_with_truobles_xlsx}',
                sheet_name=she,
            )
            list_data = excel_data_df['Дата'].tolist()
            list_orders = excel_data_df['Номер заказа'].tolist()
            list_troubles = excel_data_df['Проблема'].tolist()
            list_document = excel_data_df['Решение (СЗ)'].tolist()
            list_status = excel_data_df['Уведомление об ошибке ИЦ'].tolist()
            list_trailers = excel_data_df['Обозначение'].tolist()
            list_causers = excel_data_df['Виновник'].tolist()
            list_users = excel_data_df['Смена'].tolist()

            list_data_filter = []
            for data in list_data[1:]:
                if data == 'None':
                    data = ' '
                else:
                    data = (str(data)[:10])
                list_data_filter.append(data)

            list_orders_filter = []
            for order in list_orders[1:]:
                if order == 'None':
                    order = ' '
                else:
                    order = str(order)
                list_orders_filter.append(order)

            list_troubles_filter = []
            for trouble in list_troubles[1:]:
                if trouble == 'None':
                    trouble = ' '
                else:
                    trouble = str(trouble)
                list_troubles_filter.append(trouble)

            list_documents_filter = []
            for document in list_document[1:]:
                if document == 'None':
                    document = ' '
                else:
                    document = str(document)
                list_documents_filter.append(document)

            list_status_filter = []
            for status in list_status[1:]:
                if status == 'None':
                    status = ' '
                else:
                    status = str(status)
                list_status_filter.append(status)
            # for i in range(len(list_status_filter)):
            #     list_status_filter[i] = list_status_filter[i]

            list_trailers_filter = []
            for trailer in list_trailers[1:]:
                trailer = transform_to_1c(trailer)
                list_trailers_filter.append(trailer)
            for i in range(len(list_trailers_filter)):
                list_trailers_filter[i] = db.script_trailer_id(
                    list_trailers_filter[i])[0]

            list_causers = list_causers[1:]
            for i in range(len(list_causers)):
                if list_causers[i] == 'None':
                    list_causers[i] = ' '
                else:
                    list_causers[i] = db.script_causer_id(list_causers[i])[0]

            list_users = list_users[1:]
            for i in range(len(list_users)):
                list_users[i] = db.script_user_external_id(list_users[i])[0]

            create = pandas.DataFrame({'date': list_data_filter,
                                       'order_num': list_orders_filter,
                                       'problem': list_troubles_filter,
                                       'document': list_documents_filter,
                                       'status': list_status_filter,
                                       'trailer_id': list_trailers_filter,
                                       'causer_id': list_causers,
                                       'user_id': list_users,
                                       })
            # create = create.dropna()
            # create['status'] = create['status'].astype(int)
            name = she + ' ' + file_with_truobles_xlsx
            create.to_excel(f'for_excel_files/complete/{name}',
                            sheet_name=she,
                            index=False
                            )
    except Exception as err:
        print(err)


# Добавление в базу данных проблем из созданных excel файлов
def add_troubles_in_db():
    try:
        file_list = os.listdir('for_excel_files/complete')
        for month_troubles_xlsx in file_list:
            excel_data_df = pandas.read_excel(
                f'for_excel_files/complete/{month_troubles_xlsx}',
            )
            spisok_strok = []
            for stroka in excel_data_df.iloc:
                list_stroka = list(stroka)
                for _ in range(len(list_stroka)):
                    intermediate_stroka = []
                    date = str(list_stroka[0])
                    intermediate_stroka.append(date)
                    if list_stroka[1] is None or list_stroka[1] == ' ' or list_stroka[1] == '':
                        order_num = None
                    else:
                        order_num = str(list_stroka[1])
                    intermediate_stroka.append(order_num)
                    problem = list_stroka[2]
                    intermediate_stroka.append(problem)
                    if list_stroka[3] is None or list_stroka[3] == ' ' or list_stroka[3] == '':
                        document = None
                    else:
                        document = str(list_stroka[3])
                    intermediate_stroka.append(document)
                    if list_stroka[4] is None or list_stroka[4] == ' ' or list_stroka[4] == '':
                        status = None
                    else:
                        status = int(list_stroka[4])
                    intermediate_stroka.append(status)
                    trailer_id = int(list_stroka[5])
                    intermediate_stroka.append(trailer_id)
                    if list_stroka[6] is None or list_stroka[6] == ' ' or list_stroka[6] == '':
                        causer_id = None
                    else:
                        causer_id = int(list_stroka[6])
                    intermediate_stroka.append(causer_id)
                    user_id = int(list_stroka[7])
                    intermediate_stroka.append(user_id)
                spisok_strok.append(intermediate_stroka)
            for str_of_table in spisok_strok:
                db.create_trouble(str_of_table)
    except Exception as err:
        print(err)


# add_trailers_in_db('C:/pet_Dev/CHMZAP_HELPER/for_excel_files/Список прицепов мой.xlsx')
# create_excel_troubles('Прицепы, ошибки и статистика 2023.xlsx')
# add_troubles_in_db()
