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

    @staticmethod
    def _from(datahead: bytes) -> "head":
        """
        head — заголовок шрифта
        Зачем нужна: хранит глобальные параметры шрифта. Без неё не понять, в каких единицах заданы координаты и как читать другие таблицы.

        Что внутри:
            unitsPerEm — система координат (1024 или 2048 обычно).
            indexToLocFormat — короткий или длинный формат loca.
            magicNumber — маркер, что это действительно head (0x5F0F3CF5).
            Даты создания/изменения.
            Bounding box всего шрифта.
            Флаги стиля (bold, italic).

        Кто использует: 
            парсер берёт unitsPerEm для масштабирования координат и indexToLocFormat для чтения loca
        """
        return head(
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

class maxp:
    """
    Смещение    Размер	Тип	    Имя
    0x00	    4	    Fixed	version
    0x04	    2	    uint16	numGlyphs
    0x06	    2	    uint16	maxPoints
    0x08	    2	    uint16	maxContours
    0x0A	    2	    uint16	maxCompositePoints
    0x0C	    2	    uint16	maxCompositeContours
    0x0E	    2	    uint16	maxZones
    0x10	    2	    uint16	maxTwilightPoints
    0x12	    2	    uint16	maxStorage
    0x14	    2	    uint16	maxFunctionDefs
    0x16	    2	    uint16	maxInstructionDefs
    0x18	    2	    uint16	maxStackElements
    0x1A	    2	    uint16	maxSizeOfInstructions
    0x1C	    2	    uint16	maxComponentElements
    0x1E	    2	    uint16	maxComponentDepth

    """

    version: int
    numGlyphs: int
    maxPoints: int
    maxContours: int
    maxCompositePoints: int
    maxCompositeContours: int
    maxZones: int
    maxTwilightPoints: int
    maxStorage: int
    maxFunctionDefs: int
    maxInstructionDefs: int
    maxStackElements: int
    maxSizeOfInstructions: int
    maxComponentElements: int
    maxComponentDepth: int

    @staticmethod
    def _from(datamaxp: bytes) -> "maxp":
        """
        maxp — максимумы
        
        Зачем нужна: 
            содержит numGlyphs — сколько всего глифов в шрифте. Без этого не понять, какой длины массивы в loca и hmtx.

        Что внутри:
            numGlyphs — ключевое поле.
            Различные максимумы (maxPoints, maxContours, maxStackElements) — нужны для хинтинга.

        Кто использует: 
            парсер — чтобы знать размер loca (numGlyphs + 1 записей). Рендер — чтобы понимать границы допустимых glyph_id.
        """
        return maxp(
            int.from_bytes(datamaxp[0x00 : 0x04]),
            int.from_bytes(datamaxp[0x04 : 0x06]),
            int.from_bytes(datamaxp[0x06 : 0x08]),
            int.from_bytes(datamaxp[0x08 : 0x0A]),
            int.from_bytes(datamaxp[0x0A : 0x0C]),
            int.from_bytes(datamaxp[0x0C : 0x0E]),
            int.from_bytes(datamaxp[0x0E : 0x10]),
            int.from_bytes(datamaxp[0x10 : 0x12]),
            int.from_bytes(datamaxp[0x12 : 0x14]),
            int.from_bytes(datamaxp[0x14 : 0x16]),
            int.from_bytes(datamaxp[0x16 : 0x18]),
            int.from_bytes(datamaxp[0x18 : 0x1A]),
            int.from_bytes(datamaxp[0x1A : 0x1C]),
            int.from_bytes(datamaxp[0x1C : 0x1E]),
            int.from_bytes(datamaxp[0x1E : 0x20]),
        )

class Font(CoreObject):
    # таблица
    _head: head | None = None
    _maxp: maxp | None = None

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
            self._head = head._from(data[heads.offset : heads.offset+heads.length])

        if "maxp" in self.tableRecord:
            maxps: FontDirectory = self.tableRecord["head"]
            self._maxp = head._from(data[maxps.offset : maxps.offset+maxps.length])
        
        self.file = file

if __name__ == "__main__":
    #print(int.from_bytes((0xFF).to_bytes()))
    f = Font("minecraft.ttf")
    print(f.sfntVersion, f.numTables, f.searchRange, f.entrySelector, f.rangeShift)
    
    print(f.tableRecord["head"].tabl)
