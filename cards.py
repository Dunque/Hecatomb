import pygame as pg
from settings import *
vec = pg.math.Vector2


class Card(pg.sprite.Sprite):
	def __init__(self, game):
		self.game = game
		self.groups = game.cards
		pg.sprite.Sprite.__init__(self, self.groups)
		self.active = False
		self.pos = vec(0, 0)
		self.image = pg.Surface((TILESIZE, TILESIZE))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()

	def activate(self):
		if not self.active:
			print("Active")
			self.active = True

	def destroy(self):
		if self.active:
			print("Destroy")
			self.active = False
