from PyForge.easel.app import App
from PyForge.easel.scene import Scene
from PyForge.easel.surface import Surface
from PyForge.widget.button import Button

class MainScene(Scene):
    def clickButtonMain(self, num: int):
        print(f"Нажата кнопка {num}!")
    
    def __init__(self, page: App):
        super().__init__(page)
        sur = Surface((100, 100), flags=0)
        self.append(Button(page, (150, 150), sur, is_click=self.clickButtonMain))

def main(dir: str) -> int:
    app = App(size=(400, 400), scene=[MainScene])
    app.start()