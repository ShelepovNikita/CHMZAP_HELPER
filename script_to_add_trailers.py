
import pandas
from transform import transform_to_1c
from config import db
import sqlite3

excel_data_df = pandas.read_excel('Список прицепов.xlsx', sheet_name='sheet1')

list_trailers = excel_data_df['trailers'].tolist()

for trailer in list_trailers:
    x = transform_to_1c(trailer)
    try:
        db.create_trailer(x)
    except (sqlite3.Error, sqlite3.Warning) as err:
        print(f"Trailer {x} dublicate!", err)
