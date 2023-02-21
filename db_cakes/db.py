import logging
import sqlite3

from db_cakes.data_for_db import cakes, types


class DB_BakeryProducts:
    """Создает базу данных,
    загружает данные в базу,
    позволяет получать данные из базы.
    """

    conn = sqlite3.connect('db/bakery_products.db')
    cur = conn.cursor()

    def create_table(self):
        """Создает базу данных"""
        self.cur.executescript('''
        CREATE TABLE IF NOT EXISTS types(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
         );
        CREATE TABLE IF NOT EXISTS cakes(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            path_photo TEXT NOT NULL,
            type_id INTEGER NOT NULL,
            FOREIGN KEY (type_id) REFERENCES types(id)
        );
        ''')

    def add_data(self, name_table, data):
        """Загружает данные в базу."""

        elm = '?, ' * (len(data[0]) - 1)
        self.cur.executemany(f'INSERT OR IGNORE INTO {name_table} VALUES({elm}?);', data)

    def get_cake_descr_path(self, name_cake):
        """Позволяет получить описание и путь до картинки по названию пирога."""

        try:
            get_position = ''f'SELECT description, path_photo FROM cakes WHERE name = "{name_cake}"'''
            res = self.cur.execute(get_position)
            row = res.fetchone()
            return row
        except TypeError:
            logging.info(f'Пирогов {name_cake} нет в базе ')

    def save_close(self):
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    db = DB_BakeryProducts()
    db.create_table()
    db.add_data('types', types)
    db.add_data('cakes', cakes)
    db.save_close()


