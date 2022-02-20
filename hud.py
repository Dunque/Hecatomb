import pygame as pg


class CrosshairGun(pg.sprite.Sprite):
	def __init__(self, scene):
		self.scene = scene
		self.groups = scene.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.image = scene.gunCrosshairImg
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