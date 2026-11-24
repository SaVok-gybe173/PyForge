import os
import shutil
import py_compile
def mkdir(dir):
    os.mkdir(dir)
    print(f"Папка '{dir}' успешно создана.")

def copin(r, w):
    d = open(r, 'r')
    f = open(w, 'w')
    f.write(d.read())
    f.close()
    d.close()
    print(f"Папка '{w}' успешно создана.")

class CreatingStructure:
    def __init__(self, page: str, name: str = 'MyProject', developer = 'main', main_file = "src", version: str = '0.0.1'):
        self.page = page
        self.developer = developer
        self.dir = os.path.join(self.page, name)
        self.main_file = os.path.join(self.dir, main_file)
        self.name = name
        self.version = version
        self.der = os.path.dirname(os.path.abspath(__file__))


    def start(self):
        if os.path.exists(self.page):
            mkdir(self.dir)
            self.assets = os.path.join(self.dir, "assets")
            mkdir(self.assets)                          # Все ресурсы игры
            mkdir(os.path.join(self.assets, "images"))  # Спрайты, фоны, иконки
            mkdir(os.path.join(self.assets, "sounds"))  # Звуковые эффекты
            mkdir(os.path.join(self.assets, "fonts"))   # Шрифты
            mkdir(os.path.join(self.assets, "music"))   # Фоновая музыка

            mkdir(self.main_file)
            mkdir(os.path.join(self.main_file, "modules")) # Игровые модули

            copin(os.path.join(self.der, 'text', 'Main.py'), os.path.join(self.main_file, 'main.py'))
            copin(os.path.join(self.der, 'text', '__main__.py'), os.path.join(self.dir, 'main.py'))
    
            mkdir(os.path.join(self.dir, 'mods'))   # моды (если подключены)
            mkdir(os.path.join(self.dir, 'data'))   # Игровые данные (уровни, диалоги, конфиги)
            mkdir(os.path.join(self.dir, 'tests'))  # Тесты для вашего кода
            mkdir(os.path.join(self.dir, 'docs'))   # Документация проекта
            shutil.copytree(os.path.dirname(self.der), os.path.join(self.dir, "PyForge"))

        else:
            raise ValueError('Не найдена директория.')

class Compilit:
    def __init__(self, f:str):
        py_compile.compile(f, f.replace('.py', ".pyc"))

        # Или компилируем всю папку
        for root, dirs, files in os.walk('mods'):
            for file in files:
                if file.endswith('.py'):
                    path = os.path.join(root, file)
                    # Компилируем в папку mods_compiled с той же структурой
                    comp_path = os.path.join('mods_compiled', os.path.relpath(path, 'mods') + 'c')
                    os.makedirs(os.path.dirname(comp_path), exist_ok=True)
                    py_compile.compile(path, comp_path)
