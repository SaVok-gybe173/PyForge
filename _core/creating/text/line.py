from PyForge.font.ttf.font import Font
from PyForge.font.ttf.render import render_text
from PyForge.easel import Window, PfObjectIMG
from PyForge.easel.surface import Surface
from PyForge.math.markup import Point, Size
from PyForge.easel.event import CommonEvent, MouseButtonEvent, MouseMotionEvent
from PyForge._core.creating.input.core import GraphicsInputTextCore

FONT = "minecraft.ttf"

class TextLine(PfObjectIMG):
    font: Font # шрифт
    core: GraphicsInputTextCore # ядро текста
    layout: tuple[list[float], list[float], list[int]] # тех инфа для выделения
    _min_y: int
    _size_px: int
    _color: tuple
    anchor: int = 0 # начальный символ
    idx: int = 0 # конечный символ
    dragging: bool # активно ли щас выделение

    def __init__(self, page: Window, left_top: Point | tuple[int, int], font: str | Font, text: str, size_px: int, color: tuple[int, int, int] = (255, 255, 255)):
        if isinstance(font, str): self.font = Font(font)
        elif isinstance(font, Font): self.font = font
        else: return ValueError()
        self._size_px = size_px
        self._color = color
        self.core = GraphicsInputTextCore(text)
        sur, self._min_y = render_text(self.font, text, size_px, color)
        super().__init__(page, left_top, sur)
        self.layout =   self.font.layout(text, size_px, self.top)
        print(self.layout)

    def draw(self, win: Surface): # убрать потом
        win.blit(self.img, (self.left, self.top-self._min_y))

    # события
    def mousebuttondown(self, common: CommonEvent, button: MouseButtonEvent):
        self.idx = self.ancho = self.core.hit_test(button.x, self.layout[0], self.layout[1])
        self.dragging = True
        self.core.set_selection(self.anchor, self.idx) # каретка, без выделения

    def mousemotion(self, common: CommonEvent, motion: MouseMotionEvent):
        self.idx = self.core.hit_test(motion.x, self.layout[0], self.layout[1])
        self.core.set_selection(self.anchor, self.idx)

    def mousebuttonup(self, common, button):
        self.dragging = False

    # сеттеры и геттеры
    @property
    def text(self) -> str:
        return self.core.text
    @text.setter
    def text(self, text: str) -> None:
        self.core.text = text
        self.layout = self.font.layout(text, self.size_px, self.top)
        self.img, self._min_y = render_text(self.font, text, self._size_px, self._color)

    @property
    def size_px(self) -> int:
        return self._size_px
    @size_px.setter
    def size_px(self, size_px: int) -> None:
        self._size_px = size_px
        self.layout = self.font.layout(self.text, size_px, self.top)
        self.img, self._min_y = render_text(self.font, self.core.text, size_px, self._color)