### Тестирование

О тестировании программ тут:

https://edu-support.mephi.ru/materials/190/edu/03/lecture.md?to=html

https://habr.com/ru/post/269759/

Для установки модуля тестирования PyTest:

`pip install pytest`

Для тестирования запускаем команду:

`python -B -m pytest -v -s -p 
 no:cacheprovider tests/addresses.py`

`-s` - показывать всю историю вызова функций

`-v` - показывать ход выполнения тестов

