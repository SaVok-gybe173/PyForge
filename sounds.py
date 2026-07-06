from pygame.mixer import *
from typing import Optional, Callable, Union, Dict
from ._core.resources import TypeFile as TypeSound, load_dir
import pygame as pg
import zipfile
import tempfile
import shutil

PYFORGE_SOUNDS = {}

def load(file: str):
    return Sound(file)

class AppSound:
    temp = tempfile.mkdtemp()
    texture: dict[str, dict | pg.Surface]

    _instance: "AppSound" = None
    __update_fun: list[Callable] = []


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            #cls.__init__ = object.__init__
        return cls._instance

    
    def __init__(self, soundfile: str | None, typefile: Optional[str] = TypeSound.ZIP):
        if soundfile is None:
            self.__create( {})
            return
        if typefile == TypeSound.ZIP:
            with zipfile.ZipFile(soundfile, 'r') as zip_ref:
                zip_ref.extractall(self.temp)
                soundfile = self.temp

        elif not typefile == TypeSound.DIR:
            raise ValueError("не верный тип данных typefile")
        self.__create(load_dir(soundfile))

    @classmethod
    def __create(cls, sound):
        cls.sound = sound
        if not "app" in cls.sound:
            cls.sound["app"] = {}
        if not "music" in cls.sound["app"]:
            sound["app"]["music"] = {}
        if not "PyForge" in cls.sound["app"]:
            sound["app"]["music"] = PYFORGE_SOUNDS
    
    def __del__(self):
        shutil.rmtree(self.temp)

    @classmethod
    def get(cls, *path):

        dat = cls.texture
        for i in path:
            try:
                dat = dat[i]
            except KeyError:
                dat[i] = {}
                dat = dat[i]
        return dat
    
    @classmethod
    def add(cls, path: tuple[str]|str, textur: Union["AppSound", Dict[str, Union["AppSound", Sound]], Sound]):
        if type(path) is str:
            path = path.split("/")

        if type(textur) is AppSound:
            textur = textur.texture
        cls.get(*path[:-1])[path[-1]] = textur

def newAppSound(texturfile: str | None, typefile: Optional[str] = TypeSound.ZIP) -> AppSound:
    return AppSound(texturfile, typefile)

def getAppSound() -> AppSound:
    return AppSound._instance

__all__ = [
    "pre_init",
    "init",
    "quit",
    "get_init",
    "stop",
    "pause",
    "unpause",
    "fadeout",
    "set_num_channels",
    "get_num_channels",
    "set_reserved",
    "find_channel",
    "get_busy",
    "get_sdl_version",
    "Sound",
    "music",
    "Channel",

    "TypeSound",
    "AppSound",
    "newAppSound",
    "getAppSound"
]


