from typing import Callable, Any
import pygame as pg
import os

class TypeFile:
    ZIP = 'z'
    DIR = 'd'

class ErrorFile:
    def __init__(self, error: Exception, path: str):
        self.error = error
        self.path = path
    def __str__(self):
        return f"{self.path}  --> {str(self.error)}"

def load_dir(path: str, load: Callable):
    data: dict[str, dict | Any] = {}
    for i in os.listdir(path):
        file = os.path.join(path, i)
        if os.path.isdir(file):
            data[i] = load_dir(file, load)

        else:
            try:
                data[i] = load(file)
            except Exception as e:
                data[i] = ErrorFile(e, file)
    return data
