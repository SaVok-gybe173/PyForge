import pygame as pg

class FrameMod:
    game:object
    
    __version__ = '0.0.1'
    __names__ = None
    __tims__ = []
    
    def __init__(self, game):
        self.game = game
    def close(self):
        '''
        сработает после завершении порграммы
        '''
    def event(self, event:pg.event.get):
        '''
        сработает for event in pg.event.get()
        Аргументы:
            event: pg.event.get
        '''
    def draw(self, screen: pg.display.set_mode):
        '''
        сработает при каждом цикле
        Аргументы:
            screen: pg.display.set_mode
        '''

class Main(FrameMod):
    def __init__(self, game):
        super().__init__(game)
