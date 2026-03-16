import pygame 

try:
    function
except NameError:
	class function(object):
		pass



class StrucktureBlock(pygame.sprite.Sprite):
	name = "StrucktureBlock"
	id = 0
	teg = "FyForge:struckture.StrucktureBlock"
	npt_teg = dict(struckture=True, type="rect")
	type = "rect"
	
	def update(self): ... # обновление
	def event(self, e: pygame.event.Event): ... # эвенты
	def draw(self, s: pygame.Surface): ... #рисование
	def colisen(self, side): ... #вызывается при колизии
	def get_rect(self) -> pygame.Rect: ... #возвращает класс Rect из pygame
	def is_walk(self) -> bool: return True # работает ли колизия на обьекте
	def set_function(self, f: function): ... #получапт функцию 
	def muve(self, x, y): ... #сдвиг
	def muve_report(self, f):
		self.muve_main = f
		def wrapper(*args, **kargs):
			return f(*args, **kargs)
		return wrapper
class Block(StrucktureBlock):
	teg = "FyForge:block.Block"
	def set_function(self, f: function, i):
		self._coliseon = f
		self.index = i
		
	def coliseon(self, x=0, y=0):
		return self._coliseon(x,y,self)
	def __init__(self, x_y, image: pygame.Surface, colisens = True):
		self.x, self.y = x_y
		self.image = image
		self.is_walk = (lambda _ = None: colisens)
	def draw(self, s: pygame.Surface):
		s.blit(self.image, (self.x, self.y))
		
	def get_rect(self):
		return self.image.get_rect(topleft=(self.x, self.y))
			
class Plaer(Block):
	teg = "FyForge:plaer.Plaer"
	speed = 5
	def event(self, e: pygame.event.Event):
		pass
	def update(self):
		keys = pygame.key.get_pressed()
		#print(self.coliseon(y = -self.speed))
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			if self.coliseon(y = -self.speed)[0]:
				self.y -= self.speed
		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			if self.coliseon(y = self.speed)[0]:
				self.y += self.speed
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			if self.coliseon(x = -self.speed)[0]:
				self.x -= self.speed
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			if self.coliseon(x = self.speed)[0]:
				self.x += self.speed
				
class Chart:
	colisin_blocks: list[StrucktureBlock]
	def listing_colisen(self, x, y, odjk, i=0):
		main_rect = odjk.get_rect().move(x, y)
		index = odjk.index
		log = set()
		for rect in self.colisin_blocks:
			
			if (main_rect.colliderect(rect.get_rect()) and rect.is_walk()) and rect.index != index:
				log.add((rect.teg, rect.id))
		return (not log.__len__()), log
	def __init__(self, x_y, wigth_height , blocks: list | None = None):
		self.x, self.y, self.wigth, self.height = (*x_y, *wigth_height)
		
		self.colisin_blocks = list()  if blocks is None else blocks
		self.colisin_blocks_rect = list()
		
		self.update_rect()
	def update_rect(self):
		self.colisin_blocks_rect = list()
		for i, rect in enumerate(self.colisin_blocks):
			rect.set_function(self.listing_colisen, i)
			rect.muve_report(self.muve)
			#rect.set_function((lambda x=0, y=0, rect= rect, i = i: self.listing_colisen(x, y, rect)))
			
	def update(self):
		for rect in self.colisin_blocks:
			rect.update()	
	def draw(self, s: pygame.Surface):
		for rect in self.colisin_blocks:
			rect.draw(s)
	def event(self, e: pygame.event.Event):
		for rect in self.colisin_blocks:
			rect.event(e)
	def muve(self, x, y): ... #сдвиг
			
if __name__ == "__main__":
	width, height = 1000, 700
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	clock = pygame.time.Clock()
	p = 20
	c = Chart((0,0), (300, 400), [
		Block((20, 40),pygame.Surface ((14, 79))),
		Plaer((200, 40),pygame.Surface ((90, 79)))
		])
	r = 1
	while r:
		screen.fill((78, 98, 179))
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: r = 0
			c.event(event)
			if event.type == pygame.KSCAN_W:
				print(1)
		c.update()
		c.draw(screen)
		pygame.display.flip()
		clock.tick(60)
		#print(clock.get_fps())
	pygame.quit()
	