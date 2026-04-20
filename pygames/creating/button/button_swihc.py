import pygame as pg
try:
	from ..colisions import collision_surface, collision_maus
except ImportError:
	from colisions import collision_surface, collision_maus
from PyForge.tools import PfObject

class AnimarionSwitching(PfObject):
	pass

class Circle(PfObject):
	def __init__(self, holst: pg.Surface = None, color = (225,25,225), spid = 10):
		self.holst = holst
		self.center = None
		self.color = color
		self.x = self.y = 0
		self.fin_position = 0
		self.new_position = 0
		self.spid = spid
		
	def __call__(self, button: "Switching"):
		self.button = button
		if self.holst is None:
			self.holst = pg.Surface((button.holst.get_width() // 2, button.holst.get_width()))
			
			self.holst.fill(self.color)
		self.fin_position = button.holst.get_width() //2 #button.button.distance
		print(self.fin_position)
	def _update(self):
		pass
	def update(self):
		if self.x+self.spid < self.new_position:
			self.x += self.spid
		elif self.x > self.new_position+self.spid: 
			self.x  -= self.spid
		else:
			self.x = self.new_position
	def draw(self, holst):
		#self.x = self.new_position
		holst.blit(self.holst, (int(self.x), self.y))
	def on_click(self, aktiv):
		if aktiv:
			self.new_position = 0
		else:
			self.new_position = self.fin_position

class Switching(PfObject):
	def __init__(self, color = (0,0,0,0),circle: Circle = None, radius = 0, color_radius = (0,0,0,0), animation: AnimarionSwitching = None):
		''' 
		*args:
			color: цвет кнопки
			radius: радиус скругления кнопки
			color_radius: цвет скругления
			animation: класс анимации
		'''
		self.circle = Circle() if circle is None else circle
		self.animation = AnimarionSwitching() if  animation is None else animation
		self._aktivation = False
		self.color = color
		self.radius = radius
		self.color_radius = color_radius
		
	def __call__(self, button: "SwitchingButton", wigth_height, x_y):
		self.up = pg.Surface(wigth_height)
		self.button = button
		self.set_wigth_height(wigth_height)
		self.x, self.y = x_y
		self._update()
		
		
	def set_wigth_height(self, wigth_height):
		self.holst = pg.Surface(wigth_height)
		self.holst.fill(self.color)
		self.circle(self)
		
	def _update(self):
		self.button_rect = self.holst.get_rect(topleft = (self.x, self.y ))
		self.circle._update()
	def on(self):
		self.aktivation = True
	def off(self):
		self.aktivation = False
	def shift(self):
		self._aktivation = not self._aktivation
		self.on_click()
	
	@property
	def aktivation(self):
		return self._aktivation
	@aktivation.setter
	def aktivation(self, activ):
			self._aktivatio = activ
			self.on_click()
			
	def on_click(self):
		self.circle.on_click(self.aktivation)
	def draw(self, holst):
		self.up.blit(self.holst, (0,0))
		self.circle.draw(self.up)
		holst.blit(self.up, (self.x, self.y))
	def update(self):
		pass
		
class SwitchingButton(PfObject):
	def __init__(self, wigth_height = (80,40), x_y = (0,0), switching: Switching = None, radius: int = 0, distance = 4):
		''' 
		*args:
			wigth_height: размеры
			x_y: кординаты
			switching: кнопка
			
			animation: класс анимации
			
		'''
		if switching is None: switching = Switching()
		self.switching = switching 
		self.visible = True
		self.holst = pg.Surface(wigth_height)
		self.holst.fill((255,255,255))
		self.x, self.y = x_y
		self.distance = distance
		self._update(wigth_height)
		
	def update(self):
		self.switching.update()
		self.switching.circle.update()
	def _update(self, wigth_height):
		self.switching(self, (wigth_height[0]-(self.distance*2),wigth_height[1]-(self.distance*2) ), (self.distance, self.distance))
	def draw(self, screen: pg.Surface):
		if self.visible:
			self.switching.draw(self.holst)
			screen.blit(self.holst, (self.x, self.y))
			
		
	def on_click(self):
		self.switching.on_click()
		
	@property
	def aktivation(self):
		return self.switching.aktivation
	@aktivation.setter
	def aktivation(self, aktivation):
		self.switching.aktivation = aktivation
	def shift(self):
		self.switching.shift()
	def collidespoint_switching(self, pos):
		return collision_maus(self.switching.holst, (self.x+self.distance, self.y+self.switching.y), pos)
		
		
if __name__ == "__main__":
	s = Switching()
	fdk = SwitchingButton(x_y = (300, 200), wigth_height =(100,30))
	fdkkk = SwitchingButton(x_y = (400, 400), switching = s)
	fd = SwitchingButton(x_y = (0, 0), switching = s)
	pg.init()
	clock = pg.time.Clock()
	screen = pg.display.set_mode((500,500))
	r = 1
	while r:
		screen.fill((30,30,30))
		for event in pg.event.get():
			if event.type == pg.QUIT: r = False
			elif event.type == pg.MOUSEBUTTONDOWN:
				if fdk.collidespoint_switching(event.pos):
					fdk.switching.shift()
				elif fdkkk.collidespoint_switching(event.pos):
					fdkkk.switching.shift()
				elif fd.collidespoint_switching(event.pos):
					fd.switching.shift()
		fdk.update()
		fdkkk.update()
		fd.draw(screen)
		fdkkk.draw(screen)
		fdk.draw(screen)
		pg.display.flip()
		clock.tick(60)
	pg.quit()