# прямой API sdl2
from sdl2.clipboard import (SDL_SetClipboardText as SetClipboardText, # Помещает текст в системный буфер обмена. 0 при успехе, отрицательное значение при ошибке
                            SDL_GetClipboardText as GetClipboardText, # Извлекает текст из буфера обмена. bytes с текстом (в кодировке UTF-8)
                            SDL_HasClipboardText as HasClipboardText, # Проверяет, содержит ли буфер обмена текст. True, если текст есть, иначе False
                            SDL_SetPrimarySelectionText as SetPrimarySelectionText, # Помещает текст в primary selection (только для Unix/Linux). 0 при успехе, отрицательное значение при ошибке
                            SDL_GetPrimarySelectionText as GetPrimarySelectionText, # Извлекает текст из primary selection (только для Unix/Linux).	bytes с текстом
                            SDL_HasPrimarySelectionText as HasPrimarySelectionText) # Проверяет наличие текста в primary selection (только для Unix/Linux).	True или False

# оболочка над API sdl2
def set_text_buffer(text: str) -> None:
    """
    Устанавливает текст в буфер обмена.

    Args:
        text (str): Текст который мы хотим поместить в буфер.
    Raise:
        BufferError: если буфер не работает.
    """
    err = SetClipboardText(text.encode('utf-8'))
    if err:
        raise BufferError(f"Ошибка в буфере: {err}")

def get_text_buffer() -> str:
    """
    Возвращает текст из буфер обмена.

    Return:
        str: Текст который лежал в буфере обмена
    Raise:
        BufferError: если буфер не работает.
    """
    if HasClipboardText():
        return GetClipboardText().decode('utf-8')
    else:
        raise BufferError("Не удалось достать текст из буфера")