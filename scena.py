try:
    from .EaselPy.strukture import Scene
    from .pygames.creating.button import Button, ButtonClick, AnimationButton, FrameAnimationButton, Increase, Impuls, CollorsClick
    from .__info__ import __version__
    from .pygames.creating.listitng import ListItems, ListOfItems, FrameListItems
except ImportError:
    from EaselPy.strukture import Scene
    from pygames.creating.button import Button, ButtonClick, AnimationButton, FrameAnimationButton, Increase, Impuls, CollorsClick
    from pygames.creating.listitng import ListItems, ListOfItems, FrameListItems
    from __info__ import __version__
import json, pygame as pg

"&" # переменная в функции
"$" #обращение к классу

funcs = {
    "a0aa111aa11a": Button,
    "a0aa111aa11b": ButtonClick,
    "a0aa111aa11c": AnimationButton,
    "a0aa111aa11d": FrameAnimationButton,
    "a0aa111aa11e": Increase,
    "a0aa111aa11r": Impuls,
    "a0aa111aa11r": CollorsClick,

    "a0aa111aa13a": ListItems,
    "a0aa111aa13b": ListOfItems,
    "a0aa111aa13c": FrameListItems,

    "b0aa111aa11a": pg.image.load,
    "b0aa111aa11b": pg.image.save,
}

start_scena = """# PyForge v{version}
import pygame as pg
import PyForge

class {MyScene}(PyForge.Scene):
"""

print(start_scena)

def load_sene(file: str = "*.json", screen = None) -> Scene:
    """
    Docstring для load_sene
    
    :param file: Фаил загрузочной сценны
    :type file: str
    :param screen: Основное окно
    :return: Сцена
    :rtype: Scene
    """
    with open(file, 'r')  as f:
        s: dict = json.loads(f.read())
    scena = Scene(screen)
    for d, arg in s["def"].items():
        print(d, arg)
        peremen = dict()
        if d == "__init__":
            for init, init_arg in arg.items():
                if init_arg['type'] == 'return':
                    args_f = []
                    kargs_f = dict()
                    for f in init_arg['args']:
                        try:
                            if type(f) is str:
                                if f[0] == "$":
                                    f = scena.__dict__[f[1:]]
                                elif f[0] == "&":
                                    f = peremen[f[1:]]
                        except Exception: ...
                        args_f.append(f)
                    for k, f in init_arg['kargs'].items():
                        try:
                            if type(f) is str:
                                if f[0] == "$":
                                    f = scena.__dict__[f[1:]]
                                elif f[0] == "&":
                                    f = peremen[f[1:]]
                        except Exception: ...
                        kargs_f[k] = f
                    if init_arg['name'][0] == "$":
                        scena.__dict__[init_arg['name'][1:]] = funcs[init](*args_f, **kargs_f)
                    elif init_arg['name'][0] == "&":
                        
                        peremen[init_arg['name'][1:]] = funcs[init](*args_f, **kargs_f)
    return scena

def save_python(file: str = "*.json"):
    with open(file, 'r')  as f:
        s: dict = json.loads(f.read())
    scena = ""
    for d, arg in s["def"].items():
        print(d, arg)
        if d == "__init__":
            scena += "\tdef __init__(self, screen: pg.Surfase):\n"
            for init, init_arg in arg.items():
                if init_arg['type'] == 'return':
                    args_f = ""
                    kargs_f = ""
                    for f in init_arg['args']:
                        try:
                            if type(f) is str:
                                if f[0] == "$":
                                    f = f"self.{f[1:]}"
                                elif f[0] == "&":
                                    f = f[1:]
                                else:
                                    f = '\"'+f+'\"'
                        except Exception: ...
                        args_f += str(f)+","
                    for k, f in init_arg['kargs'].items():
                        try:
                            if type(f) is str:
                                if f[0] == "$":
                                    f = f"self.{f[1:]}"
                                elif f[0] == "&":
                                    f = f[1:]
                                else:
                                    f = '\"'+f+'\"'
                        except Exception: ...
                        print(f)
                        kargs_f += k+" = "+str(f)+","
                    if init_arg['name'][0] == "$":
                        scena += f"\t\tself.{init_arg['name'][1:]} = PyForge.{funcs[init].__name__}({args_f}{kargs_f})\n"
                    elif init_arg['name'][0] == "&":
                        
                        scena += f"\t\t{init_arg['name'][1:]} = PyForge.{funcs[init].__name__}({args_f}{kargs_f})\n"
            if not arg.items():
                scena += "\t\tpass"
    print(start_scena+scena)
    return (start_scena+scena).format(version = __version__, MyScene = s["name"])
if __name__ == "__main__":
    print(save_python("PyForge\\creating_a_structure\\scena.json"))
    

