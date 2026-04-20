import pygame as pg, numpy as np, math
from PyForge.tools import PfObject

def degrees_to_radians(deg: int):
    # из в градуса в радиант
    return deg * math.pi / 180.0

def none(*args, **kargs):
            return None

# ---------- Camera (orbit) ----------
class _Camera(PfObject):
    mouse_pressed = False
    fun_turn_x = none
    def __init__(self, pos=[0,0,0], yaw=0.0, pitch=0.0):
        """
        pos - позиция камеры
        yaw - наклон камеры
        pitch - угол поворота
        """
        self.pitch = float(pitch)
        self.pos = pos
        self.yaw = float(yaw)
        self.fov = 1.0
        self.speed_x = 0.25
        self.speed_z = 0.25
        self.speed_y = 0.25
        self.angle_x = 3    # Угол по горизонтали (радианы)
        self.angle_y = 3
        self.target = np.array((0, 0, 10), dtype=float)
    def update_move(self, keys):
        """Обновляет вектор движения на основе нажатых клавиш"""
        
        # Движение происходит по осям мира:
        # X - влево/вправо
        # Y - вверх/вниз  
        # Z - вперед/назад
        if keys[pg.K_w]:  # Вперед (по оси Z)
            self.pos[2] += math.cos(self.pitch) * self.speed_z
            self.pos[0] += math.sin(self.pitch) * self.speed_z
        if keys[pg.K_s]:  # Назад
            self.pos[2] -= math.cos(self.pitch) * self.speed_z
            self.pos[0] -= math.sin(self.pitch) * self.speed_z
        if keys[pg.K_d]:  # Вправо (по оси X)
            self.pos[0] -= math.cos(self.pitch) * self.speed_x
            self.pos[2] -= math.sin(self.pitch) * self.speed_x
        if keys[pg.K_a]:  # Влево
            self.pos[0] += math.cos(self.pitch) * self.speed_x
            self.pos[2] += math.sin(self.pitch) * self.speed_x
        if keys[pg.K_SPACE]:  # Вверх (по оси Y)
            self.pos[1] += self.speed_y
        if keys[pg.K_LCTRL]:  # Вниз
            self.pos[1] -= self.speed_y
        print( self.pos)
    def update(self):
        if self.pitch > math.pi:
            print(self.pitch)
    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                self.mouse_pressed = True
                self.last_mouse_pos = pg.mouse.get_pos()
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_pressed = False
        elif event.type == pg.MOUSEMOTION:
            if self.mouse_pressed:
                current_pos = pg.mouse.get_pos()
                dx = current_pos[0] - self.last_mouse_pos[0]
                dy = current_pos[1] - self.last_mouse_pos[1]
                self.pitch += dx/10*self.angle_x
                self.fun_turn_y(self.yaw)
                self.fun_turn_x(dx/10*self.angle_x)
                print()
                self.yaw += dy/10*self.angle_x
                self.fun_turn_y(-self.yaw)
                self.last_mouse_pos = current_pos
    def turn_x(self, fun):
        self.fun_turn_x = fun
        def wrapper(*args, **kargs):
            return fun(*args, **kargs)
        return wrapper
    def turn_y(self, fun):
        self.fun_turn_y = fun
        def wrapper(*args, **kargs):
            return fun(*args, **kargs)
        return wrapper
    
class Camera(_Camera):
    def update_move(self, keys):
        x = y = z = 0


        if keys[pg.K_w]:  # Вперед (по оси Z)
            z += self.speed_z
        if keys[pg.K_s]:  # Назад
            z -= self.speed_z
        if keys[pg.K_d]:  # Вправо (по оси X)
            x -= self.speed_x

        if keys[pg.K_a]:  # Влево
            x += self.speed_x

        if keys[pg.K_SPACE]:  # Вверх (по оси Y)
            y += self.speed_y
        if keys[pg.K_LCTRL]:  # Вниз
            y -= self.speed_y
        self.pos[0] += x
        self.pos[1] += y
        self.pos[2] += z
        return x, y, z


if __name__ == "__main__":
    width, height = 1000, 700
        
    pg.init()
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()
    
    #d = get_figyre('C:\\Users\\SaVok\\Desktop\\Новаяпапка\\genr\\UXM6SH5PW8QC2PRJYCLOJN3M5.obj', (width, height))

    cam = Camera()

    p = 20
    r = 1

    while r:
        cam.update()
        #p -= 0.1
        screen.fill((0, 0, 0))
        for event in pg.event.get(): 
            if event.type == pg.QUIT: r = 0
        pg.display.flip()
        #print(clock.get_fps())
    pg.quit()
