import pygame as pg
from src.settings.settings import *
from src.sprites.anim import Anim
from src.hud.hud import Interaccion

vec = pg.math.Vector2


class Chest(pg.sprite.Sprite):
	def __init__(self, scene, x, y):
		self.scene = scene
		self._layer = WALL_LAYER
		self.groups = self.scene.all_sprites, self.scene.walls_SG
		pg.sprite.Sprite.__init__(self, self.groups)

		self.chestAnim = Anim(self.scene.chestImg, (96, 96), 10, 0, 2)
		self.image = self.chestAnim.get_frame()
		self.rect = self.image.get_rect()

		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE
		self.pos = vec(self.rect.x + 50, self.rect.y)
		self.interaccion = Interaccion(self.scene, self.pos, self.scene.abrirImg)

		self.opened = False

	def update(self):
		if not self.opened:
			player = pg.sprite.spritecollideany(self, self.scene.player_SG)
			if player:
				self.interaccion.activate()
				if player.interact:
					self.open()
			else:
				self.interaccion.deactivate()

	def open(self):
		self.opened = True
		self.interaccion.deactivate()
		self.chestAnim.current_frame = 1
		self.image = self.chestAnim.get_frame()
