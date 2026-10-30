from .animation import FrameAnimationButton
from ....cpu.creating.image.tools import round_corners_alternative
from ....easel import Surface
from ....easel.event import Event, CommonEvent, MouseMotionEvent, MouseButtonEvent, MOUSEBUTTONDOWN, MouseWheelEvent
    
class Increase(FrameAnimationButton):
    def __init__(self, speed = 0.5, fps = 60, size = 5, click_size = 0, effect_size = 10):
        self.effect_size =  effect_size
        self.speed = speed
        self.click_size = click_size or speed//2
        self.i = 0
        self.conIf = 1/fps
        self.size = size
        
    def effect(self):
        if self.i >= self.effect_size:
            self.i -=  self.effect_size
            self.x += self.effect_size
            self.y += self.effect_size
            self.width -= self.effect_size*2
            self.height -= self.effect_size*2
        else:
            self.x += self.i
            self.y += self.i
            self.width -= self.i*2
            self.height -= self.i*2
            self.i = 0

    def update(self, dt):
        if self.button.rect.collidepoint(*self.button.page.mouse_pos):
            if self.size > self.i:
                self.x = self.x - (self.speed + self.conIf)
                self.y = self.y - (self.speed + self.conIf)
                
                self.height = self.height + (self.speed + self.conIf)*2
                self.width = self.width + (self.speed + self.conIf)*2
                
                self.i += self.speed + self.conIf
        elif 0 < self.i:

            self.x = self.x + (self.speed + self.conIf)
            self.y = self.y + (self.speed + self.conIf)
            
            self.height = self.height - (self.speed + self.conIf)*2
            self.width = self.width - (self.speed + self.conIf)*2
            
            self.i -= self.speed + self.conIf
        self.button.left = self.y
        self.button.top = self.x
        
        self.button.height = self.height
        self.button.width = self.width
    def __call__(self, button):
        super().__call__(button)
        self.x = button.left
        self.y = button.top
        self.width_height = (button.width, button.height)

    def mousebuttondown(self, common: CommonEvent, button: MouseButtonEvent):
        self.effect()

class Impulse(FrameAnimationButton):
    def __init__(self, speed: int | float = 0.5, shadow: int = 50, click_shadow: int = 30, time_click: int | float = 0.1):
        self.speed = speed
        self.i = 0
        self.click_shadow = click_shadow
        self.shadow = (0,0,0, shadow)
        self.shadow_srov = (0,0,0,0)
        
        self.shadow_surface = None
        self.radius = 0
        self.SusTo = None
        
        self.time_click = time_click
        self.activity = 0
        self.a_activity = True
    def __call__(self, button):
        super().__call__(button)
        self.shadow_surface = Surface((button.width, button.height))
        
    def update(self, dt):
        
        if self.button.rect.collidepoint(*self.button.page.mouse_pos):
            if self.SusTo != 0:
                self.SusTo = 0
                self.shadow_surface.fill(self.shadow)
                self._round_image()
        else:
            if self.SusTo != 1:
                self.SusTo = 1
                self.shadow_surface.fill(self.shadow_srov)
                self._round_image()
        
        if self.activity < self.time_click and self.a_activity:
            self.activity += dt
        elif self.a_activity:
            self.a_activity = False
            self.SusTo = 0
            self.shadow_surface.fill(self.shadow)
            self._round_image()
            
    def draw(self, screen: Surface):
        screen.blit(self.shadow_surface, (self.button.left, self.button.top))
        #pg.draw.circle(self.shadow_surface, (0,0,0), (50, 25), 20)
    def _round_image(self):
        pass
    def effect(self):
        self.a_activity = True
        self.activity = 0
        self.shadow_surface.fill((self.shadow[0], self.shadow[2], self.shadow[2], self.shadow[3]+self.click_shadow))
        self._round_image()
    
class ImageClick(FrameAnimationButton):
    def __init__(self, retention_image: Surface, click_image: Surface, time_click: int | float = 0.15):
        self.retention_image = retention_image
        self.click_image = click_image
        self.activity = time_click
        self.time_click = time_click
    def update(self, dt):
        if self.activity < self.time_click:
            self.activity += dt
            self.button.img = self.click_image
        elif self.button.rect.collidepoint(*self.button.page.mouse_pos):
            self.button.img = self.retention_image
        else:
            self.button.img = self.static_image
    def __call__(self, button):
        self.static_image = button.img
        return super().__call__(button)
    def effect(self):
        self.activity = 0

    def mousebuttondown(self, common: CommonEvent, button: MouseButtonEvent):
        if self.button.rect.collidepoint(button.x, button.y):
                self.activity = 0

            