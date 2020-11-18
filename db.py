import os
from typing import Dict, List, Tuple

import sqlite3


class DB:
    """Класс для работы с базой данных"""

    def __init__(self):
        self.conn = sqlite3.connect(os.path.join("db", "addresses.db"))
        self.cursor = self.conn.cursor()

    def insert(self, table: str, column_values: Dict):
        cursor = self.cursor
        columns = ', '.join(column_values.keys())
        values = [tuple(column_values.values())]
        placeholders = ", ".join("?" * len(column_values.keys()))
        cursor.executemany(
            f"INSERT INTO {table} "
            f"({columns}) "
            f"VALUES ({placeholders})",
            values)
        return self.conn.commit()

    def fetchall(self, table: str, columns: List[str]) -> List[Tuple]:
        columns_joined = ", ".join(columns)
        cursor = self.cursor
        cursor.execute(f"SELECT {columns_joined} FROM {table} LIMIT 100")
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result

    def delete(self, table: str, row_id: int) -> None:
        row_id = int(row_id)
        cursor = self.cursor
        cursor.execute(f"delete from {table} where id={row_id}")
        self.conn.commit()

    def get_cursor(self):
        return self.cursor

    def _init_db(self):
        """Инициализирует БД"""
        cursor = self.cursor
        with open("createdb.sql", "r") as f:
            sql = f.read()
        cursor.executescript(sql)
        self.conn.commit()

    def check_db_exists(self):
        """Проверяет, инициализирована ли БД, если нет — инициализирует"""
        cursor = self.cursor
        cursor.execute("SELECT name FROM sqlite_master "
                       "WHERE type='table' AND name='addresses'")
        table_exists = cursor.fetchall()
        if table_exists:
            return
        self._init_db()
