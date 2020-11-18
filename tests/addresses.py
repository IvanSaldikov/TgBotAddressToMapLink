from addresses import Address, AddressDB
from db import DB

from pytest import approx


class TestAddress():
    """Тестирование работы класса работы с адресами"""

    def setup_class(self):
        """Инициализация тестового класса - начало тестирования"""
        self.db = DB()
        self.conn = self.db.conn
        self.cursor = self.db.cursor
        self.address = Address()

    def test_init(self):
        """Инициализация класса"""
        assert isinstance(self.address, Address)

    def test_add_address_to_db(self):
        """Добавление адреса в базу данных"""
        ret = self.address.add_address('message.text',
                                       'link_to_yamaps',
                                       99999999)
        assert ret is None

    def teardown_class(self):
        """При завершении тестирования"""
        cursor = self.cursor.execute("delete from addresses where address='message.text' "
                                     "and link_to_ya_map='link_to_yamaps'"
                                     "and user_id=99999999")
        cursor.fetchall()
        self.conn.commit()
