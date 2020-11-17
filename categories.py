"""Работа с категориями адресов"""
from typing import Dict, List, NamedTuple

import db
from datetime_fmt import get_now_formatted

class Category(NamedTuple):
    """Структура категории"""
    id: int
    name: str
    user_id: int


class Categories:
    def __init__(self, user_id):
        self._user_id = user_id
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """Возвращает справочник категорий адресов из БД для данного пользователя"""
        cursor = db.get_cursor()
        sql_str = ("select id, name, user_id, created "
                       f"from categories where user_id = {self.get_user_id()} "
                       "order by created desc LIMIT 20")
        cursor.execute(sql_str)
        categories = cursor.fetchall()
        categories_result = []
        for index, category in enumerate(categories):
            categories_result.append(Category(
                id=int(category[0]),
                name=category[1],
                user_id=int(category[2]),
            ))
        return categories_result

    def get_all_categories(self) -> List[Category]:
        """Возвращает справочник категорий."""
        return self._categories

    def get_user_id(self) -> int:
        """Возвращает id текущего пользователя."""
        return self._user_id

    def get_category_name(self, cat_id: int) -> Category:
        """Возвращает отображаемое название категории по id."""
        cursor = db.get_cursor()
        sql_str = ("select id, name, user_id "
                       f"from categories where user_id = {self.get_user_id()} and id={cat_id} ")
        cursor.execute(sql_str)
        row = cursor.fetchone()
        if row[1]:
            cat_name = row[1]
        else:
            cat_name = '*UNKNOWN*'
        return cat_name

    def add_category(self, name: str) -> None:
        db.insert("categories", {
            "user_id": self.get_user_id(),
            "name": name,
            "created": get_now_formatted()
        })
        return

    def delete_category(self, row_id: int) -> None:
        """Удаляет категорию по ее идентификатору"""
        cursor = db.get_cursor()
        sql_str = (f"delete from categories where id={row_id} and user_id={self.get_user_id()}")
        cursor.execute(sql_str)

