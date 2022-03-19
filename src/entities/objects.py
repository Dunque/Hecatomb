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
			with open(self.scene.dialogues_src,encoding='utf-8') as f:
				for i, line in enumerate(f):
					if i == textLines:
						dialogue = line.rstrip("\n").split('\\n')
			self.value = random.randint(3,5) * 100
			dialogue[0] += ' ' + str(self.value) + ' RUBLOS.'
			self.dialogo = DialogoInGame(self.scene, dialogue, stopMove=True)

		self.opened = False
		self.talking = False
		self.isActive = False
		self.interacted = False
		self.dineros_given = False

	def update(self):
		if self.isActive:
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
				if self.opened:
					self.interacted = True

	def open(self):
		self.opened = True
		self.talking = True
		self.interaccion.deactivate()
		self.chestAnim.current_frame = 1
		self.image = self.chestAnim.get_frame()
		if not self.scene.completly_finished:
			self.dialogo.drawText()

	def talkFast(self):
		if not self.scene.completly_finished:
			if not self.interacted:
				self.dialogo.drawText()
		else:
			self.dialogo.end()
			self.scene.completly_finished = True
			if not self.dineros_given:
				self.scene.player.mas_dineros(round(self.value / 107.75, 2))
				self.dineros_given = True
				self.scene.drawDineros()

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

		self.candelabroAnim = Anim(self.scene.candelabroImg, (64, 64), 5, 0, 8)
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

	def update(self):
		self.image = self.candelabroAnim.get_frame()


class Exit(pg.sprite.Sprite):
	def __init__(self, scene, x, y):
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
		if self.scene.canExit:
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
		self.scene.nextScene()


class Medkit(pg.sprite.Sprite):
	def __init__(self, scene, x, y, healAmount):
		self.scene = scene
		self._layer = WALL_LAYER
		self.groups = self.scene.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)

		self.image = self.scene.medkitImg
		self.rect = self.image.get_rect()

		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE
		self.pos = vec(self.rect.x, self.rect.y)
		self.interaccion = Interaccion(self.scene, self.pos, self.scene.abrirImg)

		self.healAmount = healAmount
		self.isActive = False

	def update(self):
		if self.isActive:
			player = pg.sprite.spritecollideany(self, self.scene.player_SG)
			if player:
				self.interaccion.activate()
				if player.interact:
					self.interaccion.deactivate()
					self.healPlayer()
					#TODO SOUND healing	
					self.kill()	
			else:
				self.interaccion.deactivate()

	def healPlayer(self):
		self.scene.HEAL_SOUND.play()
		self.scene.player.entityData.heal(self.healAmount)
