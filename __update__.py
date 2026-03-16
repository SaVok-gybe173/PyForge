import os
import json
from ast import literal_eval
try:
    from .installer import yandex_install, unzip_archive
    from .installer.yandex_downloads import get_file
except ImportError:
    from installer import yandex_install, unzip_archive
    from installer.yandex_downloads import get_file
file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(file)
info: dict = literal_eval(get_file("https://disk.yandex.ru/d/_5EQGnBOjbDOmQ").decode())
wersion = list(info["versions"].keys())
for i, v in enumerate(wersion):
    print(i+1, v)
v = int(input("введи индекс версии которую ты хочешь скачать: "))
print(f"начинаю установку {wersion[v-1]}")

if input("продолжить? \'Y\\n\' ").lower() in "yes":
    p = True
else:
    p = False

if wersion:
    try:
        
        yandex_install(info['versions'][wersion[v-1]['url']], f"{file}\\downloaded_{wersion[v-1]}.zip")
        unzip_archive(f"{file}\\downloaded_{wersion[v-1]}.zip", file)
    except Exception as e:
        print("Ошибка:", e)
    input("Загрузка завершиа, нажми enter что бы продолжить ...")