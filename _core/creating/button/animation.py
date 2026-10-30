from ....easel import PfObject, Surface
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from .button import _AnimationButton
else:
    _AnimationButton = Any


class FrameAnimationButton(PfObject):
    def __init__(self):
        super().__init__(None, (0, 0), (0, 0))

    def __call__(self, button: _AnimationButton): # для получении объекта кнопки
        self.button = button

    def effect(self):
        "при вызове эффекта"
        
    def clicking(self):
        pass

    # рабочие функции

    def event(self, event):
        return super().event(event)

    def draw(self, win):
        return super().draw(win)

    def update(self, dt):
        return super().update(dt) 

    def mousebuttondown(self, common, button):
        return super().mousebuttondown(common, button)

    def mousemotion(self, common, motion):
        return super().mousemotion(common, motion)
    