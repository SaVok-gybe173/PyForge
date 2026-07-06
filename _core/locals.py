"""грфика в движке"""

GRAPHICS_PYGAME = "pygame"
GRAPHICS_GL_2D_ORTHO = "opengl-2d_ortho"
GRAPHICS_GL_3D_PERSPECTIVE = "opengl-3d_perspective"
GRAPHICS_GL_3D_ISOMERIC = "opengl-3d_isometric"
GRAPHICS_GL_2D_PIXEL_PERSPECTIVE = "opengl-2d_pixel_perfect" 
GRAPHICS_GL_CUSTOM_SETUP = "opengl-custom_setup"


class Graphics:
    __instance = None
    graphics = GRAPHICS_PYGAME

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    def __init__(self, graphics: str | None = None):
        if not graphics is None:
            self.graphics = graphics
    def get(self):
        return self.graphics

def changing_graphics(graphics):
    Graphics(graphics)

GRAPHICS = Graphics()

