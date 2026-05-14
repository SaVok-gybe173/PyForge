from pyfiglet import Figlet
from rich.console import Console
from termcolor import cprint
from os import path
try:
    from .structure.structure import InvalidPageError, CreatingStructure
except ImportError:
    from structure.structure import InvalidPageError, CreatingStructure

import locale
locale.setlocale(locale.LC_ALL, "")

language = {
    "RU": {
        "list": ['1 Создать проект', '2 Сделать копию проекта', '3 Запуск проекта'],
        'input': {
            1: '\nВведите число: ',
            2: '\nВведите дирикторию: ',
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

console = Console()
flr = Figlet(font='slant')  # Более стильный шрифт
ascii_art = flr.renderText("Python Forge!")
console.print(ascii_art, style="bold blue")

flt = Figlet(font='standard')

print(*language[lan]["list"], "", sep='\n')

N = int(input(language[lan]["input"][1]))

if not 0 < N <= 3:
    cprint(language[lan]["error"], 'red')
    raise TypeError(language[lan]["error"])

F = input(language[lan]["input"][2])

if not path.exists(F):
    cprint(language[lan]["error"], 'red')
    raise InvalidPageError()

if N == 1:
    CreatingStructure(F, input(language[lan]["input"][3]), input(language[lan]["input"][4]),).start()
    