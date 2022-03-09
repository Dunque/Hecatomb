import pygame as pg
from src.sprites.anim import *
from src.entities.character import *
from src.entities.states.enemystates import *
from src.hud.hud import Interaccion, DialogoInGame

vec = pg.math.Vector2

class NPCBase(Character):
	def __init__(self, scene, x, y, textLines, anims = None):
		if not anims:
			# Aniamtion stuff
			idleAnim = Anim(scene.playerIdleSheet,
							(CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 4)
		else:
			idleAnim = anims

		animList = [idleAnim, idleAnim, idleAnim, idleAnim, idleAnim]

		super(NPCBase, self).__init__(scene, x, y, animList,
									 (scene.all_sprites, scene.npc_SG), PlayerStats())
		self.acc = vec(0, 0)
		self.rect.center = self.pos
		self.state = EnemyGroundedState(self, "GROUNDED")

		self.pos = vec(self.rect.x + 50, self.rect.y)
		self.profileImg = self.scene.npc1Profile
		self.interaccion = Interaccion(self.scene, self.pos, self.scene.hablarImg)
		with open(self.scene.dialogues_src) as f:
			for i, line in enumerate(f):
				if i == textLines:
					dialogue = line
		self.dialogo = DialogoInGame(self.scene, dialogue.rstrip("\n").split('\\n'), stopMove=True, profileImg=self.profileImg)
		self.talking = False
		self.right = True

	def update(self):
		player = pg.sprite.spritecollideany(self, self.scene.player_SG)
		if player:
			if not self.talking:
				self.interaccion.activate()
				if player.interact:
					self.talk()
			elif player.interact:
					self.talkFast()
			else:
				self.stopTalkFast()
		else:
			self.interaccion.deactivate()
			if self.talking:
				self.scene.completly_finished = False
			self.talking = False

	def talk(self):
		self.talking = True
		print(self.scene.player.rect)
		print(self.rect)
		if self.rect.x > self.scene.player.rect.x and self.right:
			self.image = pg.transform.flip(self.image, True, False)
			self.right = False
		elif self.rect.x < self.scene.player.rect.x and not self.right:
			self.image = pg.transform.flip(self.image, True, False)
			self.right = True
		self.interaccion.deactivate()
		if not self.scene.completly_finished:
			self.dialogo.drawText()

	def talkFast(self):
		if not self.scene.completly_finished:
			self.dialogo.drawText()
		else:
			self.dialogo.end()

	def stopTalkFast(self):
		self.dialogo.stopText()
