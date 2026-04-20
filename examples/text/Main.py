from PyForge import Game
import os
import pygame as pg

class Main(Game):
    condition = 0
    def __init__(self, direct):
        self.direct = direct
        super().__init__((0,0), (25,25,25), flags = 0, mods_dir=os.path.join(direct, 'mods'),) 