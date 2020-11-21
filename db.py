
from typing import Dict
import sqlalchemy as sa
from config import DB_HOST, DB_PASSWORD, DB_NAME, DB_USER, DB_TYPE


class DB:
    """Класс для работы с базой данных"""

    def __init__(self):
        # Подключаемся к базе данных SQLite3 или Postgres
        if DB_TYPE == 0:
            db_conn_str = 'sqlite:///db/addresses.db'
        else:
            db_conn_str = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
        self.conn = sa.create_engine(db_conn_str)
        #self.check_db_exists()

    def insert(self, table: str, column_values: Dict):
        columns = ', '.join(column_values.keys())
        values = [tuple(column_values.values())]
        placeholders = ", ".join("?" * len(column_values.keys()))
        ins = (
            f"INSERT INTO {table} "
            f"({columns}) "
            f"VALUES ({placeholders})"
        )
        return self.conn.execute(ins, values)

    def delete(self, table: str, row_id: int) -> None:
        row_id = int(row_id)
        self.conn.execute(f"delete from {table} where id={row_id}")

    def _init_db(self):
        """Инициализирует БД"""
        if DB_TYPE == 0:
            create_db_file_name = "createtable_sqlite3.sql"
        else:
            create_db_file_name = "createdb_postgresql.sql"
        with open(create_db_file_name, "r") as f:
            sql = f.read()
        self.conn.execute(sql)

    def check_db_exists(self):
        """Проверяет, инициализирована ли БД, если нет — инициализирует"""
        if DB_TYPE == 0:
            sql_str = "SELECT * FROM sqlite_master WHERE type='table' AND name='addresses'"
        else:
            sql_str = ('SELECT table_name FROM information_schema.tables WHERE table_schema='
            'public'
            ' and table_name=\'addresses\';')
        table_exists = self.conn.execute(sql_str)
        for row in table_exists:
            if row:
                return
        self._init_db()
