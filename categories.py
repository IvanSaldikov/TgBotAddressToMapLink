"""Работа с категориями адресов"""
from typing import Dict, List, NamedTuple

import db


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
        #print(sql_str)
        cursor.execute(sql_str)
        categories = cursor.fetchall()
        categories_result = []
        #print(categories)
        for index, category in enumerate(categories):
            print(category)
            print(type(category))
            print('categories',categories)
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

    def get_category(self, category_id: str) -> Category:
        """Возвращает категорию по id."""
        finded = None
        return finded

    def delete_category(self, row_id: int) -> None:
        """Удаляет категорию по ее идентификатору"""
        cursor = db.get_cursor()
        sql_str = (f"delete from categories where id={row_id} and user_id={self.get_user_id()}")
        cursor.execute(sql_str)

