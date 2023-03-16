
import sqlite3


class Database:
    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file, check_same_thread=False)
        self.cur = self.con.cursor()

    def create_tables(self):
        # causers = [(1, 'КО'), (2, 'Производство'), (3, 'Снабжение')]
        with self.con:
            self.cur.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                external_id INTEGER,
                first_name TEXT,
                last_name TEXT,
                work_email TEXT);
            CREATE TABLE IF NOT EXISTS trailers (
                id INTEGER PRIMARY KEY,
                designation TEXT UNIQUE);
            CREATE TABLE IF NOT EXISTS causers (
                id INTEGER PRIMARY KEY,
                name TEXT);
            CREATE TABLE IF NOT EXISTS troubles (
                id INTEGER PRIMARY KEY,
                date TEXT,
                order_num TEXT,
                problem TEXT,
                document TEXT,
                status INTEGER,
                trailer_id INTEGER NOT NULL,
                causer_id INTEGER,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(trailer_id) REFERENCES trailers(id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(causer_id) REFERENCES causers(id));
            ''')
            # self.cur.executemany(
            #     'INSERT INTO causers VALUES(?, ?);',
            #     (causers))

    # Создание пользователя
    def create_user(self, data):
        with self.con:
            self.cur.execute('''
                INSERT INTO users(
                    external_id,
                    first_name,
                    last_name)
                VALUES(?, ?, ?);''', (data))

    # Поиск пользователя
    def check_user(self, user_id):
        with self.con:
            result = self.cur.execute(
                'SELECT * FROM users WHERE external_id = ?;',
                (user_id,)).fetchall()
        return bool(len(result))

    # Поиск почты
    def check_email(self, user_id):
        with self.con:
            result = self.cur.execute(
                'SELECT work_email FROM users WHERE external_id = ?;',
                (user_id,)).fetchall()[0]
        return result[0]

    # Создание почты
    def create_email(self, email, user_id):
        with self.con:
            self.cur.execute(
                'UPDATE users SET work_email=? WHERE external_id=?',
                (email, user_id))

    # Список прицепов
    def read_trailers(self):
        with self.con:
            list_trailers = self.cur.execute(
                'SELECT id, designation FROM trailers'
                ).fetchall()
        return list_trailers

    # Поиск прицепа по id
    def search_trailer(self, id):
        with self.con:
            select_trailer = self.cur.execute(
                'SELECT designation FROM trailers WHERE id = ?;',
                (id,)).fetchall()
        return select_trailer[0]

    # Поиск прицепа по designation
    def search_trailer_designation(self, designation):
        with self.con:
            select_trailer = self.cur.execute(
                'SELECT id FROM trailers WHERE designation = ?;',
                (designation,)).fetchall()
        return select_trailer[0]

    # Поиск виновника id
    def search_causer_id(self, name):
        with self.con:
            causer_id = self.cur.execute(
                'SELECT id FROM causers WHERE name = ?;',
                (name,)).fetchall()
        return causer_id[0]

    # Поиск виновника name
    def search_causer_name(self, id):
        with self.con:
            causer_name = self.cur.execute(
                'SELECT name FROM causers WHERE id = ?;',
                (id,)).fetchall()
        return causer_name[0]

    # Поиск пользователя
    def search_user(self, external_id):
        with self.con:
            result = self.cur.execute(
                'SELECT id FROM users WHERE external_id = ?;',
                (external_id,)).fetchall()
        return result[0]

    # Создание записи в таблице проблем
    def create_trouble(self, create_list):
        with self.con:
            self.cur.execute('''
                INSERT INTO troubles(
                    date,
                    order_num,
                    problem,
                    document,
                    status,
                    trailer_id,
                    causer_id,
                    user_id)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?);''', (create_list))

    # Создание записи в таблице прицепов
    def create_trailer(self, designation):
        with self.con:
            self.cur.execute(
                'INSERT INTO trailers(designation) VALUES(?)',
                (designation,))

    def search_designation_trailer(self, designation):
        designation = ('%' + designation + '%')
        with self.con:
            result = self.cur.execute('''
                SELECT
                    id,
                    designation
                FROM trailers
                WHERE designation LIKE ?;''', (designation,)).fetchall()
        return result

# Функции для скрпита парсинга таблиц экселя
# ===================================================================================
    def script_trailer_id(self, designation):
        with self.con:
            result = self.cur.execute(
                'SELECT * FROM trailers WHERE designation = ?;',
                (designation,)).fetchall()
        return result[0]

    def script_causer_id(self, name):
        with self.con:
            result = self.cur.execute(
                'SELECT * FROM causers WHERE name = ?;',
                (name,)).fetchall()
        if result == []:
            result = ' '
        else:
            result = result[0]
        return result

    def script_user_external_id(self, last_name):
        with self.con:
            result = self.cur.execute('''
                SELECT
                    external_id,
                    last_name
                FROM users
                WHERE last_name = ?;''', (last_name,)).fetchall()
        return result[0]
# ===================================================================================

    def search_by_trailer_in_troubles(self, id):
        with self.con:
            result = self.cur.execute(
                'SELECT * FROM troubles WHERE trailer_id = ? ORDER BY date;',
                (id,)).fetchall()
        return result

    # Поиск пользователя, фамилия
    def search_user_last_name(self, external_id):
        with self.con:
            result = self.cur.execute(
                'SELECT last_name FROM users WHERE external_id = ?;',
                (external_id,)).fetchall()
        return result[0]

    def search_user_first_name(self, external_id):
        with self.con:
            result = self.cur.execute(
                'SELECT first_name FROM users WHERE external_id = ?;',
                (external_id,)).fetchall()
        return result[0]

    # Поиск по дате
    def search_by_date_in_troubles(self, date):
        date = ('%' + date + '%')
        with self.con:
            result = self.cur.execute(
                'SELECT * FROM troubles WHERE date LIKE ? ORDER BY date;',
                (date,)).fetchall()
        return result

    # Поиск по периоду
    def search_by_period_in_troubles(self, start_date, end_date):
        # date = ('%' + date + '%')
        with self.con:
            result = self.cur.execute('''
                SELECT
                    *
                FROM troubles
                WHERE date >= ? AND date <= ?
                ORDER BY date;''', (start_date, end_date,)).fetchall()
        return result

    # Количество записей
    def count_troubles(self):
        with self.con:
            result = self.cur.execute(
                'SELECT COUNT(*) FROM troubles;').fetchall()
        return result[0]

    # Макс дата
    def min_date(self):
        with self.con:
            result = self.cur.execute(
                'SELECT MIN(date) FROM troubles;').fetchall()
        return result[0]

    # Мин дата
    def max_date(self):
        with self.con:
            result = self.cur.execute(
                'SELECT MAX(date) FROM troubles;').fetchall()
        return result[0]

    # Поиск по id записи
    def search_by_id_in_troubles(self, id):
        with self.con:
            result = self.cur.execute(
                'SELECT * FROM troubles WHERE id = ?;',
                (id,)).fetchall()
        return result[0]

    # Поиск пользователя, фамилия
    def search_user_emal(self, external_id):
        with self.con:
            result = self.cur.execute(
                'SELECT work_email FROM users WHERE external_id = ?;',
                (external_id,)).fetchall()
        return result[0]

    # Редактирование записи
    def update_trouble(self, update_list, id):
        with self.con:
            self.cur.execute('''
                UPDATE troubles
                SET date = ?,
                    order_num = ?,
                    problem = ?,
                    document = ?,
                    status = ?,
                    trailer_id = ?,
                    causer_id = ?,
                    user_id = ?
                WHERE id = ?;''', (*update_list, id))
        return True

    # Удаление записи
    def delete_trouble(self, id):
        with self.con:
            self.cur.execute(
                'DELETE FROM troubles WHERE id=?;',
                (id,))
        return True
