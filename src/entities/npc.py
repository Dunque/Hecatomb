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
			idleAnim = Anim(scene.playerIdleSheet, (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 4)
			talkingAnim = Anim(scene.playerTalkingSheet, (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 4)
		else:
			idleAnim = anims

		self.animList = [idleAnim, talkingAnim, idleAnim, idleAnim, idleAnim]
		self.currentAnim=self.animList[0]

		super(NPCBase, self).__init__(scene, x, y, self.animList,
									 (scene.all_sprites, scene.npc_SG), PlayerStats())
		self.acc = vec(0, 0)
		self.rect.center = self.pos
		self.state = EnemyGroundedState(self, "GROUNDED")

		self.pos = vec(self.rect.x + 50, self.rect.y)
		self.profileImg = self.scene.npc1Profile
		self.interaccion = Interaccion(self.scene, self.pos, self.scene.hablarImg)
		with open(self.scene.dialogues_src,encoding='utf-8') as f:
			for i, line in enumerate(f):
				if i == textLines:
					dialogue = line
		self.dialogo = DialogoInGame(self.scene, dialogue.rstrip("\n").split('\\n'), stopMove=True, profileImg=self.profileImg)
		self.talking = False
		self.right = True

		self.talked = False

	def update(self):
		if self.right:
			self.image = pg.transform.flip(self.currentAnim.get_frame(), False, False)
		else:
			self.image = pg.transform.flip(self.currentAnim.get_frame(), True, False)
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
			self.currentAnim = self.animList[0]

		if not self.talking or self.scene.dialogue_continuation:
			self.currentAnim = self.animList[0]
		else:
			self.currentAnim = self.animList[1]

	def talk(self):
		#boolean to check if player hs interacted with the npc
		self.talked = True
		#Boolean to trigger the talking logic
		self.talking = True

		self.currentAnim = self.animList[1]
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
			self.currentAnim = self.animList[1]
			self.scene.completly_finished = True

	def stopTalkFast(self):
		self.dialogo.stopText()
