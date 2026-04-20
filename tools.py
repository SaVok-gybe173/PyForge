import pygame

def cordinate_transformation(fraction: tuple[float]) -> tuple[int]:
    size = pygame.display.get_window_size()
    return size[0]/2*(fraction[0]+1), size[1]/2*(-fraction[1]+1)

def cord(event: pygame.event.Event, i = 1):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == i:
            print(event.pos)
            return event.pos
class MathCord:
    stade = None
    def event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.stade is None:
                self.stade = cord(event)
                print(f"сохранено {self.stade}")
            else:
                stade = cord(event)
                print(f"x_y = ({min((self.stade[0], stade[0]))}, {min((self.stade[1], stade[1]))}), w_h = ({abs(self.stade[0]-stade[0])}, {abs(self.stade[1]-stade[1])})")
                self.stade = None
    def __call__(self, event: pygame.event.Event):
        self.event(event)

class PfObject:
    def draw(self, sceen: pygame.Surface):
        pass
    def update(self):
        pass
    def event(self, event: pygame.event.Event):
        pass

    def size_update(self, old: tuple[int], new: tuple[int]):
        pass

    