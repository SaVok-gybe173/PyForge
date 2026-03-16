import math
import pygame
import numpy as np

try:
    from .plaer import Camera
except ImportError:
    from plaer import Camera

try:
    from .calculate import _Figur
except ImportError:
    try:
        from calculate import _Figur
    except Exception as e:
        raise ImportError(e)
else:
    pass

def degrees_to_radians(deg: int):
    # из в градуса в радиант
    return deg * math.pi / 180.0

def load_obj(filename, texturs = False):
    vertices = []
    faces = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == 'v':
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                vertices.append((x, y, z))
            elif parts[0] == 'f':
                face_vertices = []
                cld = 0
                for part in parts[1:4]:
                    indices = part.split('/')
                    vertex_index = int(indices[0]) - 1
                    face_vertices.append(vertex_index)
                    cld += 1
                if not texturs:
                    del face_vertices[-1]
                faces.append(face_vertices)
    
    return vertices, faces

class Figure(_Figur):
    
    # Вершины куба
    @property
    def vertices(self):
        return self.get_projected_vertices()
    @vertices.setter
    def vertices(self, vertices: list[list[int,int,int | float]]):
        self.set_vertices(np.array(vertices, dtype=np.float32))
    
    @property
    def edges(self):
        return self.get_edges()
    @edges.setter
    def edges(self, edges):
        self.set_edges(edges)

    def __init__(self, width_height , position: tuple = (0.0, 0.0, 0.0)):
        width_, height_ = width_height
        super().__init__(width_, height_, position)
    def class_draw(self, start, end):
        pygame.draw.line(self.holst, (255, 255, 255), start, end, 2)
    def draw(self, holst):
        v = self.vertices
        for i in self.edges:
            pygame.draw.line(holst, (255, 255, 255), v[i[0]], v[i[1]], 2)
            #self.class_draw(v[i[0]], v[i[1]])
    def turn_y(self, i):
        super().turn_y(i)
    def turn_x(self, i):
        super().turn_x(i)
    def turn_z(self, i):
        super().turn_z(i)
    def update(self, flow = 0 , smesh = [0.0, 0.0, 0.0]):
        super().update(flow, smesh)

def get_figyre(data: str = '.obj', holst = pygame.Surface((500, 500))):
    figure = Figure( holst)
    vertices, edges= load_obj(data)
    figure.edges = edges
    figure.vertices = vertices
    return figure

        
if __name__ == "__main__":
    width, height = 1000, 700
        
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    
    #d = get_figyre('C:\\Users\\SaVok\\Desktop\\Новаяпапка\\genr\\UXM6SH5PW8QC2PRJYCLOJN3M5.obj', (width, height)) 
    d = Figure((width, height))
    cam = Camera()
    #print(load_obj("C:\\Users\\SaVok\\Desktop\\Untitled.obj"))
    d.vertices, d.edges = load_obj('C:\\Users\\SaVok\\Desktop\\Новаяпапка\\genr\\UXM6SH5PW8QC2PRJYCLOJN3M5.obj')#create_unit_cube() C:\Users\SaVok\Desktop\source\de_dust2.obj
    p = 0.0
    r = 1
    d.turn_y(180)
    objects: list[Figure] = [d]
    d.set_fov(70)

    @cam.turn_x
    def turn_x(gradus):
        for obs in objects:
            obs.turn_x(gradus)
            print(1)
    @cam.turn_y
    def turn_y(gradus):
        for obs in objects:
            obs.turn_y(gradus)
            print(1)

    while r:
        keys = pygame.key.get_pressed()
        screen.fill((0, 0, 0))
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: r = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(d.vertices)
            cam.event(event)
        #d.turn_x(1)
        cam.update()
        #print(cam.update_move(keys))
        d.set_position(cam.update_move(keys))
        d.update()
        d.draw(screen)
        pygame.display.flip()
        #print(clock.get_fps())
    pygame.quit()
