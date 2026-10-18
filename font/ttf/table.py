"""
Ниже dataclasses для всех таблиц, которые нужны для рендера. 
Каждое поле снабжено комментарием: что это и зачем оно. 
В конце — зачем вообще нужен сам файл шрифта.

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
    def _from(datahead: bytes) -> "head":
        """
        Зачем нужна: 
            хранит глобальные параметры шрифта. Без неё не понять, в каких единицах заданы координаты и как читать другие таблицы.

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

    def _to(self) -> bytes:
        return (
            self.version.to_bytes(4) +
            self.fontRevision.to_bytes(4) +
            self.checkSumAdjustment.to_bytes(4) +
            self.magicNumber.to_bytes(4) +
            self.flags.to_bytes(2) +
            self.unitsPerEm.to_bytes(2) +
            self.created.to_bytes(8) +
            self.modified.to_bytes(8) +
            self.xMin.to_bytes(2) +
            self.yMin.to_bytes(2) +
            self.xMax.to_bytes(2) +
            self.yMax.to_bytes(2) +
            self.macStyle.to_bytes(2) +
            self.lowestRecPPEM.to_bytes(2) +
            self.fontDirectionHint.to_bytes(2) +
            self.indexToLocFormat.to_bytes(2) + 
            self.glyphDataFormat.to_bytes(2)
        )

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
    def _from(datamaxp: bytes) -> "maxp":
        """
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

@dataclass
class loca: # индекс местоположений глифов
    """
    Смещение в loca	Размер	Тип	Имя
    2*i (короткий)	2	uint16	offset[i], реальное = значение * 2
    4*i (длинный)	4	uint32	offset[i], реальное = значение
    Длина массива — numGlyphs + 1 элементов.

    """
    @staticmethod
    def _from(data: bytes) -> "loca":
        """
        Зачем нужна: 
            говорит, где именно в таблице glyf лежит каждый глиф. 
            Без неё glyf — просто куча байт, в которой не найти нужный глиф.

        Что внутри: 
            массив из numGlyphs + 1 смещений. 
            Границы глифа glyph_id — это loca[glyph_id] и loca[glyph_id + 1] (относительно начала glyf).
        
        Кто использует: 
            рендер — чтобы вырезать байты конкретного глифа.
        """

@dataclass
class glyf: # контуры глифов
    """
    Границы глифа берутся из loca: глиф №i занимает байты [loca[i], loca[i+1]) от начала glyf.

    Заголовок глифа (10 байт):

    Смещение    Размер	Тип	    Имя
    0x00	    2	    int16	numberOfContours
    0x02	    2	    int16	xMin
    0x04	    2	    int16	yMin
    0x06	    2	    int16	xMax
    0x08	    2	    int16	yMax
    Дальше для простого глифа (numberOfContours => 0), смещения — от начала глифа:

    Поле	            Тип	                        Описание
    endPtsOfContours	uint16[numContours]	        Индекс последней точки каждого контура
    instructionLength	uint16	                    Длина инструкций
    instructions	    uint8[instructionLength]	Байт-код хинтинга
    flags	            uint8[перем.]	            Флаги точек (с Repeat)
    xCoordinates	    uint8/int16[]	            X-координаты, дельта-кодированные
    yCoordinates	    uint8/int16[]	            Y-координаты, дельта-кодированные
    """

    @staticmethod
    def _from(data: bytes) -> "glyf":
        """
        Зачем нужна: 
            сама форма буквы. Здесь лежат контуры всех глифов шрифта — точки, кривые Безье, флаги.

        Что внутри: 
            numberOfContours — сколько контуров.
            endPtsOfContours — где кончается каждый контур.
            flags — on-curve / off-curve для каждой точки.
            xCoordinates / yCoordinates — дельта-кодированные координаты.

        Кто использует: 
            рендер — читает контуры, строит полигоны, растеризует. 
            Это ядро отрисовки.
        """

@dataclass
class cmap: # сопоставление символов и глифов
    """
    Смещение    	    Размер	Тип	    Имя
    0x00	            2	    uint16	version
    0x02	            2	    uint16	numTables
    0x04 + 8*i + 0x00	2	    uint16	platformID (запись №i)
    0x04 + 8*i + 0x02	2	    uint16	encodingID
    0x04 + 8*i + 0x04	4	    uint32	subtableOffset

    Подтаблица Format 4 — от начала подтаблицы:
    Смещение            Размер	    Тип	    Имя
    0x00	            2	        uint16	format (= 4)
    0x02	            2	        uint16	length
    0x04	            2	        uint16	language
    0x06	            2	        uint16	segCountX2
    0x08	            2	        uint16	searchRange
    0x0A	            2	        uint16	entrySelector
    0x0C	            2	        uint16	rangeShift
    0x0E	            2*segCount	uint16	endCode[]
    0x0E + 2*segCount	2	        uint16	reservedPad
    0x10 + 2*segCount	2*segCount	uint16	startCode[]
    0x10 + 4*segCount	2*segCount	int16	idDelta[]
    0x10 + 6*segCount	2*segCount	uint16	idRangeOffset[]
    0x10 + 8*segCount	перем.	    uint16	glyphIdArray[]

    """
    @staticmethod
    def _from(data: bytes) -> "cmap":
        """
        Зачем нужна: 
            переводит код символа (Unicode) в номер глифа (glyph_id). 
            Без неё ты не знаешь, какой глиф соответствует букве 'A'.

        Что внутри: 
            одна или несколько подтаблиц. 
            Основная — Format 4 (Unicode BMP) с сегментами startCode…endCode и массивом glyphIdArray.

        Кто использует: 
            рендер текста — первый шаг. Символ => glyph_id => дальше ищем контуры.
        """
@dataclass
class hhea: # горизонтальный заголовок
    """
    Смещение    Размер	Тип	    Имя
    0x00	    4	    Fixed	version
    0x04	    2	    int16	ascender
    0x06	    2	    int16	descender
    0x08	    2	    int16	lineGap
    0x0A	    2	    uint16	advanceWidthMax
    0x0C	    2	    int16	minLeftSideBearing
    0x0E	    2	    int16	minRightSideBearing
    0x10	    2	    int16	xMaxExtent
    0x12	    2	    int16	caretSlopeRise
    0x14	    2	    int16	caretSlopeRun
    0x16	    2	    int16	caretOffset
    0x18	    8	    —	    reserved (4 * int16 = 0)
    0x20	    2	    int16	metricDataFormat
    0x22	    2	    uint16	numberOfHMetrics

    """

    @staticmethod
    def _from(data: bytes) -> "hhea":
        """
        Зачем нужна: 
            метрики строки и указание, сколько записей в hmtx.

        Что внутри:
            ascender / descender / lineGap — высота над baseline, глубина под baseline, межстрочный интервал.
            advanceWidthMax — максимальная ширина глифа.
            numberOfHMetrics — сколько глифов имеют собственную ширину в hmtx.

        Кто использует: 
            рендер текста — для вертикального позиционирования строки. 
            Парсер hmtx — чтобы понять, сколько записей читать.
        """

@dataclass
class hmtx: # горизонтальные метрики
    """
    Смещение 	    Размер	Тип	    Имя
    0x00 + 4*i	    2	    uint16	advanceWidth[i] (для i < N)
    0x02 + 4*i	    2	    int16	leftSideBearing[i] (для i < N)
    4*N + 2*(i - N)	2	    int16	leftSideBearing[i] (для i >= N)

    где N = numberOfHMetrics из hhea.
    """

    @staticmethod
    def _from(data: bytes) -> "hmtx":
        """
        Зачем нужна: 
            говорит, на сколько сдвинуть курсор после каждого глифа и какой у него левый отступ.

        Что внутри:
            advanceWidth[glyph_id] — ширина ячейки глифа (на сколько пикселей сдвинуть перо).
            leftSideBearing[glyph_id] — отступ от левого края ячейки до первой точки контура.

        Кто использует: 
            рендер строки — расстановка глифов. Без этой таблицы все буквы налезут друг на друга.


        """

@dataclass
class name: # имена
    """
    Смещение            Размер	Тип	    Имя
    0x00	            2	    uint16	format
    0x02	            2	    uint16	count
    0x04	            2	    uint16	stringOffset
    0x06 + 12*i + 0x00	2	    uint16	platformID (запись №i)
    0x06 + 12*i + 0x02	2	    uint16	encodingID
    0x06 + 12*i + 0x04	2	    uint16	languageID
    0x06 + 12*i + 0x06	2	    uint16	nameID
    0x06 + 12*i + 0x08	2	    uint16	length
    0x06 + 12*i + 0x0A	2	    uint16	offset
    
    Сами строки лежат по адресу stringOffset + offset от начала name.
    """

    @staticmethod
    def _from(data: bytes) -> "name":
        """
        Зачем нужна: 
            человекочитаемая информация о шрифте — что это за шрифт, кто автор, версия, лицензия.

        Что внутри: 
            набор записей nameID => строка. 
            Полезные: семейство, подсемейство (Regular/Bold), полное имя, версия, PostScript-имя.

        Кто использует: 
            операционная система для отображения имени шрифта в списке. 
            Для рендера не нужна, но полезна для отладки («что я вообще открыл»).
        """

@dataclass
class post: # PostScript-информация
    """
    Смещение    Размер	Тип	    Имя
    0x00	    4	    Fixed	version
    0x04	    4	    Fixed	italicAngle
    0x08	    2	    int16	underlinePosition
    0x0A	    2	    int16	underlineThickness
    0x0C	    4	    uint32	isFixedPitch
    0x10	    4	    uint32	minMemType42
    0x14	    4	    uint32	maxMemType42
    0x18	    4	    uint32	minMemType1
    0x1C	    4	    uint32	maxMemType1

    Дальше — зависит от версии (в 2.0 идёт массив имён глифов, в 3.0 ничего).
    """

    @staticmethod
    def _from(data: bytes) -> "post":
        """
        Зачем нужна: 
            метрики для совместимости с PostScript и признак моноширинности.

        Что внутри:
            isFixedPitch — 0 для пропорционального шрифта, ≠0 для моноширинного.
            italicAngle, underlinePosition, underlineThickness.
            В версии 2.0 — имена всех глифов.

        Кто использует: 
            в основном системы печати. Для рендера полезна только isFixedPitch — если шрифт моноширинный, можно упростить расстановку.
        """

# Опциональные, но почти всегда присутствуют

@dataclass
class OSH2: # OS/2 (H = F+2) — метрики для Windows
    """
    Смещение    Размер	Тип	        Имя
    0x00	    2	    uint16	    version
    0x02	    2	    int16	    xAvgCharWidth
    0x04	    2	    uint16	    usWeightClass
    0x06	    2	    uint16	    usWidthClass
    0x08	    2	    uint16	    fsType
    0x0A	    2	    int16	    ySubscriptXSize
    0x0C	    2	    int16	    ySubscriptYSize
    0x0E	    2	    int16	    ySubscriptXOffset
    0x10	    2	    int16	    ySubscriptYOffset
    0x12	    2	    int16	    ySuperscriptXSize
    0x14	    2	    int16	    ySuperscriptYSize
    0x16	    2	    int16	    ySuperscriptXOffset
    0x18	    2	    int16	    ySuperscriptYOffset
    0x1A	    2	    int16	    yStrikeoutSize
    0x1C	    2	    int16	    yStrikeoutPosition
    0x1E	    2	    int16	    sFamilyClass
    0x20	    10	    uint8[10]	panose
    0x2A	    4	    uint32	    ulUnicodeRange1
    0x2E	    4	    uint32	    ulUnicodeRange2
    0x32	    4	    uint32	    ulUnicodeRange3
    0x36	    4	    uint32	    ulUnicodeRange4
    0x3A	    4	    —	        achVendID (4 символа)
    0x3E	    2	    uint16	    fsSelection
    0x40	    2	    uint16	    usFirstCharIndex
    0x42	    2	    uint16	    usLastCharIndex
    0x44	    2	    int16	    sTypoAscender
    0x46	    2	    int16	    sTypoDescender
    0x48	    2	    int16	    sTypoLineGap
    0x4A	    2	    uint16	    usWinAscent
    0x4C	    2	    uint16	    usWinDescent

    Дальше зависит от version:
    v0 — конец (78 байт)
    v1 — добавляются ulCodePageRange1 (0x4E), ulCodePageRange2 (0x52) → 86 байт
    v2 — добавляются sxHeight (0x56), sCapHeight (0x58), usDefaultChar (0x5A), usBreakChar (0x5C), usMaxContext (0x5E) → 96 байт
    v3 — как v2 (не несёт новых полей)
    v4 — + usLowerOpticalPointSize (0x60), usUpperOpticalPointSize (0x62) → 100 байт
    """

    @staticmethod
    def _from(data: bytes) -> "OSH2":
        """
        Зачем нужна: без неё Windows не признаёт шрифт «полноценным» и не использует в некоторых местах.

        Что внутри:
            usWeightClass — 400 (normal), 700 (bold).
            usWidthClass — 1..9, 5 = normal.
            fsSelection — italic, bold, regular.
            sTypoAscender / sTypoDescender / sTypoLineGap — альтернативные метрики строки.
            usWinAscent / usWinDescent — метрики для Windows.
            ulUnicodeRange1..4 — какие блоки Unicode поддерживаются.
            panose — классификация стиля (для подбора похожих шрифтов).

        Кто использует: 
            Windows для выбора шрифта, для позиционирования. 
            Для своего рендера не обязательна — метрики можно взять из hhea.
        """
        return OSH2()

@dataclass
class kern: # кернинг
    @staticmethod
    def _from(data: bytes) -> "kern":
        """
        Зачем нужна: 
            попарные сдвиги между глифами. 
            Например, AV в большинстве шрифтов сближаются, потому что «A» и «V» можно подвинуть друг к другу.

        Что внутри: 
            таблица пар (left_glyph, right_glyph) → value. 
            value прибавляется к advanceWidth левого глифа при рендере.

        Кто использует: 
            рендер — для качественной типографики. 
            Без неё буквы стоят «по сетке», но всё равно читаемо. 

        """

@dataclass
class GPOS: # OpenType-позиционирование
    @staticmethod
    def _from(data: bytes) -> "GPOS":
        """
        Зачем нужна: 
            современная замена kern. 
            Умеет не только попарный кернинг, но и сложное позиционирование: 
                диакритика (например, «й» = «и» + breve), марки, курсивные наклоны.

        Что внутри: 
            сложная система lookup-таблиц с бинарным форматом. 
            Гораздо сложнее kern.

        Кто использует: 
            cовременные шрифты с качественной типографикой.
        """

@dataclass
class GSUB: # OpenType-подстановки
    @staticmethod
    def _from(data: bytes) -> "GSUB":
        """
        Зачем нужна: 
            замены глифов. Лигатуры (fi → ﬁ), альтернативные формы, маленькие заглавные и т.д.

        Что внутри: 
            похоже на GPOS — lookup-таблицы.

        Кто использует: 
            продвинутая типографика.
        """

@dataclass
class GDEF: # классы глифов
    @staticmethod
    def _from(data: bytes) -> "GDEF":
        """
        Зачем нужна: 
            вспомогательная для GPOS и GSUB. 
            Размечает глифы на категории: базовые, марки, лигатуры.

        Что внутри: 
            массив классов глифов и таблица атрибутов.

        Кто использует: 
            только GPOS/GSUB. Самостоятельного значения не имеет.
        """

# Опциональные, для хинтинга
#
# Хинтинг — это подсказки рендереру, как правильно округлять глифы при мелких размерах. 
# Реализовать его очень сложно (это интерпретатор байт-кода). 

@dataclass
class cvt: # Control Values Table
    @staticmethod
    def _from(data: bytes) -> "cvt":
        """
        Зачем нужна: 
            массив «опорных» вертикальных и горизонтальных значений (высоты штрихов, положение baseline). 
            Хинтинг-программа использует их как эталоны.

        Что внутри: 
            массив int16
        """    

@dataclass
class fpgm: #  Font Program
    @staticmethod
    def _from(data: bytes) -> "fpgm":
        """
        Зачем нужна: 
            байт-код, который выполняется один раз при загрузке шрифта. 
            Определяет вспомогательные функции, настраивает переменные для хинтинга.

        Что внутри: 
            байт-код для виртуальной машины TrueType.
        """

@dataclass
class prep: # Pre-Program
    @staticmethod
    def _from(data: bytes) -> "prep":
        """
        Зачем нужна: 
            байт-код, который выполняется при каждом размере шрифта. 
            Настраивает control values под конкретный ppem (пикселей на em).

        Что внутри: 
            байт-код.
        """
@dataclass
class gasp:
    @staticmethod
    def _from(data: bytes) -> "gasp":
        """
        Зачем нужна: 
            говорит рендереру, для каких размеров применять хинтинг, для каких — сглаживание.

        Что внутри: 
            массив пар (размер, флаги). 

        Флаги: 
            применять ли grid-fitting, применять ли сглаживание.

        Кто использует: 
            системный рендерер.
        """

# Опциональные, специальные

@dataclass
class DSIG: # цифровая подпись
    @staticmethod
    def _from(data: bytes) -> "DSIG":
        """
        Зачем нужна: 
            подтверждает, что шрифт не был изменён после выпуска. 
            Криптографическая подпись.

        Что внутри: 
            записи с форматом, длиной и смещением подписи. 
            Сами подписи — отдельные блоки данных.

        Кто использует: 
            системы проверки легитимности шрифта.
        """

@dataclass
class hdmx:
    @staticmethod
    def _from(data: bytes) -> "hdmx": # Horizontal Device Metrics
        """
        Зачем нужна: 
            заранее посчитанные ширины глифов для конкретных ppem. 
            Ускоряет рендеринг на старых системах.

        Что внутри: 
            для каждого размера — массив ширин.

        Кто использует: 
            старые Windows. 
            Современный рендер обходится.
        """

@dataclass
class LTSH: # Linear Threshold
    @staticmethod
    def _from(data: bytes) -> "LTSH":
        """
        Зачем нужна: 
            говорит, с какого размера глиф можно рендерить «линейно», без хинтинга.

        Что внутри: 
            массив порогов на каждый глиф.

        Кто использует: 
            вместе с хинтингом.
        """

@dataclass
class VDMX: #  Vertical Device Metrics
    @staticmethod
    def _from(data: bytes) -> "VDMX":
        """
        Зачем нужна: 
            заранее посчитанные вертикальные метрики для конкретных размеров. 
            Нужна для правильного межстрочного расстояния на малых размерах.

        Что внутри: 
            сложная структура из групп размеров и значений.

        Кто использует: 
            Windows для вертикального позиционирования.
        """

@dataclass
class ttcf: # TTC / ttcf — TrueType Collection
    @staticmethod
    def _from(data: bytes) -> "ttcf":
        """
        Зачем нужна: 
            позволяет в одном файле хранить несколько шрифтов, 
            разделяющих общие таблицы (например, Regular, Bold, Italic — все используют один glyf, но разные hmtx и head).

        Что внутри: 
            список offset до Font Directory каждого шрифта.

        Кто использует: 
            системы для экономии места. 
        Для парсера: 
            если видишь sfntVersion = 'ttcf', значит файл — коллекция, и работать надо чуть иначе.
        """
@dataclass
class EBLC: # EBLC / EBDT — встроенные bitmap-глифы
    @staticmethod
    def _from(data: bytes) -> "EBLC":
        """
        Зачем нужна: 
            шрифт может содержать готовые картинки глифов для мелких размеров (не контуры, а пиксели). 
            Рендерер тогда просто берёт картинку, не растеризует.

        Что внутри: 
            метрики (EBLC) и сами битмапы (EBDT) или их сжатые варианты (EBSC, CBDT, CBLC).

        Кто использует: 
            рендереры для повышения чёткости на малых размерах. 
        """

@dataclass
class SVG: # SVG-глифы
    @staticmethod
    def _from(data: bytes) -> "SVG":
        """
        Зачем нужна: 
            глифы описываются как SVG. 
            Полезно для цветных и сложных шрифтов (иконки, эмодзи).

        Что внутри: 
            таблица с SVG-документами для глифов.

        Кто использует: 
            современные браузеры для цветных шрифтов.
        """
@dataclass
class COLR: # COLR / CPAL — цветные глифы
    @staticmethod
    def _from(data: bytes) -> "COLR":
        """
        Зачем нужна: 
            для эмодзи и иконок. 
            COLR описывает, как собрать цветной глиф из слоёв, CPAL — палитру цветов.

        Что внутри: 
            слоистые описания + цвета.

        Кто использует: 
            рендерер эмодзи.
        """

#   Минимум для базового рендера текста:
#   Таблица	    Зачем
#   head	    unitsPerEm, indexToLocFormat
#   maxp	    numGlyphs
#   loca	    границы глифов
#   glyf	    контуры
#   cmap	    символ → glyph_id
#   hhea	    numberOfHMetrics, метрики строки
#   hmtx	    ширины глифов
#
#   Добавь потом, для качества:
#   Таблица	    Что даёт
#   kern	    попарный кернинг
#   OS/2	    альтернативные метрики, вес/стиль
#
#   Игнорируй полностью:
#   Таблица	                    Почему
#   cvt, fpgm, prep, gasp, LTSH	хинтинг — очень сложно, не критично
#   GPOS, GSUB, GDEF	        продвинутая типографика
#   DSIG, hdmx, VDMX	        служебные
#   name, post	                метаданные
#   EBLC, EBDT, SVG, COLR	    спец-случаи (bitmap, цветные)