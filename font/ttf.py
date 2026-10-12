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
│  Table Record #(numTables-1)  (16 байт)     │
├─────────────────────────────────────────────┤  байт 0x000C + 16 * numTables
│                                             │
│  Тело таблицы №0 (например, 'DSIG')         │  <- здесь лежит таблица DSIG
│  ...padding до кратности 4 байтам...        │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│  Тело таблицы №1 (например, 'GDEF')         │  <- здесь лежит таблица GDEF
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│  Тело таблицы №2 (например, 'GPOS')         │  <- здесь лежит таблица GPOS
│                                             │
├─────────────────────────────────────────────┤
│  ... остальные таблицы ...                  │  конец файла
└─────────────────────────────────────────────┘  

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
from dataclasses import dataclass
from math import ceil


def round_up(x, to = 4):
    return ceil(x / to) * to

@dataclass
class FontDirectory:
    tag: str        # 4 байта, 4 символа ASCII
    checkSum: int   # 4 байта, uint32
    offset: int     # 4 байта, uint32
    length: int     # 4 байта, uint32
    tabl = None 


@dataclass
class head:
    """
    Смещение в head	Размер	Тип	    Имя
    0x00	        4	    uint32	version
    0x04	        4	    uint32	fontRevision
    0x08	        4	    uint32	checkSumAdjustment
    0x0C	        4	    uint32	magicNumber
    0x10	        2	    uint16	flags
    0x12	        2	    uint16	unitsPerEm
    0x14	        8	    int64	created
    0x1C	        8	    int64	modified
    0x24	        2	    int16	xMin
    0x26	        2	    int16	yMin
    0x28	        2	    int16	xMax
    0x2A	        2	    int16	yMax
    0x2C	        2	    uint16	macStyle
    0x2E	        2	    uint16	lowestRecPPEM
    0x30	        2	    int16	fontDirectionHint
    0x32	        2	    int16	indexToLocFormat
    0x34	        2	    int16	glyphDataFormat
    """
    version: int            # 0x00010000
    fontRevision: int       # 0x00010000
    checkSumAdjustment: int
    magicNumber: int        # 0x5F0F3CF5
    flags: int
    unitsPerEm: int         # 1024 или 2048 (иногда 1000, 2000)
    created: int
    modified: int
    modified: int
    xMin: int
    yMin: int
    xMax: int
    yMax: int
    macStyle: int
    lowestRecPPEM: int
    fontDirectionHint: int
    indexToLocFormat: int   # 0 или 1
    glyphDataFormat: int    # 0

class Font(CoreObject):
    file: str | None = None

    sfntVersion: int = 0x00010000   # 0x00010000 — TrueType, 'OTTO' — CFF/OpenType
    numTables: int                  # Сколько таблиц в файле
    searchRange: int                # 2^floor(log2(numTables)) × 16
    entrySelector: int              # log2(searchRange / 16)
    rangeShift: int                 # numTables × 16 − searchRange

    tableRecord: dict[FontDirectory]        # 16*numTables

    def __init__(self, file: str | None = None):
        if file: self.load(file)

    def load(self, file: str):
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
        tableRecord: list[bytes] = [cesh[i:i + 16] for i in range(0, len(cesh), 16)]
        tableRecord: list[FontDirectory] = [FontDirectory(i[:0x04].decode('ASCII'), int.from_bytes(i[0x04:0x08]), int.from_bytes(i[0x08:0x0C]), int.from_bytes(i[0x0C:0x0C+4])) for i in tableRecord]
        self.tableRecord = {i.tag: i for i in tableRecord}

        if "head" in self.tableRecord:
            heads: FontDirectory = self.tableRecord["head"]
            offset = round_up(heads.offset)
            datahead = data[offset : offset+heads.length]
            heads.tabl = head(
                int.from_bytes(datahead[0x00 : 0x04]),
                int.from_bytes(datahead[0x04 : 0x08]),
                int.from_bytes(datahead[0x08 : 0x0C]),
                int.from_bytes(datahead[0x0C : 0x10]),
                int.from_bytes(datahead[0x10 : 0x12]),
                int.from_bytes(datahead[0x12 : 0x14]),
                int.from_bytes(datahead[0x14 : 0x1C], signed=True),
                int.from_bytes(datahead[0x1C : 0x24], signed=True),
                int.from_bytes(datahead[0x24 : 0x26], signed=True),
                int.from_bytes(datahead[0x26 : 0x28], signed=True),
                int.from_bytes(datahead[0x28 : 0x2A], signed=True),
                int.from_bytes(datahead[0x2A : 0x2C], signed=True),
                int.from_bytes(datahead[0x2C : 0x2E]),
                int.from_bytes(datahead[0x2E : 0x30]),
                int.from_bytes(datahead[0x30 : 0x32], signed=True),
                int.from_bytes(datahead[0x32 : 0x34], signed=True),
                int.from_bytes(datahead[0x34 : 0x36], signed=True),
            )
        
        self.file = file

if __name__ == "__main__":
    #print(int.from_bytes((0xFF).to_bytes()))
    f = Font("minecraft.ttf")
    print(f.sfntVersion, f.numTables, f.searchRange, f.entrySelector, f.rangeShift)
    
    print(f.tableRecord["head"].tabl)
