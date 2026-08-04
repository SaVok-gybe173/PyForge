from ..googl_downloads import install as googl_install
from ..yandex_downloads import install as yandex_install
import threading
from ..arh import unzip_archive

class ModelInstall:
    _threading: threading.Thread | None = None

    def __init__(self, url, destination_path: str = 'downloaded_file.zip',):
        self.url = url
        self.destination_path = destination_path

    def install_threading(self, fun, path = '.'):
        self._threading = threading.Thread(target=self.install, args=(fun, path), daemon=True)
        self._threading.start()

    def join(self, timeout: float | None = None) -> None:
        self._threading.join(timeout)
    
    def install(self, fun):
        pass

class GooglInstall(ModelInstall):
    def install(self, fun, path = '.'):
        googl_install(self.url, self.destination_path, lambda _: fun(_-2 if _==100 else _))
        unzip_archive(self.destination_path, path)
        fun(100)

class YandexInstall(ModelInstall):
    def install(self, fun, path = '.'):
        googl_install(self.url, self.destination_path, lambda _: fun(_-2 if _==100 else _))
        unzip_archive(self.destination_path, path)
        fun(100)
        
