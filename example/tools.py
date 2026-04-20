import pygame as pg
import sys
from functools import wraps
sys.path.append("C:\\Users\\SaVok\\Desktop\\PygameRedactor")
from PyForge.tools import cordinate_transformation as ct

def decorete_cord(fun):
    @wraps(fun)
    def wrapper(*arg, **karg):
        arg = [*arg]
        print(arg)
        if type(arg[0]) is int:
            arg[1] = -arg[1]
        else:
            arg[0] = (arg[0][0], -arg[0][1])
        return fun(*arg, **karg)
        print(arg)
    return wrapper

#ct = decorete_cord(ct)

if __name__ == '__main__':

    pg.init()
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    running = True
    while running:
        screen.fill((25, 25, 25))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        pg.draw.line(screen, (255,255,255), ct((0,0 )), ct((1, 0)) )
        pg.draw.line(screen, (255,255,255), ct((0,0 )), ct((0, 1)) )
        pg.draw.line(screen, (255,255,255), ct((-0.5, 0.5 )), ct((0.5, -0.5)) )
        pg.draw.circle(screen, (255,255,255), ct((1, 1)), 50)
        pg.draw.circle(screen, (255,255,255), ct((-1, -1)), 50)
        clock.tick(60)
        pg.display.flip()
    pg.quit()