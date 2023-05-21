
import os
import pandas as pd
from config import db


def create_user_folder(user_id):
    DIR = f'/home/CHMZAP/CHMZAP_HELPER/send_email/attachments/{user_id}'
    if not os.path.isdir(DIR):
        os.mkdir(DIR)
    return DIR


def create_excel(result, user_folder):
    try:

        # Обработка данных для первого листа эксель
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
            counter = 0
            for value in names_of_columns_db.values():
                x = stroka[counter]
                if stroka[counter] is not None:
                    if counter == 5:
                        if stroka[counter] == 0:
                            x = 'Требует решения'
                        else:
                            x = 'Проблема решена'
                    elif counter == 6:
                        x = db.search_trailer(stroka[counter])[0]
                    elif counter == 7:
                        x = db.search_causer_name(stroka[counter])[0]
                    elif counter == 8:
                        x = db.search_user_last_name(stroka[counter])[0]
                else:
                    x = None
                counter += 1
                value.append(x)

        # Обработка данных для второго листа эксель
        subunit_list = [
            'КО',
            'Производство',
            'Снабжение',
        ]
        count_troubles_list = []
        statistic_data = {
            'Подразделение': subunit_list,
            'Количество ошибок': count_troubles_list
        }
        for subunit in subunit_list:
            count = names_of_columns_db['Виновник'].count(subunit)
            count_troubles_list.append(count)

        sheet_name1 = 'Ошибки'
        sheet_name2 = 'Статистика'

        df_first_sheet = pd.DataFrame(names_of_columns_db)
        df_second_sheet = pd.DataFrame(statistic_data)
        path = f'{user_folder}/send.xlsx'
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df_first_sheet.to_excel(
            writer,
            sheet_name=sheet_name1,
            startrow=1,
            startcol=1,
            header=False,
            index=False
        )
        df_second_sheet.to_excel(
            writer,
            sheet_name=sheet_name2,
            startrow=1,
            startcol=1,
            header=False,
            index=False
        )
        workbook = writer.book
        worksheet1 = writer.sheets[sheet_name1]
        worksheet2 = writer.sheets[sheet_name2]

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
        worksheet1.set_column(1, 1, 20)
        worksheet1.set_column(2, 3, 12)
        worksheet1.set_column(4, 5, 30)
        worksheet1.set_column(6, 6, 20)
        worksheet1.set_column(7, 7, 30)
        worksheet1.set_column(8, 9, 20)

        for col_num, value in enumerate(df_first_sheet.columns.values):
            worksheet1.write(0, col_num + 1, value, header_format)
        for index, row in df_first_sheet.iterrows():
            if len(row[3]) <= 15:
                len_str = 20
            else:
                len_str = len(row[3]) * 0.9
            worksheet1.set_row(index + 1, len_str, cell_format)

        for col_num, value in enumerate(df_second_sheet.columns.values):
            worksheet2.write(0, col_num + 1, value)

        worksheet2.set_column(1, 1, 33)
        worksheet2.set_column(2, 2, 33)

        chart = workbook.add_chart({'type': 'pie'})
        chart.add_series({
            'name':       'Статистика по ошибкам',
            'categories': [sheet_name2, 1, 1, 4, 1],
            'values':     [sheet_name2, 1, 2, 4, 2],
            'data_labels': {'category': True,
                            'position': 'outside_end',
                            'percentage': True},
        })
        chart.set_title({'name': 'Статистика по ошибкам'})
        chart.set_style(10)
        worksheet2.insert_chart('B5', chart)
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
