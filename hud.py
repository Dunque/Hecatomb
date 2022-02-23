import pygame as pg
from settings import *


class Interaccion(pg.sprite.Sprite):
	def __init__(self, scene, pos, image):
		self._layer = HUD_LAYER
		self.scene = scene
		self.groups = self.scene.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = pos

class CrossHair:
	def __init__(self, scene, image):
		self._layer = HUD_LAYER
		self.scene = scene
		self.groups = scene.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = pg.mouse.get_pos()

	def update(self):
		cam_moved = self.scene.camera.get_moved()

		mouse_x, mouse_y = pg.mouse.get_pos()

		mouse_x = mouse_x - cam_moved[0]
		mouse_y = mouse_y - cam_moved[1]
		self.rect.center = mouse_x, mouse_y

	def activate(self):
		self.add(self.scene.all_sprites)


class CrosshairGun(CrossHair, pg.sprite.Sprite):
	def __init__(self, scene):
		super().__init__(scene, scene.gunCrosshairImg)


class CrosshairShotGun(CrossHair, pg.sprite.Sprite):
	def __init__(self, scene):
		super().__init__(scene, scene.shotgunCrosshairImg)

