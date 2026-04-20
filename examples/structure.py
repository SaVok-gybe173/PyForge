import os
import shutil
import py_compile

try:
    from .errors import InvalidPageError
except ImportError:
    from errors import InvalidPageError

def mkdir(diricrori):
    os.mkdir(diricrori)
    print(f"Папка '{diricrori}' успешно создана.")

def copin(r, w):
    d = open(r, 'r')
    f = open(w, 'w')
    f.write(d.read())
    f.close()
    d.close()
    print(f"Папка '{w}' успешно создана.")

class CreatingStructure:
    def __init__(self, page: str, name: str = 'MyProject', developer = 'main', main_file =  'src/{developer}/{name}', version: str = '0.0.1'):
        self.page = page
        self.developer = developer
        self.diricrori = os.path.join(self.page, name)
        self.main_file = os.path.join(self.diricrori, main_file.format(developer = developer, name = name))
        self.name = name
        self.version = version
        self.der = os.path.dirname(os.path.abspath(__file__))
    def start(self):
        if os.path.exists(self.page):
            mkdir(self.diricrori)
            mkdir(os.path.join(self.diricrori, "src"))
            mkdir(os.path.join(self.diricrori, "src", self.developer))
            mkdir(self.main_file)
            copin(os.path.join(self.der, 'text', 'Main.py'), os.path.join(self.main_file, 'Main.py'))
            d = open(os.path.join(self.der, 'text', '__main__.py'), 'r')
            f = open(os.path.join(self.diricrori, '__main__.py'), 'w')
            f.write(d.read().format(developer = self.developer, name = self.name))
            f.close()
            d.close()
            mkdir(os.path.join(self.diricrori, 'mods'))
            mkdir(os.path.join(self.diricrori, 'sys_files'))
            mkdir(os.path.join(self.diricrori, 'program_fils'))
            mkdir(os.path.join(self.diricrori, 'python3'))
            shutil.copytree(os.path.dirname(self.der), os.path.join(self.diricrori, "PyForge"))

        else:
            raise InvalidPageError('Не найдена дериктория.')

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

if __name__ == '__main__':
    CreatingStructure('d', 'd', 'd').start()