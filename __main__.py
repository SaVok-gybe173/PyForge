from pyfiglet import Figlet
from rich.console import Console
from termcolor import cprint
from os import path
try:
    from .creating_a_structure.structure import InvalidPageError, CreatingStructure

except ImportError:
    from creating_a_structure.structure import InvalidPageError, CreatingStructure

console = Console()
flr = Figlet(font='slant')  # Более стильный шрифт
ascii_art = flr.renderText("Python Forge!")
console.print(ascii_art, style="bold blue")

flt = Figlet(font='standard')

print('1 Создать проект', '2 Сделать копию проекта', '3 Запуск проекта', "", sep='\n')

N = int(input('\nВведите число:'))

if not 0 < N <= 3:
    cprint('Не верные данные', 'red')
    raise TypeError('Не верные данные')

F = input('\nВведите дирикторию:')

if not path.exists(F):
    cprint('Не верные данные', 'red')
    raise InvalidPageError()

if N == 1:
    CreatingStructure(F, input('Имя: '), input('разработчик: '),).start()
    