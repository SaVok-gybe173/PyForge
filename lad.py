from dataclasses import dataclass
from typing import List, Callable
from .textures import getAppTexture, Texture, TypeTexture, _AppTexture, newAppTexture, makeSheet
import pygame as pg
import zlib

COMANDS = {} # 4 байтa
NAME_COMANDS = {}
COMPRESSIONS = {(0).to_bytes(1): lambda data: zlib.compress(data, 0), # сжатие
                (1).to_bytes(1): lambda data: zlib.compress(data, 1),
                (2).to_bytes(1): lambda data: zlib.compress(data, 2),
                (3).to_bytes(1): lambda data: zlib.compress(data, 3),
                (4).to_bytes(1): lambda data: zlib.compress(data, 4),
                (5).to_bytes(1): lambda data: zlib.compress(data, 5),
                (6).to_bytes(1): lambda data: zlib.compress(data, 6),
                (7).to_bytes(1): lambda data: zlib.compress(data, 7),
                (8).to_bytes(1): lambda data: zlib.compress(data, 8),
                (9).to_bytes(1): lambda data: zlib.compress(data, 9),}

DECOMPRESS = {(0).to_bytes(1): zlib.decompress, # расжатие
              (1).to_bytes(1): zlib.decompress,
              (2).to_bytes(1): zlib.decompress,
              (3).to_bytes(1): zlib.decompress,
              (4).to_bytes(1): zlib.decompress,
              (5).to_bytes(1): zlib.decompress,
              (6).to_bytes(1): zlib.decompress,
              (7).to_bytes(1): zlib.decompress,
              (8).to_bytes(1): zlib.decompress,
              (9).to_bytes(1): zlib.decompress}

def addComand(name: str, byte: bytes, fun: Callable):
    """
    Добавление своей команды
    """
    if len(byte) > 4:
        raise ValueError("длина \"byte\" должна быть 4 байта")
    elif len(byte) < 4:
        byte = b'\x00'*(4-len(byte))+byte
    NAME_COMANDS[name] = byte
    COMANDS[byte] = fun


@dataclass
class tile:
    name: bytes # команда 4 байта
    cells: List[bytes] # длина 8 байт

@dataclass
class lad:
    name: str # 3 байта
    compression: int # 1 байт

    comands: List[tile]

def savebytes(lads: lad) -> bytes:
    """
    длает из структуры в байты
    """
    data = lads.name.encode('ascii')
    data += lads.compression.to_bytes(length=1, byteorder='big')
    data_compress = b""

    for com in lads.comands:
        data_compress += com.name

        data_compress += len(com.cells).to_bytes(4)

        for cell in com.cells:
            data_compress += len(cell).to_bytes(8)
            data_compress += cell

    data += COMPRESSIONS[lads.compression.to_bytes(length=1, byteorder='big')](data_compress)
    return data

def save(lads: lad, file: str) -> None:
    """
    сохраняет в фаил
    """
    with open(file, "w+b") as f:
        f.write(savebytes(lads))

def loadbytes(byte: bytes) -> lad:
    """
    делает из байтов в структуру
    """
    data = lad(byte[0:3], int.from_bytes(byte[3:4]), [])
    comands = DECOMPRESS[data.compression.to_bytes(length=1, byteorder='big')](byte[4:])

    while True:
        if len(comands) <= 8:
            break

        till = tile(comands[:4], [])
        lens = int.from_bytes(comands[4:8])
        comands = comands[8:]

        for _ in range(lens):
            lens = int.from_bytes(comands[:8])
            comands = comands[8:]

            till.cells.append(comands[:lens])
            comands = comands[lens:]

        data.comands.append(till)
    return data

def load(file: str) -> lad:
    """
    Загружает из файла и делает структуру
    """
    with open(file, "r+b") as f:
        return loadbytes(f.read())

def start(lads: lad):
    """
    запуск команд
    """
    for cmd in lads.comands:
        COMANDS[cmd.name](*cmd.cells)


#команды текстур
addComand("appTexture", (0).to_bytes(4), (lambda _: newAppTexture(None if b'*' == _ else _.decode())))
addComand("addTextureSur", b"\x01", (lambda path, sur_byte, width, height: getAppTexture().add(path.decode(), pg.image.fromstring(sur_byte, (int.from_bytes(width), int.from_bytes(height)), 'RGBA'))))

def createTextureSur(surface: pg.Surface, path: str):
    return tile(NAME_COMANDS["addTextureSur"], [path.encode(), pg.image.tostring(surface, 'RGBA'), int.to_bytes(surface.get_width(), 2), int.to_bytes(surface.get_height(), 2)])
def createAppTexture(file: str|None = None):
    return tile(NAME_COMANDS["appTexture"], [b"*" if file is None else file.encode()])

def createTexture(testur: Texture):
    """
    создает список команд из текстур
    """
    f: list[tile] = []
    for k, i in makeSheet(testur).items():
        if type(i) is pg.Surface:
            f.append(createTextureSur(i, k))
    return f

