from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from dataclasses import dataclass

import math
import numpy as np
try:
    import pygame
except ImportError as e:
    print("102 - error:", e)
    import sys
    sys.exit(102)

@dataclass
class aabb:
    left: int 
    right: int
    bottom: int
    top: int

class SurfaceGL:
    def __init__(self, x=0, y=0, width=100, height=100, color=(1.0, 1.0, 1.0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vertices = self._create_rectangle_vertices()
        self.rotation = 0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.is_circle = False
        self.circle_radius = min(width, height) / 2
        
    def _create_rectangle_vertices(self):
        """Создает вершины прямоугольника"""
        half_w = self.width / 2
        half_h = self.height / 2
        return [
            [-half_w, -half_h],  
            [half_w, -half_h],   
            [half_w, half_h],    
            [-half_w, half_h]   
        ]
    
    def _create_circle_vertices(self, segments=32):
        """Создает вершины круга"""
        vertices = []
        for i in range(segments):
            angle = i * (2 * math.pi / segments)
            x = math.cos(angle) * self.circle_radius
            y = math.sin(angle) * self.circle_radius
            vertices.append([x, y])
        return vertices
    
    def transform_vertices(self, new_vertices):
        """Изменяет вершины объекта"""
        self.vertices = new_vertices
        self.is_circle = False
        
    def to_circle(self, segments=32):
        """Преобразует объект в круг"""
        self.is_circle = True
        self.circle_radius = min(self.width, self.height) / 2
        self.vertices = self._create_circle_vertices(segments)
        
    def set_position(self, x, y):
        """Устанавливает позицию объекта"""
        self.x = x
        self.y = y
        
    def set_rotation(self, angle):
        """Устанавливает угол поворота (в градусах)"""
        self.rotation = angle
        
    def set_scale(self, scale_x, scale_y=None):
        """Устанавливает масштаб"""
        self.scale_x = scale_x
        self.scale_y = scale_y if scale_y is not None else scale_x
        
    def get_transformed_vertices(self):
        """Возвращает преобразованные вершины с учетом позиции, поворота и масштаба"""
        transformed = []
        
        for vertex in self.vertices:
            x = vertex[0] * self.scale_x
            y = vertex[1] * self.scale_y  
            if self.rotation != 0:
                rad = math.radians(self.rotation)
                cos_a = math.cos(rad)
                sin_a = math.sin(rad)

                x_rot = x * cos_a - y * sin_a
                y_rot = x * sin_a + y * cos_a
                x, y = x_rot, y_rot
            
            x += self.x
            y += self.y
            
            transformed.append([x, y])
        return transformed
    
    def get_aabb(self) -> aabb:
        """Возвращает AABB (Axis-Aligned Bounding Box) объекта"""
        vertices = self.get_transformed_vertices()
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        return aabb(min(xs),max(xs),min(ys),max(ys))
    
    def collides_with_point(self, point_x, point_y):
        """Проверяет коллизию с точкой (мышью)"""
        if self.is_circle:
            distance = math.sqrt((point_x - self.x)**2 + (point_y - self.y)**2)
            return distance <= (self.circle_radius * max(self.scale_x, self.scale_y))
        else:
            aabb = self.get_aabb()
            return (aabb.left <= point_x <= aabb.right and 
                    aabb.bottom <= point_y <= aabb.top)
    
    def collides_with_surface(self, other_surface: "SurfaceGL"):
        """Проверяет коллизию с другим SurfaceGL объектом"""
        aabb1 = self.get_aabb()
        aabb2 = other_surface.get_aabb()
        
        return not (aabb1.right <= aabb2.left or
                   aabb1.left >= aabb2.right or
                   aabb1.top <= aabb2.bottom or
                   aabb1.bottom >= aabb2.top)
    
    def draw(self):
        """Отрисовывает объект"""
        glColor3f(*self.color)
        vertices = self.get_transformed_vertices()
        
        if self.is_circle:
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(self.x, self.y) 
            for vertex in vertices:
                glVertex2f(vertex[0], vertex[1])
            glVertex2f(vertices[0][0], vertices[0][1])  
            glEnd()
        else:
            glBegin(GL_QUADS)
            for vertex in vertices:
                glVertex2f(vertex[0], vertex[1])
            glEnd()

def init_2d(width, height):
    """Инициализация OpenGL для 2D"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, height, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def draw_line(x1, y1, x2, y2, color, width=1):
    """Рисование линии"""
    glColor3f(*color)
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

if __name__ == "__main__":
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("SurfaceGL Demo - 2D Objects with Collision")
    
    init_2d(display[0], display[1])
    
    rect1 = SurfaceGL(200, 200, 150, 100, (1.0, 0.0, 0.0))
    rect2 = SurfaceGL(400, 300, 120, 120, (0.0, 1.0, 0.0))
    
    circle1 = SurfaceGL(600, 200, 80, 80, (0.0, 0.0, 1.0))
    circle1.to_circle()
    
    triangle = SurfaceGL(200, 400, 100, 100, (1.0, 1.0, 0.0))
    triangle_vertices = [[0, -50],[50, 50], [-50, 50]]
    triangle.transform_vertices(triangle_vertices)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rect2.set_position(mouse_x, mouse_y)
        triangle.set_rotation(pygame.time.get_ticks() / 10 % 360)
        scale = 1.0 + 0.5 * math.sin(pygame.time.get_ticks() / 500)
        circle1.set_scale(scale)
        
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        rect1.draw()
        rect2.draw()
        circle1.draw()
        triangle.draw()
        collisions = []
        if rect2.collides_with_point(mouse_x, mouse_y):
            collisions.append(("Mouse", "Green Rect"))
            rect2.color = (1.0, 1.0, 1.0)  
        else:
            rect2.color = (0.0, 1.0, 0.0)  
        if rect1.collides_with_surface(rect2):
            collisions.append(("Red Rect", "Green Rect"))
            rect1.color = (1.0, 0.5, 0.5)  
        else:
            rect1.color = (1.0, 0.0, 0.0) 
            
        if circle1.collides_with_surface(rect2):
            collisions.append(("Blue Circle", "Green Rect"))
            circle1.color = (0.5, 0.5, 1.0)  
        else:
            circle1.color = (0.0, 0.0, 1.0)
        for obj in [rect1, rect2, circle1, triangle]:
            aabbf = obj.get_aabb()
            draw_line(aabbf.left, aabbf.bottom, aabbf.right, aabbf.bottom, (1, 1, 1), 1)
            draw_line(aabbf.right, aabbf.bottom, aabbf.right, aabbf.top, (1, 1, 1), 1)
            draw_line(aabbf.right, aabbf.top, aabbf.left, aabbf.top, (1, 1, 1), 1)
            draw_line(aabbf.left, aabbf.top, aabbf.left, aabbf.bottom, (1, 1, 1), 1)
        pygame.display.set_caption(f"SurfaceGL Demo - Collisions: {len(collisions)}")
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()