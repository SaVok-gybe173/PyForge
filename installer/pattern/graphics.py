from PyForge import Scene
from PyForge.easel.strukture import Window
from PyForge.button import Button, AnimationButton, FrameAnimationButton, Increase, Impuls, CollorsClick
from PyForge.lad import start, load
from PyForge.list import ListItems, ListOfItems
from PyForge.input import InputLine
from PyForge.installer.conductor import select_folder
from PyForge.progress import ProgressBar
try:
    from .theme import TEMA, get_TEMA
    from .language import TRANSLATION, get_TRANSLATION
except (ModuleNotFoundError, ImportError):
    from PyForge.installer.pattern.theme import TEMA, get_TEMA
    from PyForge.installer.pattern.language import TRANSLATION, get_TRANSLATION
try:
    from .format import format_size, _render
    from .create import _create_gray_button, _create_blue_button
except (ModuleNotFoundError, ImportError):
    from PyForge.installer.pattern.format import format_size, _render
    from PyForge.installer.pattern.create import _create_gray_button, _create_blue_button

try:
    from .options import _Options
    from .installclass import ModelInstall
except:
    from PyForge.installer.pattern.options import _Options
    from PyForge.installer.pattern.installclass import ModelInstall

import subprocess
import threading
import pygame as pg
import os

class InstallerScene(Scene):
    def _set_main(self, main_class: "_Installer"):
            self.main = main_class
    def __init__(self, win=None):
        pass
    
    def init(self):
        self.further = pg.Surface((self.main.size[0], 48), pg.SRCALPHA)
        self.further.fill(self.get_tema()["fin_further"])
        pg.draw.line(self.further, self.get_tema()["line"], (0, 0), (self.main.size[0], 0))

    def get_tema(self):
        return TEMA[get_TEMA()]
    def get_translation(self) -> dict[str, dict[str, str]]:
        return TRANSLATION[get_TRANSLATION()]
    
    def draw(self, screen):
        screen.blit(self.further, (0, 332))

def Welcome(version):
    """
    1.

    Приветствие (Welcome)
    Название и логотип программы
    Версия
    Краткое описание, что сейчас будет происходить
    """
    class Welcome(InstallerScene):
        def __init__(self, win=None):
            super().__init__(win)
        def init(self):
            super().init()
            self._Bcancellation = _create_gray_button(self.get_translation()["cancellation"], (self.main.size[0]-90, 15+332), self.get_tema()["text"])
            self._Bfurther = _create_blue_button(self.get_translation()["further"], (self._Bcancellation.x-90, 15+332), self.get_tema()["text"])

            self.icon = pg.surface.Surface((200, 332), pg.SRCALPHA)
            pg.draw.rect(self.icon, (200, 200, 200), self.icon.get_rect(), 1)
            
            self.titul = _render(self.get_translation()["welcome"].format(name=self.main.name), pg.font.Font(r"C:\Windows\Fonts\Arialbd.ttf", 18), self.main.size[0]-210, 0)
            self.info = _render(self.get_translation()["welcome_info"].format(name=self.main.name, version=version), pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12), self.main.size[0]-210, 0)

        def event(self, event):
            self._Bfurther.event(event)
            self._Bcancellation.event(event)

            if self._Bcancellation.lcm(event):
                self._Bcancellation.efects()
                self._Bcancellation.stop()
                self.main.close()
            elif self._Bfurther.lcm(event):
                self._Bfurther.efects()
                self._Bfurther.stop()
                self.main.condition += 1

        def update(self):
            self._Bfurther.update()
            self._Bcancellation.update()

        def draw(self, screen: pg.Surface):
            super().draw(screen)
            self._Bfurther.draw(screen)
            self._Bcancellation.draw(screen)

            screen.blit(self.titul, (210, 5))
            screen.blit(self.info, (210, 72))
            screen.blit(self.icon, (0, 0))

    return Welcome


def EULA(text):
    """
    2.

    Лицензионное соглашение (EULA)
    Текст лицензии в прокручиваемом окне
    Чекбокс "Я принимаю условия" (без него кнопка "Далее" неактивна)
    """
    class EULA(InstallerScene):
        def init(self):
            super().init()
            self._Bcancellation= _create_gray_button(self.get_translation()["cancellation"], (self.main.size[0]-90, 15+332), self.get_tema()["text"])

            # для галочки (позже)
            self.on = _create_blue_button(self.get_translation()["further"], (self._Bcancellation.x-90, 15+332), self.get_tema()["text"])
            self.off = _create_gray_button(self.get_translation()["further"], (self._Bcancellation.x-90, 15+332), self.get_tema()["text"])
            self._Bfurther = self.off # по умолчанию, потом поменять

            def option(activ):
                if activ:
                    self._Bfurther = self.on
                else:
                    self._Bfurther = self.off

            self.options = _Options((40, 290), self.get_translation()["license_agree"], lambda: None)
            self.options.set_switch(option)

            self._Bback = _create_gray_button(self.get_translation()["back"], (self._Bfurther.x-80, 15+332), self.get_tema()["text"])

            self.license = pg.font.Font(r"C:\Windows\Fonts\Arialbd.ttf", 14).render(self.get_translation()["license"], True, self.get_tema()["text"])
            self.license_info = pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 11).render(self.get_translation()["license_info"], True, self.get_tema()["text"])


            self.list = ListOfItems((40, 70), (410, 210), distance=0, items=[ListItems(_render(text,  pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 11), 410))])
            self.holst = pg.Surface((410, 210), pg.SRCALPHA)
            pg.draw.rect(self.holst, (200, 200, 200), self.holst.get_rect(), 1)

        def event(self, event):
                    if self.options.activ:
                        self._Bfurther.event(event)
                    self._Bback.event(event)
                    self._Bcancellation.event(event)
                    self.list.event(event)
                    self.options.event(event)

                    if self._Bback.lcm(event):
                        self._Bback.efects()
                        self._Bback.stop()
                        self.main.condition -= 1
                    elif self._Bfurther.lcm(event) and self.options.activ:
                        self._Bfurther.efects()
                        self._Bfurther.stop()
                        self.main.condition += 1
                    elif self._Bcancellation.lcm(event):
                        self._Bcancellation.efects()
                        self._Bcancellation.stop()
                        self.main.close()
        
        def update(self):
            if self.options.activ:
                self._Bfurther.update()
            self._Bback.update()
            self._Bcancellation.update()
            self.list.update()
            self.options.update()

        def draw(self, screen: pg.Surface):
            super().draw(screen)
            self._Bfurther.draw(screen)
            self._Bback.draw(screen)
            self._Bcancellation.draw(screen)
            screen.blit(self.holst, self.list.left_top.pixel)
            self.list.draw(screen)
            screen.blit(self.license, (20, 15))
            screen.blit(self.license_info, (40, 34))
            self.options.draw(screen)

    return EULA


def ChoosingPath(len_byts=1024):
    r"""
    3.
    
    Выбор пути установки
    Поле с путём по умолчанию (C:\Program Files\ИмяПрограммы)
    Кнопка "Обзор" для смены пути
    Показ требуемого/доступного места на диске
    """


    class ChoosingPath(InstallerScene):
        threading_activ = False

        def init(self):
            super().init()
            self._Bcancellation= _create_gray_button(self.get_translation()["cancellation"], (self.main.size[0]-90, 15+332), self.get_tema()["text"])
            self._Bfurther = _create_blue_button(self.get_translation()["further"], (self._Bcancellation.x-90, 15+332), self.get_tema()["text"])
            self._Bback = _create_gray_button(self.get_translation()["back"], (self._Bfurther.x-80, 15+332), self.get_tema()["text"])
            self._Breview = _create_gray_button(self.get_translation()["review"], (40, 100), self.get_tema()["text"])

            self.path = pg.font.Font(r"C:\Windows\Fonts\Arialbd.ttf", 14).render(self.get_translation()["path"], True, self.get_tema()["text"])
            self.path_info = pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12).render(self.get_translation()["path_info"].format(name=self.main.name), True, self.get_tema()["text"])
            self.path_agree = _render(self.get_translation()["path_agree"], pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12), 450, color=self.get_tema()["text"])
            self.path_size = _render(self.get_translation()["path_size"].format(**dict(zip(["size", "byts"], format_size(len_byts, self.get_translation()["units"], self.get_translation()["byte"])))), pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12), 450, color=self.get_tema()["text"])
            
            
            fon = pg.Surface((430, 20), pg.SRCALPHA)
            fon.fill(self.get_tema()["fin_further"])
            pg.draw.rect(fon, (200, 200, 200), fon.get_rect(), 1)
            self.line = InputLine((40, 70), fon, self.main.path, font=pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 14), color=self.get_tema()["text"])

        def event(self, event):
                    self._Bfurther.event(event)
                    self._Bback.event(event)
                    self._Bcancellation.event(event)
                    self._Breview.event(event)
                    try:
                        self.line.event(event)
                    except TypeError:
                        pass

                    if self._Bback.lcm(event):
                        self._Bback.efects()
                        self._Bback.stop()
                        self.main.condition -= 1
                    elif self._Bfurther.lcm(event):
                        self._Bfurther.efects()
                        self._Bfurther.stop()
                        if os.path.isdir(self.main.path) and not self.threading_activ:
                            self.main.condition += 1
                    elif self._Bcancellation.lcm(event):
                        self._Bcancellation.efects()
                        self._Bcancellation.stop()
                        self.main.close()
                    elif self._Breview.lcm(event):
                        if not self.threading_activ:
                            threading.Thread(target=self._path, daemon=True).start()
        
        def update(self):
            self._Bfurther.update()
            self._Bback.update()
            self._Bcancellation.update()
            self.line.update()
            self._Breview.update()

        def draw(self, screen: pg.Surface):
            super().draw(screen)
            self._Bfurther.draw(screen)
            self._Bback.draw(screen)
            self._Bcancellation.draw(screen)
            self._Breview.draw(screen)
            self.line.draw(screen)

            if self.line.active:
                pg.draw.line(screen, self.get_tema()["line"], (self.line.left, self.line.top+17), (self.line.left+430, self.line.top+17), 3)

            screen.blit(self.path, (20, 15))
            screen.blit(self.path_info, (40, 34))
            screen.blit(self.path_agree, (40, 130))
            screen.blit(self.path_size, (40, 332-self.path_size.get_height()))

        def _path(self):
            try:
                path = select_folder()
                if not path is None:
                    self.line.text = self.main.path = path
            except: ...
            self.threading_activ = False
        
    return ChoosingPath


def AdditionalOptions(options: list[_Options]):
    """
    4.

    Дополнительные опции (если нужно)
    Создать ярлык на рабочем столе
    Добавить в автозагрузку
    Выбор компонентов (для модульных программ)
    
    """
    class AdditionalOptions(InstallerScene):
        def init(self):
            super().init()
            self.main.options = options
            self._Bcancellation= _create_gray_button(self.get_translation()["cancellation"], (self.main.size[0]-90, 15+332), self.get_tema()["text"])
            self._Bfurther = _create_blue_button(self.get_translation()["further"], (self._Bcancellation.x-90, 15+332), self.get_tema()["text"])
            self._Bback = _create_gray_button(self.get_translation()["back"], (self._Bfurther.x-80, 15+332), self.get_tema()["text"])
                    
            self.additionally = pg.font.Font(r"C:\Windows\Fonts\Arialbd.ttf", 14).render(self.get_translation()["additionally"], True, self.get_tema()["text"])
            self.additionally_info = pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12).render(self.get_translation()["additionally_info"].format(name=self.main.name), True, self.get_tema()["text"])
            self.additionally_agree = _render(self.get_translation()["additionally_agree"].format(name=self.main.name), pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12), 450, color=self.get_tema()["text"])
            self.additionally_options = pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12).render(self.get_translation()["additionally_options"].format(name=self.main.name), True, self.get_tema()["text"])

            self.options: list[_Options] = options
            for i, option in enumerate(options):
                option.buton.x = 50
                option.buton.y = 140+(20*i)

            
        def event(self, event):
            self._Bfurther.event(event)
            self._Bback.event(event)
            self._Bcancellation.event(event)

            for option in self.options:
                option.event(event)
            
            if self._Bback.lcm(event):
                self._Bback.efects()
                self._Bback.stop()
                self.main.condition -= 1
            elif self._Bfurther.lcm(event):
                self._Bfurther.efects()
                self._Bfurther.stop()
                self.main.condition += 1
            elif self._Bcancellation.lcm(event):
                self._Bcancellation.efects()
                self._Bcancellation.stop()
                self.main.close()
                
        def update(self):
            self._Bfurther.update()
            self._Bback.update()
            self._Bcancellation.update()

            for option in self.options:
                option.update()
                    
        
        def draw(self, screen: pg.Surface):
            super().draw(screen)
            self._Bfurther.draw(screen)
            self._Bback.draw(screen)
            self._Bcancellation.draw(screen)
        
            screen.blit(self.additionally, (20, 15))
            screen.blit(self.additionally_info, (40, 34))
            screen.blit(self.additionally_agree, (40, 70))
            screen.blit(self.additionally_options, (40, 120))

            for option in self.options:
                option.draw(screen)
    
    return AdditionalOptions


def Confirmation():
    """
    5.

    Подтверждение / Готово к установке
    Сводка выбранных параметров
    Кнопка «Установить»
    """
    class Confirmation(InstallerScene):
        def init(self):
            super().init()
            self._Bcancellation= _create_gray_button(self.get_translation()["cancellation"], (self.main.size[0]-90, 15+332), self.get_tema()["text"])
            self._Bfurther = _create_blue_button(self.get_translation()["install"], (self._Bcancellation.x-90, 15+332), self.get_tema()["text"])
            self._Bback = _create_gray_button(self.get_translation()["back"], (self._Bfurther.x-80, 15+332), self.get_tema()["text"])
                    
            self.done = pg.font.Font(r"C:\Windows\Fonts\Arialbd.ttf", 14).render(self.get_translation()["done"], True, self.get_tema()["text"])
            self.done_info = pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12).render(self.get_translation()["done_info"].format(name=self.main.name), True, self.get_tema()["text"])
            self.done_agree = _render(self.get_translation()["done_agree"].format(name=self.main.name), pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12), 450, color=self.get_tema()["text"])
            
        def event(self, event):
            self._Bfurther.event(event)
            self._Bback.event(event)
            self._Bcancellation.event(event)

            
            if self._Bback.lcm(event):
                self._Bback.efects()
                self._Bback.stop()
                self.main.condition -= 1
            elif self._Bfurther.lcm(event):
                self._Bfurther.efects()
                self._Bfurther.stop()
                self.main.condition += 1
            elif self._Bcancellation.lcm(event):
                self._Bcancellation.efects()
                self._Bcancellation.stop()
                self.main.close()          
                
        def update(self):
            self._Bfurther.update()
            self._Bback.update()
            self._Bcancellation.update()
        
        def draw(self, screen: pg.Surface):
            super().draw(screen)
            self._Bfurther.draw(screen)
            self._Bback.draw(screen)
            self._Bcancellation.draw(screen)
        
            screen.blit(self.done, (20, 15))
            screen.blit(self.done_info, (40, 34))
            screen.blit(self.done_agree, (40, 70))

    return Confirmation


def InstallationProcess(install: ModelInstall):
    """
    6.

    Процесс установки
    Индикатор выполнения
    Текущее действие ("Копирование файлов...", "Настройка...")
    Возможность отмены
    """
    class InstallationProcess(InstallerScene):
        _is = True
        def update_fun(self, p):
            self.progress.set_percent(p)

        def init(self):
            super().init()
            self._Bcancellation= _create_blue_button(self.get_translation()["cancellation"], (self.main.size[0]-90, 15+332), self.get_tema()["text"])
                    
            self.installation = pg.font.Font(r"C:\Windows\Fonts\Arialbd.ttf", 14).render(self.get_translation()["installation"], True, self.get_tema()["text"])
            self.installation_info = pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12).render(self.get_translation()["installation_info"].format(name=self.main.name), True, self.get_tema()["text"])
            self.installation_agree = _render(self.get_translation()["installation_agree-install"].format(name=self.main.name), pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12), 450, color=self.get_tema()["text"])

            self.progress = ProgressBar((40, 120), (410, 20), (14, 181, 42))
            self.progress_fon = pg.Surface(self.progress.width_height, pg.SRCALPHA)
            pg.draw.rect(self.progress_fon, (200, 200, 200), self.progress_fon.get_rect(), 1)
            
        def event(self, event):
            self._Bcancellation.event(event)
            if self._Bcancellation.lcm(event):
                self._Bcancellation.efects()
                self._Bcancellation.stop()
                self.main.close()          
            
        def update(self):
            if self._is:
                install.install_threading(self.update_fun, self.main.path)
                self._is = False
            self._Bcancellation.update()
            self.progress.update()

            if self.progress.get_percent() >= 100:
                self.main.condition += 1
                for i in self.main.options:
                    i.start(self.main)

        def draw(self, screen: pg.Surface):
            super().draw(screen)
            self._Bcancellation.draw(screen)

            self.progress.draw(screen)
            screen.blit(self.progress_fon, self.progress.left_top)

            screen.blit(self.installation, (20, 15))
            screen.blit(self.installation_info, (40, 34))
            screen.blit(self.installation_agree, (40, 70))

    return InstallationProcess


def FinalScreen(start=True):
    """
    7.

    Финальный экран
    "Установка завершена"
    Чекбокс "Запустить программу сейчас"
    Кнопка "Готово"
    """
    class FinalScreen(InstallerScene):
        def init(self):
            super().init()
            
            if start:
                def option(activ):
                    self._activ = activ
                self.options = _Options((40, 290), self.get_translation()["completion-icon"].format(name=self.main.name), lambda: None)
                self.options.set_switch(option)
            self._Bfurther = _create_blue_button(self.get_translation()["complete"], (self.main.size[0]-180, 15+332), self.get_tema()["text"])
                    
            self.completion = pg.font.Font(r"C:\Windows\Fonts\Arialbd.ttf", 14).render(self.get_translation()["completion"].format(name=self.main.name), True, self.get_tema()["text"])
            self.completion_info = pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12).render(self.get_translation()["completion_info"].format(name=self.main.name), True, self.get_tema()["text"])
            self.completion_agree = _render(self.get_translation()["completion_agree"].format(name=self.main.name), pg.font.Font(r"C:\Windows\Fonts\Arial.ttf", 12), 450, color=self.get_tema()["text"])
                    
        def event(self, event):
            self._Bfurther.event(event)
            if start:
                self.options.event(event)

            if self._Bfurther.lcm(event):
                self._Bfurther.efects()
                self._Bfurther.stop()
                if start:
                    if self._activ:
                        work_dir = os.path.join(self.main.path, self.main.name)  # папка с exe
                        exe_path = os.path.join(work_dir, self.main.name + ".exe")
                        threading.Thread(target=subprocess.run, args=(f'cd /d "{work_dir}" && "{exe_path}"', ), kwargs={"shell": True}).start()
                        #subprocess.run( f'cd /d "{work_dir}" && "{exe_path}"', shell=True)
                self.main.close()        
                        
        def update(self):
            self._Bfurther.update()
            if start:
                self.options.update()
        def draw(self, screen: pg.Surface):
            super().draw(screen)
            self._Bfurther.draw(screen)
            screen.blit(self.completion, (20, 15))
            screen.blit(self.completion_info, (40, 34))
            screen.blit(self.completion_agree, (40, 70))
            if start:
                self.options.draw(screen)

    return FinalScreen

class _Installer(Window):
    def __init__(self, name, img, path, size=(500, 380), color=(30, 30, 30), scene = None, *, fps=60, flags=0, zi_set_mode=[]):
        super().__init__(size, color, scene, fps=fps, flags=flags, zi_set_mode=zi_set_mode)
        self.name = name
        self.img = img
        self.path = path

    def init(self, win):
        self.set_caption(f"Installation - {self.name}")
        self.set_icon(self.img)
        for sc in self._scene:
            sc._set_main(self)
            sc.init()

def run(name: str,img, scene: list[InstallerScene], path: str = r"C:\Program Files"):
    install = _Installer(name, img, path, scene=scene, color=TEMA[get_TEMA()]["fon"])
    install.start()
    install.join()

