# цветовые темы
TEMA = {
    "light": {
        "line": (160, 160, 160),
        "fon": (255,255,255),
        "fin_further": (0, 0, 0, 30),
        "text": (0, 0, 0)
    }
}


def set_TEMA(n):
    global _TEMA
    _TEMA = n

def get_TEMA():
    global _TEMA
    return _TEMA

# стандарт
set_TEMA("light")