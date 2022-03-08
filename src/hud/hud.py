import pygame as pg
from src.settings.settings import *
from src.sprites.anim import *


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


class Interaccion(pg.sprite.Sprite):
	def __init__(self, scene, pos, image):
		self._layer = HUD_LAYER
		self.scene = scene
		pg.sprite.Sprite.__init__(self, [])
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = pos

		self.visible = False

	def activate(self):
		if not self.visible:
			self.visible = True
			self.add(self.scene.all_sprites)

	def deactivate(self):
		if self.visible:
			self.visible = False
			self.remove(self.scene.all_sprites)


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


class Line:
	def __init__(self, text, line, last):
		self.text = text
		self.line = line
		self.last = last


class ProfileBoxDialogue(pg.sprite.Sprite):
	def __init__(self, scene, profileImg):
		self._layer = HUD_LAYER
		self.scene = scene
		pg.sprite.Sprite.__init__(self, [])
		self.anim = Anim(profileImg, (157, 155), 15, 0, 2)
		self.image = self.anim.get_frame()
		self.rect = self.image.get_rect()
		self.rect.center = HEIGHT - 300, -400

	def update(self):
		cam_moved = self.scene.camera.get_moved()
		y_offset = 137
		pos_x = (WIDTH / 2) - cam_moved[0] - 400
		pos_y = (HEIGHT / 2) - cam_moved[1] + y_offset
		self.rect.center = pos_x, pos_y

		if self.scene.dialogue:
			self.image = self.anim.get_frame()
		else:
			self.image = self.anim.frames[0]

	def activate(self):
		self.scene.all_sprites.add(self)

	def deactivate(self):
		self.scene.all_sprites.remove(self)


class ContinuationDialogue(pg.sprite.Sprite):
	def __init__(self, scene):
		self._layer = HUD_LAYER
		self.scene = scene
		pg.sprite.Sprite.__init__(self, [])
		self.image = self.scene.dialogueContinuation
		self.rect = self.image.get_rect()
		self.rect.center = HEIGHT + 390, 460

	def update(self):
		cam_moved = self.scene.camera.get_moved()
		y_offset = 390
		pos_x = (WIDTH / 2) - cam_moved[0] + 460
		pos_y = (HEIGHT / 2) - cam_moved[1] + y_offset
		self.rect.center = pos_x, pos_y

	def activate(self):
		self.scene.all_sprites.add(self)

	def deactivate(self):
		self.scene.all_sprites.remove(self)


class DialogoInGame(pg.sprite.Sprite):
	def __init__(self, scene, text, stopMove = False, profileImg = None):
		self._layer = HUD_LAYER
		self.scene = scene
		pg.sprite.Sprite.__init__(self, [])
		self.image = self.scene.dialogueBox
		self.rect = self.image.get_rect()
		self.rect.center = HEIGHT - 300, 200
		self.text = text
		self.stopMove = stopMove
		self.continuation = ContinuationDialogue(scene)

		self.profileBox = None
		if profileImg:
			self.profileBox = ProfileBoxDialogue(scene, profileImg)

	def update(self):
		cam_moved = self.scene.camera.get_moved()
		y_offset = 315
		pos_x = (WIDTH / 2) - cam_moved[0]
		pos_y = (HEIGHT / 2) - cam_moved[1] + y_offset
		self.rect.center = pos_x, pos_y

		if self.scene.dialogue_continuation and len(self.scene.remainderBatch) > 0:
			self.continuation.activate()
		else:
			self.continuation.deactivate()

	def drawText(self):
		self.scene.all_sprites.add(self)
		if self.profileBox:
			self.profileBox.activate()
		self.scene.updateDialogue(self.text)

	def stopText(self):
		self.scene.stopText()

	def end(self):
		self.scene.all_sprites.remove(self)
		if self.profileBox:
			self.profileBox.deactivate()
		self.continuation.deactivate()
