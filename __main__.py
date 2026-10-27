from os import path
from structure.structure import CreatingStructure

import locale
locale.setlocale(locale.LC_ALL, "")

print(r"""
    ____        __  __                   ______                    
   / __ \__  __/ /_/ /_  ____  ____     / ____/___  _________ ____ 
  / /_/ / / / / __/ __ \/ __ \/ __ \   / /_  / __ \/ ___/ __ `/ _ \
 / ____/ /_/ / /_/ / / / /_/ / / / /  / __/ / /_/ / /  / /_/ /  __/
/_/    \__, /\__/_/ /_/\____/_/ /_/  /_/    \____/_/   \__, /\___/ 
      /____/                                          /____/       
""")

language = {
    "RU": {
        "list": ['1 Создать проект', '2 Сделать копию проекта', '3 Запуск проекта'],
        'input': {
            1: '\nВведите число: ',
            2: '\nВведите директорию: ',
            3: 'Имя: ',
            4: 'разработчик: '
        },
        "error": 'Не верные данные'
        
    },
    "EN": {
        "list": ['1 Create a project', '2 Make a copy of the project', '3 Run the project'],
        'input': {
            1: 'Enter a number: ',
            2: 'Enter a directory: ',
            3: 'Name: ',
            4: 'Developer: '
        },
        "error": 'Incorrect data'
        
    }
}

lan = "RU" if locale.getlocale(locale.LC_MONETARY)[0] == "Russian_Russia" else "EN"

print(*language[lan]["list"], "", sep='\n')

N = int(input(language[lan]["input"][1]))

if not 0 < N <= 3:
    print(language[lan]["error"])
    raise TypeError(language[lan]["error"])

F = input(language[lan]["input"][2])

if not path.exists(F):
    print(language[lan]["error"])
    raise ValueError()

if N == 1:
    CreatingStructure(F, input(language[lan]["input"][3]), input(language[lan]["input"][4]),).start()
    