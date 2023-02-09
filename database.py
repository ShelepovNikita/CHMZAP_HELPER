
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
                last_name TEXT);
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
                causer_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(trailer_id) REFERENCES trailers(id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(causer_id) REFERENCES causers(id));
            ''')
            # self.cur.executemany(
            #     'INSERT INTO causers VALUES(?, ?);',
            #     (causers))

    # Создание пользователя
    def create_user(self, user_id, first_name, last_name):
        data = (user_id, first_name, last_name)
        with self.con:
            self.cur.execute(
                'INSERT INTO users(external_id, first_name, last_name) VALUES(?, ?, ?);',
                (*data,))

    # Поиск пользователя
    def check_user(self, user_id):
        with self.con:
            result = self.cur.execute(
                'SELECT * FROM users WHERE external_id = ?;',
                (user_id,)).fetchall()
        return bool(len(result))

    # Список прицепов
    def read_trailers(self):
        with self.con:
            list_trailers = self.cur.execute('SELECT id, designation FROM trailers').fetchall()
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

    # Список виновников
    def read_causers(self):
        with self.con:
            list_causers = self.cur.execute('SELECT id, name FROM causers').fetchall()
        return list_causers

    # Поиск виновника
    def search_causer(self, id):
        with self.con:
            select_causer = self.cur.execute(
                'SELECT name FROM causers WHERE id = ?;',
                (id,)).fetchall()
        return select_causer[0]

    # Поиск пользователя
    def search_user(self, external_id):
        with self.con:
            result = self.cur.execute(
                'SELECT id FROM users WHERE external_id = ?;',
                (external_id,)).fetchall()
        return result[0]

    # Создание записи в таблице проблем
    def create_trouble(self, list_to_push):
        with self.con:
            self.cur.execute(
                'INSERT INTO troubles(date, order_num, problem, document, status, trailer_id, causer_id, user_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?);',
                (*list_to_push,))

    # Создание записи в таблице прицепов
    def create_trailer(self, designation):
        with self.con:
            self.cur.execute(
                'INSERT INTO trailers(designation) VALUES(?)',
                (designation,))
