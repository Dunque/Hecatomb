import pygame as pg
from src.settings.settings import *
from src.sprites.anim import *
import time


class Hud:
	def __init__(self, scene):
		self.scene = scene
		self.player = scene.player
		self.camera = scene.camera
		self.dineros = Dineros(scene)
		self.text_menu = None
		self.draw_dineros = False
		self.has_menu = False
		self.time_dineros = None
		self.show_time_dineros = 3
		self.dialogue_line_y_offsets = [250, 300, 350]
		self.menu_line_y_offsets = [-130, -70, -10, 50, 140, 250]
		self.resetDialogue()

	def draw_health_bar(self, surface, position, size, color_border, color_background, color_health, progress):
		pg.draw.rect(surface, color_background, (*position, *size))
		pg.draw.rect(surface, color_border, (*position, *size), 1)
		innerPos = (position[0] + 1, position[1] + 1)
		innerSize = (int((size[0] - 2) * progress), size[1] - 2)
		pg.draw.rect(surface, color_health, (*innerPos, *innerSize))

	def draw_health(self, surf):
		self.draw_health_bar(surf, (20, 20), (300, 50),
							 WHITE, BLACK, (180, 50, 0), self.player.entityData.actualHP / self.player.entityData.maxHP)

	def drawDialogue(self):
		if not self.dialogue_cooldown and self.dialogue:
			letter = self.dialogue.pop(0)
			self.dialogue_cooldown = 5
			self.text_lines[self.dialogue_line].append(letter)
		if self.dialogue_cooldown:
			self.dialogue_cooldown -= 1

		phrases = [''.join(line) for line in self.text_lines]
		text_surfaces = [self.scene.game_font.render(phrase, WHITE)[0] for phrase in phrases]
		for i in range(len(text_surfaces)):
			self.scene.screen.blit(text_surfaces[i], (WIDTH / 2 - 500, (HEIGHT / 2) + self.dialogue_line_y_offsets[i]))

		if self.active_dialogue and len(self.text_lines[self.dialogue_line]) >= self.dialogue_length:
			if len(self.remainder_dialogue) > 0:
				self.active_dialogue = False
				self.dialogue_line += 1
				self.updateDialogue(self.remainder_dialogue)
			else:
				self.dialogue_continuation = True

	def updateDialogue(self, textLine):
		self.dialogue_continuation = False
		if not self.active_dialogue:
			self.completly_finished = False
			if self.dialogue_line == 0:
				self.firstBatch = textLine[:3]
				self.remainderBatch = textLine[3:]
				self.total_lines_batch = len(self.firstBatch)
				textLine = self.firstBatch

			self.player.stopMovement()
			self.active_dialogue = True
			self.dialogue = list(textLine[0])
			self.remainder_dialogue = textLine[1:]
			self.dialogue_length = len(self.dialogue)
		elif self.dialogue_line == self.total_lines_batch - 1 and len(
				self.text_lines[self.dialogue_line]) >= self.dialogue_length and not self.skip_dialogue:
			self.active_dialogue = False
			if not self.has_menu:
				self.text_lines[0] = []
				self.text_lines[1] = []
				self.text_lines[2] = []
			self.dialogue_line = 0
			if len(self.remainderBatch) > 0:
				self.updateDialogue(self.remainderBatch)
			else:
				self.completly_finished = True
		elif len(self.text_lines[0]) >= 2:
			self.skip_dialogue = True
			self.dialogue_cooldown = 0

	def stopText(self):
		self.skip_dialogue = False

	def resetDialogue(self):
		self.dialogue = None
		self.remainder_dialogue = None
		self.active_dialogue = False
		self.skip_dialogue = False
		self.dialogue_cooldown = 0
		self.text_line0 = []
		self.text_line1 = []
		self.text_line2 = []
		self.text_lines = [self.text_line0, self.text_line1, self.text_line2]
		self.dialogue_length = 0
		self.dialogue_line = 0
		self.completly_finished = False
		self.dialogue_continuation = False
		if self.player:
			self.player.allowMovement()

	def drawMenu(self):
		if self.text_menu:
			phrase_dialogue = ''.join(self.text_line0)
			text_surface,_ = self.scene.game_font.render(phrase_dialogue, WHITE)
			self.scene.screen.blit(text_surface, (WIDTH / 2 - 500, (HEIGHT / 2) + 250))
			phrases = self.text_menu
			text_surfaces = [self.scene.game_font.render(phrase, WHITE)[0] for phrase in phrases]
			for i in range(len(text_surfaces)):
				self.scene.screen.blit(text_surfaces[i], (WIDTH / 2 + 230, (HEIGHT / 2) + self.menu_line_y_offsets[i]))

	def drawDineros(self):
		if self.draw_dineros:
			if not self.time_dineros:
				self.time_dineros = time.time()
			time_fin = time.time()
			self.dineros.activate()
			text_surface5, rect5 = self.scene.game_font.render(str(self.player.entityData.los_dineros) + '$', (200, 200, 200))
			self.scene.screen.blit(text_surface5, (WIDTH / 2 - 680, (HEIGHT / 2) - 340))
			if time_fin - self.time_dineros > self.show_time_dineros:
				self.draw_dineros = False
				self.time_dineros = None
				self.dineros.deactivate()


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
			self.add(self.scene.all_hud)

	def deactivate(self):
		if self.visible:
			self.visible = False
			self.remove(self.scene.all_hud)


class CrossHair:
	def __init__(self, scene, image):
		self._layer = HUD_LAYER
		self.scene = scene
		self.groups = scene.all_hud
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
		self.add(self.scene.all_hud)


class CrosshairGun(CrossHair, pg.sprite.Sprite):
	def __init__(self, scene):
		super().__init__(scene, scene.gunCrosshairImg)


class CrosshairShotGun(CrossHair, pg.sprite.Sprite):
	def __init__(self, scene):
		super().__init__(scene, scene.shotgunCrosshairImg)


class Dineros(pg.sprite.Sprite):
	def __init__(self, scene):
		self._layer = HUD_LAYER
		self.scene = scene
		pg.sprite.Sprite.__init__(self, [])
		self.image = self.scene.dinerosImg
		self.rect = self.image.get_rect()
		self.x = (WIDTH / 2) - 740
		self.y = (HEIGHT / 2) - 330
		self.rect.center = self.x, self.y

	def update(self):
		cam_moved = self.scene.camera.get_moved()
		pos_x = (WIDTH / 2) - cam_moved[0] - 740
		pos_y = (HEIGHT / 2) - cam_moved[1] - 330
		self.rect.center = pos_x, pos_y

	def activate(self):
		self.scene.all_hud.add(self)

	def deactivate(self):
		self.scene.all_hud.remove(self)


class Line:
	def __init__(self, text, line, last):
		self.text = text
		self.line = line
		self.last = last


class OptionPicker(pg.sprite.Sprite):
	def __init__(self, scene):
		self._layer = HUD_LAYER
		self.scene = scene
		pg.sprite.Sprite.__init__(self, [])
		self.image = self.scene.dialogueOptionsPicker
		self.rect = self.image.get_rect()
		self.yOffsets = [-120, -60, 0, 60, 150]
		self.x = 1010
		self.y = self.yOffsets[0]
		self.rect.center = self.x, self.y

		self.option = 0

	def update(self):
		cam_moved = self.scene.camera.get_moved()
		pos_x = (WIDTH / 2) - cam_moved[0] + 200
		pos_y = (HEIGHT / 2) - cam_moved[1]
		if pg.mouse.get_pos()[1] < 366:
			self.y = self.yOffsets[0] + pos_y
			self.option = 0
		elif pg.mouse.get_pos()[1] < 431:
			self.y = self.yOffsets[1] + pos_y
			self.option = 1
		elif pg.mouse.get_pos()[1] < 491:
			self.y = self.yOffsets[2] + pos_y
			self.option = 2
		elif pg.mouse.get_pos()[1] < 571:
			self.y = self.yOffsets[3] + pos_y
			self.option = 3
		else:
			self.y = self.yOffsets[4] + pos_y
			self.option = 4
		self.rect.center = pos_x, self.y

	def activate(self):
		self.scene.all_hud.add(self)

	def deactivate(self):
		self.scene.all_hud.remove(self)
		self.scene.hud.text_menu = []


class DialogueOptions(pg.sprite.Sprite):
	def __init__(self, scene, options=None):
		self._layer = HUD_LAYER
		self.scene = scene
		pg.sprite.Sprite.__init__(self, [])
		self.image = self.scene.dialogueOptions
		self.rect = self.image.get_rect()
		self.rect.center = HEIGHT - 300, -400
		self.text = options
		self.picker = OptionPicker(scene)
		self.opcion = None

	def update(self):
		self.scene.hud.draw_dineros = True
		cam_moved = self.scene.camera.get_moved()
		y_offset = 10
		pos_x = (WIDTH / 2) - cam_moved[0] + 350
		pos_y = (HEIGHT / 2) - cam_moved[1] + y_offset
		self.rect.center = pos_x, pos_y
		self.scene.hud.text_menu = self.text

		mouse = pg.mouse.get_pressed()
		if mouse[0]:
			self.opcion = self.picker.option
			# self.scene.hud.completly_finished = True
			self.scene.hud.resetDialogue()

	def activate(self):
		self.scene.all_hud.add(self)
		self.picker.activate()

	def deactivate(self):
		self.scene.all_hud.remove(self)
		self.picker.deactivate()


class ProfileBoxDialogue(pg.sprite.Sprite):
	def __init__(self, scene, profileImg):
		self._layer = HUD_LAYER
		self.scene = scene
		pg.sprite.Sprite.__init__(self, [])
		self.anim = Anim(profileImg, (155, 155), 15, 0, 2)
		self.image = self.anim.get_frame()
		self.rect = self.image.get_rect()
		self.rect.center = HEIGHT - 300, -400

	def update(self):
		cam_moved = self.scene.camera.get_moved()
		y_offset = 137
		pos_x = (WIDTH / 2) - cam_moved[0] - 400
		pos_y = (HEIGHT / 2) - cam_moved[1] + y_offset
		self.rect.center = pos_x, pos_y

		if self.scene.hud.dialogue:
			self.image = self.anim.get_frame()
		else:
			self.image = self.anim.frames[0]

	def activate(self):
		self.scene.all_hud.add(self)

	def deactivate(self):
		self.scene.all_hud.remove(self)


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
		self.scene.all_hud.add(self)

	def deactivate(self):
		self.scene.all_hud.remove(self)


class DialogoInGame(pg.sprite.Sprite):
	def __init__(self, scene, text, stopMove=False, profileImg=None, options=None):
		self._layer = HUD_LAYER
		self.scene = scene
		pg.sprite.Sprite.__init__(self, [])
		self.image = self.scene.dialogueBox
		self.rect = self.image.get_rect()
		self.rect.center = HEIGHT - 300, 200
		self.text = text
		self.stopMove = stopMove
		self.continuation = ContinuationDialogue(scene)
		if options is not None:
			self.opciones = DialogueOptions(scene, options)
			self.opcion_escoger = None
		else:
			self.opciones = None

		self.profileBox = None
		if profileImg:
			self.profileBox = ProfileBoxDialogue(scene, profileImg)

	def update(self):
		cam_moved = self.scene.camera.get_moved()
		y_offset = 315
		pos_x = (WIDTH / 2) - cam_moved[0]
		pos_y = (HEIGHT / 2) - cam_moved[1] + y_offset
		self.rect.center = pos_x, pos_y

		if self.scene.hud.dialogue_continuation and len(self.scene.hud.remainderBatch) > 0:
			self.continuation.activate()
		else:
			self.continuation.deactivate()

		if self.opciones and self.opciones.opcion is not None:
			self.opcion_escoger = self.opciones.opcion
			self.opciones.deactivate()
			self.end()

	def drawText(self):
		self.scene.all_hud.add(self)
		if self.profileBox:
			self.profileBox.activate()
		self.scene.hud.updateDialogue(self.text)

	def stopText(self):
		self.scene.hud.stopText()

	def end(self):
		self.scene.all_hud.remove(self)
		if self.profileBox:
			self.profileBox.deactivate()
		self.continuation.deactivate()
		if self.opciones:
			self.opciones.deactivate()
		self.scene.hud.dialogue = None
		self.scene.hud.text_lines[0] = []
		self.scene.hud.resetDialogue()

	def showOptions(self):
		self.opciones.activate()
