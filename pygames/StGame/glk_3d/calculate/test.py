import pygame
import numpy as np
import math

# Инициализация
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ============ КАМЕРА С МЕТОДОМ EVENT ============
class OrbitCamera:
    def __init__(self, target=(0, 0, 0)):
        self.target = np.array(target, dtype=float)  # Центр вращения
        self.distance = 10.0  # Расстояние до цели
        self.angle_x = 0.0    # Горизонтальный угол
        self.angle_y = 0.0    # Вертикальный угол
        self.update_position()
        
    def update_position(self):
        """Обновляем позицию камеры на основе углов и расстояния"""
        # Ограничиваем вертикальный угол
        self.angle_y = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.angle_y))
        
        # Вычисляем позицию камеры
        x = self.distance * math.cos(self.angle_y) * math.sin(self.angle_x)
        y = self.distance * math.sin(self.angle_y)
        z = self.distance * math.cos(self.angle_y) * math.cos(self.angle_x)
        
        self.pos = np.array([x, y, z]) + self.target
        
    def event(self, event):
        """Обрабатывает события мыши для вращения камеры"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши - начало вращения
                pygame.mouse.get_rel()  # Сбрасываем относительное движение
            elif event.button == 4:  # Колесико вверх - приближение
                self.distance = max(3.0, self.distance - 1.0)
                self.update_position()
            elif event.button == 5:  # Колесико вниз - отдаление
                self.distance = min(30.0, self.distance + 1.0)
                self.update_position()
                
        elif event.type == pygame.MOUSEMOTION:
            # Проверяем, зажата ли левая кнопка мыши
            if pygame.mouse.get_pressed()[0]:  # 0 - левая кнопка
                # Получаем относительное движение мыши
                dx, dy = pygame.mouse.get_rel()
                
                # Добавляем к углам вращения
                sensitivity = 0.01
                self.angle_x += dx * sensitivity
                self.angle_y += dy * sensitivity
                
                # Обновляем позицию
                self.update_position()

# ============ КУБ ============
class Cube:
    def __init__(self, pos=(0, 0, 0), size=2):
        self.pos = np.array(pos, dtype=float)
        self.size = size
        self.color = (200, 100, 50)
        
        # Вершины куба
        s = size / 2
        self.vertices = np.array([
            [-s, -s, -s], [ s, -s, -s], [ s,  s, -s], [-s,  s, -s],
            [-s, -s,  s], [ s, -s,  s], [ s,  s,  s], [-s,  s,  s],
        ]) + self.pos
        
        # Грани
        self.faces = [
            (0,1,2,3), (4,5,6,7), (0,1,5,4),
            (2,3,7,6), (1,2,6,5), (0,3,7,4),
        ]
        
        # Углы вращения куба
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0
        
    def update(self, dt):
        """Обновляет вращение куба"""
        self.rot_x += 0.5 * dt
        self.rot_y += 0.3 * dt
        self.rot_z += 0.2 * dt
        
    def get_rotated_vertices(self):
        """Возвращает вершины куба после вращения"""
        s = self.size / 2
        local_vertices = np.array([
            [-s, -s, -s], [ s, -s, -s], [ s,  s, -s], [-s,  s, -s],
            [-s, -s,  s], [ s, -s,  s], [ s,  s,  s], [-s,  s,  s],
        ])
        
        # Матрицы вращения куба
        rx = np.array([
            [1, 0, 0],
            [0, math.cos(self.rot_x), -math.sin(self.rot_x)],
            [0, math.sin(self.rot_x), math.cos(self.rot_x)]
        ])
        
        ry = np.array([
            [math.cos(self.rot_y), 0, math.sin(self.rot_y)],
            [0, 1, 0],
            [-math.sin(self.rot_y), 0, math.cos(self.rot_y)]
        ])
        
        rz = np.array([
            [math.cos(self.rot_z), -math.sin(self.rot_z), 0],
            [math.sin(self.rot_z), math.cos(self.rot_z), 0],
            [0, 0, 1]
        ])
        
        # Комбинируем вращения
        rotation_matrix = ry @ rx @ rz
        
        # Применяем вращение и позицию
        rotated = local_vertices @ rotation_matrix.T
        return rotated + self.pos
    
    def draw(self, camera, screen):
        """Рисует куб на экране"""
        # Получаем вершины куба после вращения
        world_verts = self.get_rotated_vertices()
        
        # Преобразуем в координаты камеры
        cam_verts = world_verts - camera.pos
        
        # Проецируем на экран
        screen_points = []
        for x, y, z in cam_verts:
            # Ближняя плоскость отсечения
            if z <= 0:
                screen_points.append(None)
                continue
                
            # Проекция
            f = 200 / z
            sx = WIDTH/2 + x * f
            sy = HEIGHT/2 - y * f
            screen_points.append((sx, sy))
        
        # Рисуем грани
        for face in self.faces:
            points = []
            valid = True
            for i in face:
                if screen_points[i] is None:
                    valid = False
                    break
                points.append(screen_points[i])
            
            if valid and len(points) >= 3:
                pygame.draw.polygon(screen, self.color, points, 1)

# ============ СЦЕНА ============
# Создаем куб
cube = Cube(pos=(0, 0, 0), size=2)

# Создаем камеру
camera = OrbitCamera(target=cube.pos)

# Скрываем курсор мыши
pygame.mouse.set_visible(False)

# ============ ГЛАВНЫЙ ЦИКЛ ============
running = True
while running:
    dt = clock.tick(60) / 1000
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
            # Передаем событие мыши в камеру
            camera.event(event)
    
    # Обновление куба
    cube.update(dt)
    
    # Отрисовка
    screen.fill((20, 20, 30))
    
    # Рисуем куб
    cube.draw(camera, screen)
    
    # Отрисовка информации
    font = pygame.font.SysFont(None, 24)
    
    # Позиция камеры
    info_lines = [
        f"Позиция камеры: ({camera.pos[0]:.1f}, {camera.pos[1]:.1f}, {camera.pos[2]:.1f})",
        f"Расстояние: {camera.distance:.1f}",
        f"Углы: X={math.degrees(camera.angle_x):.1f}°, Y={math.degrees(camera.angle_y):.1f}°",
        "Управление:",
        "ЛКМ + движение - вращение камеры",
        "Колесико - приближение/отдаление",
        "Esc - выход"
    ]
    
    y_offset = 10
    for i, line in enumerate(info_lines):
        if i == 3:  # После углов добавляем отступ
            y_offset += 10
        text = font.render(line, True, (200, 200, 200) if i >= 3 else (255, 255, 255))
        screen.blit(text, (10, y_offset))
        y_offset += 25
    
    # FPS
    fps = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps, (WIDTH - 100, 10))
    
    pygame.display.flip()

pygame.quit()