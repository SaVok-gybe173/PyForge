"""
Не доступно на android и ios

Модуль для создание дополнительныйх окон pygame

Вксь код прописываем в классе. Дальше вызываем start
Также в коде не должны вызываться глобальные обьекты или значения. Так как процесс создаеться с новой помятью и у него нету доступа к памяти старого процесса.
Используйте multiprocessing.Queue

Пример:
from multiprocessing import Process, Queue
def worked(q):
    q.put(\"Послание из процесса\")

q = Queue()
p = Process(target=worked, args=(q,))
p.start()
print(q.get())
p.join()

Можно передовать list и так далее, но лучше использовать свою структуру и не передовать кастомные классы
Используйте json и сами создавайте обьекты
"""
from .window import Window as _window
from ..logger import printError, printInfo
from multiprocessing import Process
from typing import overload

import os

#работает с pygame v2.0
class Window(_window):
    name = None
    daemon = False

    def start(self) -> None:
        """
        Запуск нового окна
        """
        
        if self.process is None or not self.process.is_alive():
            self.process = Process(target=self.run_window, name=self.name, daemon=self.daemon)
            try:
                self.process.start()
            except Exception as e:
                printError("Ошибка создания новго окна >", e)
                raise e
        else:
            printInfo("Новое окно не было создано так как процесс уже запущен >", self.process)

    def is_alive(self) -> bool:
        """
        Проверка на работу процесса/окна

        Return:
            Возвращает bool значения активности окна
        """
        if self.process is None:
            return False
        else:
            return self.process.is_alive()

    @overload
    def join(self):
        """
        Ожидает завершение программы, 
        """

    @overload
    def join(self, timeout: float | int) -> None:
        """
        Завершает процесс окна через время, если оно и так закрыто то ничего не происходит
        
        Args:
            timeout (float | int): Время через сколько сек остоновить процесс
        """
        
    def join(self, timeout: float | int | None = None):
        if self.process is not None:
            self.process.join()
    def kill(self):
        try:
            super().kill()
        except Exception as e:
            print("[ERROR] [KILL]", e)
        self.process.kill()
            
if __name__ == '__main__':
    import multiprocessing, sys
    multiprocessing.freeze_support()
    
    if getattr(sys, 'frozen', False):
        os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']
    
    # Создаем два окна с разными параметрами
    window1 = Window(color=(220, 110, 70))
    window2 = Window()

    window1.start()
    window2.start()

    window1.join()
    window2.join()