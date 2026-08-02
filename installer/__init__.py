# pip install python-msilib
from .yandex_downloads import install as yandex_install
from .arh import unzip_archive
from .shortcut import create_and_move_shortcut
from .server import *
import msilib

"""
msilib.FCICreate(cabname, files): Создавала CAB-файл с указанными файлами, используя алгоритм сжатия MSZIP.

msilib.UuidCreate(): Генерировала новый уникальный идентификатор (UUID), необходимый для идентификации продуктов, компонентов и т.д..

msilib.OpenDatabase(path, persist): Открывала или создавала базу данных MSI.

msilib.CreateRecord(count): Создавала запись (объект Record) для добавления данных в таблицы базы MSI.

msilib.init_database(name, schema, ProductName, ProductCode, ProductVersion, Manufacturer): Создавала и инициализировала новую базу данных MSI с базовой схемой и основными свойствами продукта

"""

class Installer:
    def __init__(self, UrlOrServer: str|tuple[str, int]):
        pass