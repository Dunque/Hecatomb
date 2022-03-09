import random

import pygame as pg
from src.settings.settings import *
from src.sprites.anim import Anim
from src.hud.hud import Interaccion, DialogoInGame

vec = pg.math.Vector2


class Chest(pg.sprite.Sprite):
	def __init__(self, scene, x, y, textLines = None):
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

		self.dialogo = None
		if textLines:
			with open(self.scene.dialogues_src) as f:
				for i, line in enumerate(f):
					if i == textLines:
						dialogue = line
			self.dialogo = DialogoInGame(self.scene, dialogue.rstrip("\n").split('\\n'), stopMove=True)

		self.opened = False
		self.talking = False

	def update(self):
		player = pg.sprite.spritecollideany(self, self.scene.player_SG)
		if player:
			if not self.opened:
				if not self.talking:
					self.interaccion.activate()
					if player.interact:
						self.open()
			else:
				if player.interact:
					self.talkFast()
				else:
					self.stopTalkFast()
		else:
			self.interaccion.deactivate()
			if self.talking:
				self.scene.completly_finished = False
			self.talking = False

	def open(self):
		self.opened = True
		self.talking = True
		self.talking = True
		self.interaccion.deactivate()
		self.chestAnim.current_frame = 1
		self.image = self.chestAnim.get_frame()
		if not self.scene.completly_finished:
			self.dialogo.drawText()

	def talkFast(self):
		if not self.scene.completly_finished:
			self.dialogo.drawText()
		else:
			self.dialogo.end()

	def stopTalkFast(self):
		self.dialogo.stopText()

	def kill(self):
		super(Chest, self).kill()
		self.interaccion.deactivate()


class Candelabro(pg.sprite.Sprite):
	def __init__(self, scene, x, y):
		self.scene = scene
		self._layer = WALL_LAYER
		self.groups = self.scene.all_sprites, self.scene.walls_SG, self.scene.candelabros_SG
		pg.sprite.Sprite.__init__(self, self.groups)

		self.candelabroAnim = Anim(self.scene.candelabroImg, (64, 64), 2, 0, 8)
		self.candelabroAnim.current_frame = random.randint(0, 7)
		self.image = self.candelabroAnim.get_frame()
		self.rect = self.image.get_rect()

		self.pos = vec(x, y)

		# tilemap position
		self.x = x
		self.y = y

		# Global position
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE

		self.isActive = False

	def update(self):
		if self.isActive:
			self.image = self.candelabroAnim.get_frame()


class Exit(pg.sprite.Sprite):
	def __init__(self, scene, x, y, textLines=None):
		self.scene = scene
		self._layer = WALL_LAYER
		self.groups = self.scene.all_sprites, self.scene.walls_SG
		pg.sprite.Sprite.__init__(self, self.groups)

		self.image = self.scene.exitImg
		self.rect = self.image.get_rect()

		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE
		self.pos = vec(self.rect.x, self.rect.y)
		self.interaccion = Interaccion(self.scene, self.pos, self.scene.abrirImg)

		self.opened = False
		self.talking = False

	def update(self):
		player = pg.sprite.spritecollideany(self, self.scene.player_SG)
		if player:
			if not self.opened:
				if not self.talking:
					self.interaccion.activate()
					if player.interact:
						self.open()
		else:
			self.interaccion.deactivate()

	def open(self):
		self.scene.nextScene("next")

