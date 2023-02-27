
import os
import pandas as pd
# import sys
# For linux
# sys.path.append('..')
# For windows
# sys.path.append('C:/pet_Dev/CHMZAP_HELPER/chmzap_helper')
from config import db


def create_user_folder(user_id):
    DIR = f'send_email/attachments/{user_id}'
    if not os.path.isdir(DIR):
        os.mkdir(DIR)
    return DIR


def create_excel(result, user_folder):
    try:
        names_of_columns = (
            'Номер в базе данных',
            'Дата',
            'Заказ',
            'Проблема',
            'Документ(СЗ)',
            'Статус проблемы',
            'Обозначение прицепа',
            'Виновник',
            'Смена',
        )
        id_list = []
        date_list = []
        order_num_list = []
        problem_list = []
        document_list = []
        status_list = []
        trailer_list = []
        causer_list = []
        user_list = []
        names_of_columns_db = {
            'Номер в базе данных': id_list,
            'Дата': date_list,
            'Заказ': order_num_list,
            'Проблема': problem_list,
            'Документ(СЗ)': document_list,
            'Статус проблемы': status_list,
            'Обозначение прицепа': trailer_list,
            'Виновник': causer_list,
            'Смена': user_list
        }
        for stroka in result:
            id = stroka[0]
            date = stroka[1]
            order_num = stroka[2]
            if order_num is None:
                order_num = None
            problem = stroka[3]
            document = stroka[4]
            if document is None:
                document = None
            status = stroka[5]
            if status is None:
                status = None
            elif status == 0:
                status = 'Требует решения'
            else:
                status = 'Проблема решена'
            trailer_id = stroka[6]
            trailer = db.search_trailer(trailer_id)[0]
            causer_id = stroka[7]
            if causer_id is None:
                causer = None
            else:
                causer = db.search_causer_name(causer_id)[0]
            user_id = stroka[8]
            user = db.search_user_last_name(user_id)[0]

            id_list.append(id)
            date_list.append(date)
            order_num_list.append(order_num)
            problem_list.append(problem)
            document_list.append(document)
            status_list.append(status)
            trailer_list.append(trailer)
            causer_list.append(causer)
            user_list.append(user)
        dict_to_db = {}
        for name in names_of_columns:
            dict_to_db[name] = names_of_columns_db[name]
        df = pd.DataFrame(dict_to_db)
        path = f'{user_folder}/send.xlsx'
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df.to_excel(
            writer,
            sheet_name='Sheet1',
            startrow=1,
            startcol=1,
            header=False,
            index=False
        )
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'fg_color': '#D7E4BC',
            'border': 1
        })
        header_format.set_align('center')
        header_format.set_align('vcenter')
        header_format.set_font_size(14)
        cell_format = workbook.add_format()
        cell_format.set_font_size(12)
        cell_format.set_text_wrap(True)
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        # cell_format.set_shrink(True)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 3, 12)
        worksheet.set_column(4, 5, 30)
        worksheet.set_column(6, 6, 20)
        worksheet.set_column(7, 7, 30)
        worksheet.set_column(8, 9, 20)
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num + 1, value, header_format)
        for index, row in df.iterrows():
            if len(row[3]) <= 15:
                len_str = 20
            else:
                len_str = len(row[3]) * 0.9
            worksheet.set_row(index + 1, len_str, cell_format)
        writer.close()
        return True
    except Exception:
        return False


def delete_excel():
    try:
        for file in os.listdir('send_email/attachments'):
            os.remove(f'send_email/attachments/{file}')
    except Exception as err:
        return f'Ошибка: {err}'
