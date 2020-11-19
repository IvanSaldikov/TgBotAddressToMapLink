from typing import List, NamedTuple, Optional

from db import DB


from datetime_fmt import get_now_formatted


class AddressDB(NamedTuple):
    """Структура добавленного в БД адреса"""
    id: Optional[int]
    address: str
    link_to_ya_map: str
    user_id: int
    category_name: str
    cat_id: int


class Address():
    """Класс для работы с адресами"""

    def __init__(self):
        self.db = DB()

    def add_address(self, address: str, link_to_ya_map: str, user_id: int, is_shown: int) -> str:
        """Добавляет новый адрес в базу данных.
        Принимает на вход текст сообщения, поступившего на вход в бот"""
        inserted_id = self.db.insert('addresses',
                                     {
                                         "address": address,
                                         "link_to_ya_map": link_to_ya_map,
                                         "created": get_now_formatted(),
                                         "user_id": user_id,
                                         "is_shown": is_shown
                                     }
                                     )
        return inserted_id

    def get_all_addresses(self, user_id, cat_id=None) -> List[AddressDB]:
        """Возвращает список всех адресов, введенных пользователем"""
        added_sql_str = ''
        if cat_id is not None:
            added_sql_str = f' and category_id={cat_id}'

        rows = self.db.conn_new.execute("select id, address, link_to_ya_map, user_id "
                       f"from addresses where `user_id` = '{user_id}'{added_sql_str} "
                       "order by address LIMIT 40")
        addresses = [AddressDB(id=row[0],
                               address=row[1],
                               link_to_ya_map=row[2],
                               user_id=row[3],
                               category_name='',
                               cat_id=-1) for row in rows]
        return addresses

    def delete_address(self, row_id: int) -> None:
        """Удаляет адрес по его идентификатору"""
        self.db.delete("addresses", row_id)

    def get_link_ya_map(self, user_id, row_id):
        """Возвращаем ссылку на Яндекс.Карты"""
        sql_str = ("select id, link_to_ya_map, user_id "
                   f"from addresses where user_id = {int(user_id)} "
                   f"AND id={row_id}")
        result = self.db.conn_new.execute(sql_str)
        link_to_ya_map = "Ссылка не найдена"
        for row in result:
            link_to_ya_map = row if row else link_to_ya_map
        return link_to_ya_map

    def get_name_by_id(self, user_id: int, addr_id: int) -> str:
        """Возвращаем название адреса по его id"""
        sql_str = ("select id, address, user_id "
                   f"from addresses where user_id = {int(user_id)} "
                   f"AND id={int(addr_id)}")
        result = self.db.conn_new.execute(sql_str)
        address_name = "Адрес не найден"
        for row in result:
            address_name = row if row else address_name
        return address_name

    def get_all_addresses_and_cats(self, user_id: int) -> List[AddressDB]:
        """Возвращает список всех адресов, введенных пользователем, с указанием категорий"""
        sql_str = ("select a.id, a.address, a.user_id, c.name, c.id "
                   f"from addresses as a left join categories as c "
                   f"on a.category_id=c.id "
                   f"where a.user_id = '{int(user_id)}' and a.is_shown=1 "
                   "order by a.address LIMIT 40")
        rows = self.db.conn_new.execute(sql_str)
        addresses = [AddressDB(id=row[0],
                               address=row[1],
                               link_to_ya_map='',
                               user_id=row[2],
                               category_name=row[3],
                               cat_id=row[4]) for row in rows]
        return addresses
