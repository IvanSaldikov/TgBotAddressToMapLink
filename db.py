
from typing import Dict
import sqlalchemy as sa


class DB:
    """Класс для работы с базой данных"""

    def __init__(self, is_sqlite3=False):
        if is_sqlite3:
            db_conn_str = 'sqlite:///db/addresses.db'
        else:
            db_conn_str = 'postgresql+psycopg2://postgres:postgres@localhost/postgres'
        self.conn_new = sa.create_engine(db_conn_str)
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
        return self.conn_new.execute(ins, values)

    def delete(self, table: str, row_id: int) -> None:
        row_id = int(row_id)
        self.conn_new.execute(f"delete from {table} where id={row_id}")

    def _init_db(self):
        """Инициализирует БД"""
        with open("createdb_postgresql.sql", "r") as f:
            sql = f.read()
        self.conn_new.execute(sql)

    def check_db_exists(self):
        """Проверяет, инициализирована ли БД, если нет — инициализирует"""
        sql_str = "SELECT * FROM sqlite_master WHERE type='table' AND name='addresses'"
        sql_str = ('SELECT table_name FROM information_schema.tables WHERE table_schema='
        'public'
        ' and table_name=\'addresses\';')
        table_exists = self.conn_new.execute(sql_str)
        for row in table_exists:
            if row:
                return
        self._init_db()
