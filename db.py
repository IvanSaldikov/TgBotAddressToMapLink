import os
from typing import Dict, List, Tuple
import sqlalchemy as sa

import sqlite3


class DB:
    """Класс для работы с базой данных"""

    def __init__(self):
        #self.conn = sqlite3.connect(os.path.join("db", "addresses.db"))
        self.conn_new = sa.create_engine('sqlite:///db/addresses.db')
        #self.cursor = self.conn.cursor()
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
        with open("createdb.sql", "r") as f:
            sql = f.read()
        self.conn_new.execute(sql)

    def check_db_exists(self):
        """Проверяет, инициализирована ли БД, если нет — инициализирует"""
        table_exists = self.conn_new.execute("SELECT name FROM sqlite_master "
                       "WHERE type='table' AND name='addresses'")
        for row in table_exists:
            if row:
                return
        self._init_db()
