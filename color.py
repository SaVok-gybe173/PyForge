from dataclasses import dataclass

def cmyk_to_rgb(cmyk: "CMYK") -> "RGB":
    """c,m,y,k в процентах (0-100) -> (r,g,b) 0-255"""
    return RGB(int(round(255 * (1 - cmyk.c / 100.0) * (1 - cmyk.k / 100.0))), int(round(255 * (1 - cmyk.m / 100.0) * (1 - cmyk.k / 100.0))), int(round(255 * (1 - cmyk.y / 100.0) * (1 - cmyk.k / 100.0))))

def rgb_to_cmyk(rgb: "RGB") -> "CMYK":
    """r,g,b 0-255 -> (c,m,y,k) в процентах 0-100"""
    k = 1 - max(rgb.r / 255.0, rgb.g / 255.0, rgb.b / 255.0)
    if k == 1:
        return CMYK(0, 0, 0, 100)
    return CMYK(int(round((1 - rgb.r / 255.0 - k) / (1 - k) * 100)), int(round((1 - rgb.g / 255.0 - k) / (1 - k) * 100)), int(round((1 - rgb.b / 255.0 - k) / (1 - k) * 100)), int(round(k * 100)))

def rgb_to_hsv(rgb: "RGB") -> "HSV":
    r_norm = rgb.r / 255.0
    g_norm = rgb.g / 255.0
    b_norm = rgb.b / 255.0
    max_c = max(r_norm, g_norm, b_norm)
    diff = max_c - min(r_norm, g_norm, b_norm)
    if diff == 0: h = 0
    elif max_c == r_norm: h = 60 * ((g_norm - b_norm) / diff % 6)
    elif max_c == g_norm: h = 60 * ((b_norm - r_norm) / diff + 2)
    else: h = 60 * ((r_norm - g_norm) / diff + 4)
    return HSV(int(round(h)), int(round((0 if max_c == 0 else diff / max_c) * 100)), int(round(max_c * 100)))

@dataclass
class RGB:
    r: int
    g: int
    b: int

@dataclass
class CMYK:
    c: int
    m: int
    y: int
    k: int

@dataclass
class LAB:
    l: int
    a: int
    b: int

@dataclass
class HSV:
    h: int
    s: int
    b: int