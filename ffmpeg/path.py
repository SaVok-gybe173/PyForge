from ..easel.platform import is_window
from ..logger import printLog

import os
import subprocess
import shutil

def check_ffmpeg() -> bool:
    "Проверяет ffmpeg глобально"
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path is not None:
        return True
    else:
        return False

# Альтернативный способ с запуском
def check_ffmpeg_version():
    "Проверяет ffmpeg локально"
    try:
        result = subprocess.run([get_ffmpeg(), '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return False
    except subprocess.TimeoutExpired:
        return False


if is_window():
    ffprobe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "ffprobe.exe")
    ffmpeg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "ffmpeg.exe")
    ffplay = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "ffplay.exe")
else:
    if check_ffmpeg():
        ffprobe = "ffprobe"
        ffmpeg = "ffmpeg"
        ffplay = "ffplay"
    else:
        ...

# сеттеры и геттеры возвращают ключи
def get_ffprobe() -> str:
    global ffprobe
    return ffprobe

def get_ffmpeg() -> str:
    global ffmpeg
    return ffmpeg

def get_ffplay() -> str:
    global ffplay
    return ffplay

def set_ffprobe(_ffprobe) -> None:
    global ffprobe
    ffprobe = _ffprobe

def set_ffmpeg(_ffmpeg: str) -> None:
    global ffmpeg
    ffmpeg = _ffmpeg

def set_ffplay(_ffplay: str) -> None:
    global ffplay
    ffplay = _ffplay

if check_ffmpeg_version():
    printLog("Не найден ffmpeg для обработки видео и аудио")

print(get_ffmpeg())