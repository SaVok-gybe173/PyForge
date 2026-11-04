"""
Ниже dataclasses для всех таблиц, которые нужны для рендера. 
Каждое поле снабжено комментарием: что это и зачем оно. 
В конце - зачем вообще нужен сам файл шрифта.

"""

from dataclasses import dataclass

@dataclass
class FontDirectory:
    tag: str        # 4 байта, 4 символа ASCII
    checkSum: int   # 4 байта, uint32
    offset: int     # 4 байта, uint32
    length: int     # 4 байта, uint32

@dataclass
class head: # заголовок шрифта
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
    def _from(datahead: bytes) -> head:
        """
        Зачем нужна: 
            хранит глобальные параметры шрифта. Без неё не понять, в каких единицах заданы координаты и как читать другие таблицы.

        Что внутри:
            unitsPerEm - система координат (1024 или 2048 обычно).
            indexToLocFormat - короткий или длинный формат loca.
            magicNumber - маркер, что это действительно head (0x5F0F3CF5).
            Даты создания/изменения.
            Bounding box всего шрифта.
            Флаги стиля (bold, italic).

        Кто использует: 
            парсер берёт unitsPerEm для масштабирования координат и indexToLocFormat для чтения loca
        """

    def _to(self) -> bytes: ...

@dataclass
class maxp: # максимумы
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
    def _from(datamaxp: bytes) -> maxp:
        """
        Зачем нужна: 
            содержит numGlyphs - сколько всего глифов в шрифте. Без этого не понять, какой длины массивы в loca и hmtx.
        Что внутри:
            numGlyphs - ключевое поле.
            Различные максимумы (maxPoints, maxContours, maxStackElements) - нужны для хинтинга.
        Кто использует: 
            парсер - чтобы знать размер loca (numGlyphs + 1 записей). Рендер - чтобы понимать границы допустимых glyph_id.
        """

@dataclass
class loca: # индекс местоположений глифов
    """
    Смещение в loca	Размер	Тип	Имя
    2*i (короткий)	2	uint16	offset[i], реальное = значение * 2
    4*i (длинный)	4	uint32	offset[i], реальное = значение
    Длина массива - numGlyphs + 1 элементов.
    """

    offsets: list[int]

    @staticmethod
    def _from(data: bytes, num_glyphs: int, index_to_loc_format: int) -> loca:
        """
        Зачем нужна: 
            говорит, где именно в таблице glyf лежит каждый глиф. 
            Без неё glyf - просто куча байт, в которой не найти нужный глиф.

        Что внутри: 
            массив из numGlyphs + 1 смещений. 
            Границы глифа glyph_id - это loca[glyph_id] и loca[glyph_id + 1] (относительно начала glyf).
        
        Кто использует: 
            рендер - чтобы вырезать байты конкретного глифа.
        """

class glyph:
    
    """
    Границы глифа берутся из loca: глиф №i занимает байты [loca[i], loca[i+1]) от начала glyf.

    Заголовок глифа (10 байт):

    Смещение    Размер	Тип	    Имя
    0x00	    2	    int16	numberOfContours
    0x02	    2	    int16	xMin
    0x04	    2	    int16	yMin
    0x06	    2	    int16	xMax
    0x08	    2	    int16	yMax
    Дальше для простого глифа (numberOfContours => 0), смещения - от начала глифа:

    Поле	            Тип	                        Описание
    endPtsOfContours	uint16[numContours]	        Индекс последней точки каждого контура
    instructionLength	uint16	                    Длина инструкций
    instructions	    uint8[instructionLength]	Байт-код хинтианг
    flags	            uint8[перем.]	            Флаги точек (с Repeat)
    xCoordinates	    uint8/int16[]	            X-координаты, дельта-кодированные
    yCoordinates	    uint8/int16[]	            Y-координаты, дельта-кодированные
    """

    numberOfContours: int
    xMin: int
    yMin: int
    xMax: int
    yMax: int
    endPtsOfContours: list[int]
    flags: list[int]
    xCoordinates: list[int]
    yCoordinates: list[int]

    @staticmethod
    def _from(data: bytes) -> glyph:
        """
        data - байты ОДНОГО глифа: glyf.raw_bytes[loca[i] : loca[i+1]].
        Возвращает Glyph или None, если глиф композитный (numberOfContours < 0).
        """

class glyf: # контуры глифов
    """
    Таблица glyf - все глифы шрифта, уже разобранные.

    Зачем нужна:
        Хранит список объектов Glyph, по одному на каждый глиф.
        После Glyf._from парсинг закончен - можно сразу брать
        glyf.glyphs[glyph_id] и рисовать.

    Что внутри:
        glyphs - список длиной numGlyphs, где:
            glyphs[i]     - объект Glyph для глифа i
            glyphs[i]     - None, если глиф пустой (пробел)
            glyphs[i]     - None, если глиф композитный (пока не обрабатываем)

    Откуда берутся байты:
        Вся таблица glyf (data) вырезана из файла по offset и length
        из Font Directory. Границы каждого глифа - из loca.offsets:
            глиф №i = data[ loca.offsets[i] : loca.offsets[i+1] ]
    """

    glyphs: list[glyph | None]

    @staticmethod
    def _from(data: bytes) -> glyf:
        """
        Зачем нужна: 
            сама форма буквы. Здесь лежат контуры всех глифов шрифта - точки, кривые Безье, флаги.

        Что внутри: 
            numberOfContours - сколько контуров.
            endPtsOfContours - где кончается каждый контур.
            flags - on-curve / off-curve для каждой точки.
            xCoordinates / yCoordinates - дельта-кодированные координаты.

        Кто использует: 
            рендер - читает контуры, строит полигоны, растеризует. 
            Это ядро отрисовки.
        """