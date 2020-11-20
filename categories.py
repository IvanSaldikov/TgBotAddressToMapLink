"""Работа с категориями адресов"""
from typing import Dict, List, NamedTuple, Union

from db import DB
from datetime_fmt import get_now_formatted


class CategoryDB(NamedTuple):
    """Структура категории"""
    id: int
    name: str
    user_id: int
    addr_counter: Union[int, None]


class Category():
    """Класс для работы с категориями"""

    def __init__(self, user_id):
        self.db = DB()
        self._user_id = user_id
        self._categories = self._load_categories()

    def _load_categories(self) -> List[CategoryDB]:
        """Возвращает справочник категорий адресов из БД для данного пользователя
         с указанием количества адресов в данной категории"""
        db = self.db
        sql_str = (f"select c.id, c.name, c.user_id, coalesce(adr_cnt.cnt, 0) as cnt "
                   f"from categories as c "
                   f"left join ("
                   f"SELECT a.category_id, COUNT(*) as cnt "
                   f"FROM addresses as a "
                   f"GROUP BY category_id"
                   f") as adr_cnt on c.id=category_id "
                   f"where c.user_id = {self.get_user_id()} "
                   f"order by c.name asc LIMIT 20")
        categories = db.conn.execute(sql_str)
        categories_result = []
        for index, category in enumerate(categories):
            categories_result.append(CategoryDB(
                id=int(category[0]),
                name=category[1],
                user_id=int(category[2]),
                addr_counter=category[3],
            ))
        return categories_result

    def get_all_categories(self) -> List[CategoryDB]:
        """Возвращает справочник категорий."""
        return self._categories

    def get_user_id(self) -> int:
        """Возвращает id текущего пользователя."""
        return self._user_id

    def get_category_name(self, cat_id: int) -> CategoryDB:
        """Возвращает отображаемое название категории по id."""
        sql_str = ("select id, name, user_id "
                   f"from categories where user_id = {self.get_user_id()} and id={cat_id} ")
        rows = self.db.conn.execute(sql_str)
        cat_name = '*UNKNOWN*'
        for row in rows:
            if row:
                cat_name = row[1]
        return cat_name

    def add_category(self, name: str) -> None:
        self.db.insert("categories", {
            "user_id": self.get_user_id(),
            "name": name,
            "created": get_now_formatted()
        })
        return

    def change_category_address(self, address_id, cat_id: int) -> None:
        """Меняем категорию у адреса"""
        sql_str = (f"update addresses set category_id={cat_id} where user_id={self.get_user_id()} and id={address_id}")
        self.db.conn.execute(sql_str)

    def delete_category(self, row_id: int) -> None:
        """Удаляет категорию по ее идентификатору"""
        sql_str = (f"delete from categories where id={row_id} and user_id={self.get_user_id()}")
        self.db.conn.execute(sql_str)

    def get_cat_addr_stat(self, cat_id: int) -> int:
        """Сколько адресов содержится в категории"""
        sql_str = (f"select count(*) from addresses as a where category_id={cat_id} and user_id={self.get_user_id()}")
        rows = self.db.conn.execute(sql_str)
        cat_counter = 0
        for row in rows:
            if row[0]:
                cat_counter = int(row[0])
        return cat_counter
