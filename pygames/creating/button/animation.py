from pygame import Surface

class FrameAnimationButton:
    # структура посторойки анимациий на кнопки
    def __init__(self):
        # инцилизация
        pass
    def update(self):
        # обновление
        pass
    def event(self, event):
        # при какомто жвенти
        pass
    def __call__(self, button): # для получении обьекта кнопки
        self.button = button
    def efects(self):
        # при вызове efects
        pass
    def draw(self, screen: Surface):
        # для рисования
        pass
    