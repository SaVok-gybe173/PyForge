from PyForge.button import AnimationButton, Impuls
import pygame as pg

def format_size(bytes_count, units = ["КБ", "МБ", "ГБ", "ТБ", "ПБ"], byte = "Б" ):
    """
    Преобразует размер в байтах в строку с единицами измерения (КБ, МБ, ГБ...).
    Используется деление на 1024, округление вниз (отбрасывание дробной части).
    
    Аргументы:
        bytes_count (int): размер в байтах.
    
    Возвращает:
        str: строка вида "число единица", например "166 КБ".
    """
    if bytes_count < 1024:
        return f"{bytes_count}", f"{byte}"
    size = bytes_count
    for unit in units:
        size /= 1024.0
        if size < 1024:
            return f"{int(size)}", f"{unit}"
    return f"{int(size)}", f"{units[-1]}"

def _wrap_text(text: str, font: pg.font.Font, max_width: int): # отступы
    words = text.split(' ')
    lines: list[str] = []
    current_line = []
    for word in words:
        # пробуем добавить слово
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def _render(text: str, font: pg.font.Font, width: int, 
indent: int = 2, color = (0, 0, 0)): # рендр текста
    lens = 0

    texts = []
    for line in text.split('\n'):
            #print(_wrap_text(line, font, size[0]))
            for i in _wrap_text(line, font, width):
                texts.append(i)
    sur = pg.Surface((width, (font.get_height()+indent)*len(texts)+indent), pg.SRCALPHA)
    for line in texts:
            rend = font.render(line, True, color)
            lens += indent
            sur.blit(rend, (0, lens))
            lens += rend.get_height()
    
    return sur
        