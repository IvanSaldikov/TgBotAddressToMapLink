import datetime
import re
from typing import List, NamedTuple, Optional

import pytz

import db
import exceptions

from categories import Category


class Address(NamedTuple):
    """Структура добавленного в БД адреса"""
    id: Optional[int]
    address: str
    link_to_ya_map: str
    user_id: int


def add_address(address: str, link_to_ya_map: str, user_id: int) -> str:
    """Добавляет новый адрес в базу данных.
    Принимает на вход текст сообщения, поступившего на вход в бот"""
    """
    inserted_user_id = db.insert('users',
                    {
                        "id": user_id,
                        "created": _get_now_formatted(),
                        "last_updated": _get_now_formatted(),
                    }
               )
    """

    inserted_id = db.insert('addresses',
                    {
                        "address": address,
                        "link_to_ya_map": link_to_ya_map,
                        "created": _get_now_formatted(),
                        "user_id": user_id
                    }
               )
    return inserted_id


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def get_all_addresses(user_id) -> List[Address]:
    """Возвращает список всех адресов, введенных пользователем"""
    cursor = db.get_cursor()
    cursor.execute("select id, address, link_to_ya_map, user_id "
                   f"from addresses where user_id = {user_id} "
                   "order by created desc LIMIT 40")
    rows = cursor.fetchall()
    addresses = [Address(id=row[0], address=row[1], link_to_ya_map=row[2], user_id=row[3]) for row in rows]
    return addresses


def delete_address(row_id: int) -> None:
    """Удаляет адрес по его идентификатору"""
    db.delete("addresses", row_id)


def get_link_ya_map(user_id, row_id):
    """Возвращаем ссылку на Яндекс.Карты"""
    cursor = db.get_cursor()
    sql_str = ("select id, link_to_ya_map, user_id "
                   f"from addresses where user_id = {int(user_id)} "
                   f"AND id={row_id}")
    cursor.execute(sql_str)
    result = cursor.fetchone()
    if not result[1]:
        return "Ссылка не найдена"
    link_to_ya_map = result[1] if result[1] else 0
    return link_to_ya_map


