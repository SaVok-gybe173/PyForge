from ..._core.creating.progress.structure import _ProgressBar
from ...easel.draw import rect

class ProgressBar(_ProgressBar):
    def draw(self, scene):
        rect(scene, self.color, self.rect)