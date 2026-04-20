import cv2
import pygame as pg
from PyForge.tools import PfObject

IS_INIT = False

def init():
    global IS_INIT
    cap = cv2.VideoCapture(0)  # 0 обычно означает основную камеру

    if not cap.isOpened():
        raise pg.error("нету камер")
    else: IS_INIT = True

def list_cameras():
    global IS_INIT
    if IS_INIT:
        index = 0
        cameras = []
        while True:
            capture = cv2.VideoCapture(index)
            if not capture.isOpened():
                break
            cameras.append(f"Camera {index}")
            capture.release()
            index += 1
        return cameras
    raise pg.error("нету инцилизации camera.init()")


class Camera(PfObject):
    def __init__(self, width_height, x_y, camer = 0):
        self.x_y = x_y
        self.cap = cv2.VideoCapture(camer)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_height[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, width_height[1])
        self.pygame_frame = pg.Surface(width_height)
        self.is_flip = True
        self.width_height = width_height
    def update(self):
        ret, frame = self.cap.read()

        if ret:
            # OpenCV даёт изображение в BGR, Pygame ожидает RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if self.is_flip:
                frame = cv2.flip(frame, 1)  # зеркалирование по горизонтали (опционально)
            self.pygame_frame = pg.transform.rotate(pg.surfarray.make_surface(frame), -90)
    def draw(self, screen: pg.Surface):
        screen.blit(pg.transform.scale(self.pygame_frame, self.width_height), self.x_y)
