"""
TTF — это конкатенация таблиц в одном бинарном файле. 
Файл начинается с Font Directory — «оглавления», 
которое говорит: сколько таблиц, как они называются, где лежат и какого размера. 
Дальше идут сами таблицы в произвольном порядке.

Все многобайтовые числа — big-endian (старший байт первый). 
Все смещения — от начала файла.

Таблицы выравниваются на 4 байта: если длина таблицы не кратна 4, она дополняется нулями.

┌─────────────────────────────────────────────┐  байт 0x0000
│  Font Directory Header (12 байт)            │
│    sfntVersion, numTables, ...              │
├─────────────────────────────────────────────┤  байт 0x000C
│  Table Record #0   (16 байт)                │
│  Table Record #1   (16 байт)                │
│  Table Record #2   (16 байт)                │
│  ...                                        │
│  Table Record #(numTables-1)  (16 байт)     │
├─────────────────────────────────────────────┤  байт 0x000C + 16 * numTables
│                                             │
│  Тело таблицы №0 (например, 'DSIG')         │  ← здесь лежит таблица DSIG
│  ...padding до кратности 4 байтам...        │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│  Тело таблицы №1 (например, 'GDEF')         │  ← здесь лежит таблица GDEF
│  ...                                        │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│  Тело таблицы №2 (например, 'GPOS')         │  ← здесь лежит таблица GPOS
│                                             │
├─────────────────────────────────────────────┤
│  ...                                        │
│  ... остальные таблицы ...                  │
│  ...                                        │
└─────────────────────────────────────────────┘  конец файла

Первые 12 байт файла — это заголовок Font Directory
Байт 0x00 : 0x04   ->  sfntVersion  (4 байта)
Байт 0x04 : 0x06   ->  numTables    (2 байта)
Байт 0x06 : 0x08   ->  searchRange  (2 байта)
Байт 0x08 : 0x0A   ->  entrySelector(2 байта)
Байт 0x0A : 0x0C   ->  rangeShift   (2 байта)

Сразу после него (с байта 0x0C) начинается массив записей о таблицах. Каждая запись ровно 16 байт.
Байт 0x0C : 0x1B   ->  запись таблицы №0   (16 байт)
Байт 0x1C : 0x2B   ->  запись таблицы №1   (16 байт)
Байт 0x2C : 0x3B   ->  запись таблицы №2   (16 байт)

Байт 0x0C + 16*i ..  ->  запись таблицы №i

"""

from PyForge.easel import CoreObject

class Font(CoreObject):
    file: str | None = None

    sfntVersion: int = 0x00010000   # 0x00010000 — TrueType, 'OTTO' — CFF/OpenType
    numTables: int                  # Сколько таблиц в файле
    searchRange: int                # 2^floor(log2(numTables)) × 16
    entrySelector: int              # log2(searchRange / 16)
    rangeShift: int                 # numTables × 16 − searchRange

    tableRecord: list[bytes]        # 16*numTables

    def __init__(self, file: str | None = None):
        if file: self.load(file)

    def load(self, file):
        with open(file, 'r+b') as f:
            data = f.read()
        
        # 0x0000 : 0x000C
        self.sfntVersion =      int.from_bytes(data[0x00 : 0x04])
        self.numTables =        int.from_bytes(data[0x04 : 0x06])
        self.searchRange =      int.from_bytes(data[0x06 : 0x08])
        self.entrySelector =    int.from_bytes(data[0x08 : 0x0A])
        self.rangeShift =       int.from_bytes(data[0x0A : 0x0C])

        # 0x000C : 0x000C + 16*numTables
        cesh = data[0x000C : 0x000C + 16*self.numTables]
        self.tableRecord = [cesh[i:i + 16] for i in range(0, len(cesh), 16)]
        
            
        
        self.file = file

if __name__ == "__main__":
    f = Font("minecraft.ttf")
    print(f.sfntVersion, f.numTables, f.searchRange, f.entrySelector, f.rangeShift)