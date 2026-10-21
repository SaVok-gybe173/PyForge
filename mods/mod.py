from ..easel.event import Event

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
    def event(self, event: Event):
        '''
        сработает for event in Event
        Аргументы:
            event: Event
        '''
    def draw(self, screen):
        '''
        сработает при каждом цикле
        Аргументы:
            screen: Surface
        '''
    def start(self):
        pass

class Main(FrameMod):
    def __init__(self, game):
        super().__init__(game)
