import pygame as pg
from settings import *


class Hud:
	def __init__(self,scene):
		self.scene = scene
		self.player = scene.player
		self.camera = scene.camera
	
	def draw_health_bar(self,surface, position, size, color_border, color_background, color_health, progress):
		pg.draw.rect(surface, color_background, (*position, *size))
		pg.draw.rect(surface, color_border, (*position, *size), 1)
		innerPos  = (position[0]+1, position[1]+1)
		innerSize = (int((size[0]-2) * progress), size[1]-2)
		pg.draw.rect(surface, color_health, (*innerPos, *innerSize))

	def draw_health(self, surf):
		self.draw_health_bar(surf, (20,20), (300,50), 
				(0, 0, 0), (0, 0, 0), (200, 50, 50), self.player.entityData.actualHP/self.player.entityData.maxHP) 

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

