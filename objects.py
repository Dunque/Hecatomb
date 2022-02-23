import pygame as pg
from settings import *
from anim import Anim
from hud import Interaccion

vec = pg.math.Vector2


class Chest(pg.sprite.Sprite):
	def __init__(self, scene, x, y):
		self.scene = scene
		self._layer = WALL_LAYER
		self.groups = self.scene.all_sprites, self.scene.walls_SG
		pg.sprite.Sprite.__init__(self, self.groups)

		self.chestAnim = Anim(self.scene.chestImg, (96, 96), 10, 0, 1)
		self.image = self.chestAnim.get_frame()
		self.rect = self.image.get_rect()

		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE
		self.pos = vec(self.rect.x, self.rect.y)

	def update(self):
		player = pg.sprite.spritecollideany(self, self.scene.player_SG)
		if player:
			#print(self.pos, self.scene.player.pos)
			Interaccion(self.scene, self.pos, self.scene.abrirImg)