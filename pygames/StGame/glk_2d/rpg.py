from .pougc import Chart as _Chart, Block as _Block, Plaer as _Plaer
import pygame

class Block(_Block):
    teg = "FyForge:rpg.Block"
    def __init__(self, x_y, image, colisens=True):
        super().__init__(x_y, image, colisens)
    def muve(self, x, y):
        self.x += x
        self.y += y

class Plaer(_Plaer):
	teg = "FyForge:plaer.Plaer"
	speed = 5
	def event(self, e: pygame.event.Event):
		pass
	def update(self):
		x = y = 0
		keys = pygame.key.get_pressed()
		#print(self.coliseon(y = -self.speed))
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			if self.coliseon(y = self.speed)[0]:
				y += self.speed
		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			if self.coliseon(y = -self.speed)[0]:
				y -= self.speed
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			if self.coliseon(x = +self.speed)[0]:
				x += self.speed
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			if self.coliseon(x = -self.speed)[0]:
				x -= self.speed
		if x or y:
			self.muve_main(x, y)
	def muve(self, x, y): ...
        
class Chart(_Chart):
	teg = "FyForge:rpg.Chart"
	def __init__(self, x_y, wigth_height, blocks = None):
		super().__init__(x_y, wigth_height, blocks)
	def muve(self, x, y):
		self.x += x
		self.y += y
		for block in self.colisin_blocks:
			block.muve(x, y)