from typing import Union, Optional, Dict
from .._core.resources import TypeFile as TypeTexture, load_dir
import tempfile
import os
import zipfile
from typing import Callable
import pygame as pg
import shutil


class Texture:
    temp = tempfile.mkdtemp()
    texture: dict[str, dict | pg.Surface]

    def __init__(self, texturfile: str | None, typefile: Optional[str] = TypeTexture.ZIP):
        if texturfile is None:
            self.texture = {}
            return
        if typefile == TypeTexture.ZIP:
            with zipfile.ZipFile(texturfile, 'r') as zip_ref:
                zip_ref.extractall(self.temp)
                texturfile = self.temp

        elif not typefile == TypeTexture.DIR:
            raise ValueError("не верный тип данных typefile")
        self.texture = load_dir(texturfile, pg.image.load)

    def __del__(self):
        shutil.rmtree(self.temp)
    
    def get(self, *path):

        dat = self.texture
        for i in path:
            try:
                dat = dat[i]
            except KeyError:
                dat[i] = {}
                dat = dat[i]
        return dat
    
    def add(self, path: tuple[str]|str, textur: Union["Texture", Dict[str, Union["Texture", pg.Surface]], pg.Surface]):
        if type(path) is str:
            path = path.split("/")

        if type(textur) is Texture:
            textur = textur.texture
        self.get(*path[:-1])[path[-1]] = textur
    

class _AppTexture(Texture):
    _instance: "_AppTexture" = None
    __update_fun: list[Callable] = []


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            #cls.__init__ = object.__init__
        return cls._instance
    
    @classmethod
    def add_fun(cls, fun):
        cls.__update_fun.append(fun)
        return fun
    
    
    def add(self, path: tuple[str], textur: Union["Texture", Dict[str, Union["Texture", pg.Surface]], pg.Surface]):
        super().add(path, textur)
        self.update_fun()
    
    @classmethod
    def update_fun(cls):
        for fun in cls.__update_fun:
            fun()

    
    def get(self, *path):
        return super().get(*path)

def makeSheet(texture: _AppTexture|Texture|dict):
    if not type(texture) is dict: texture = texture.texture
    def flatten_dict(d, parent_key='', sep='/'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    return flatten_dict(texture)

def getAppTexture() -> _AppTexture:
    return _AppTexture._instance

def newAppTexture(texturfile: str | None, typefile: Optional[str] = TypeTexture.ZIP) -> _AppTexture:
    return _AppTexture(texturfile, typefile)