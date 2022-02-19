import pygame as pg
from settings import *
from operator import sub
from abc import ABC, abstractmethod

vec = pg.math.Vector2


class MenuManager(ABC):

	@abstractmethod
	def attach(self, observer):
		pass

	@abstractmethod
	def detach(self, observer):
		pass

	@abstractmethod
	def notify(self):
		pass


class Observer(ABC):

	@abstractmethod
	def update(self):
		pass


class WeaponMenu(MenuManager):
	def __init__(self, game):
		self.game = game

		self.image = self.game.playerSwordImg
		self.rect = self.image.get_rect()

		self.start_pos = vec(WIDTH / 2, HEIGHT / 2)

		self.is_active = False

		self._observers = []

		self.attach(WeaponMenuElement(self.game, 'top'))
		self.attach(WeaponMenuElement(self.game, 'down'))
		self.attach(WeaponMenuElement(self.game, 'left'))
		self.attach(WeaponMenuElement(self.game, 'right'))

		self.active_pos = None
		self.final_pos = None
		self.update()

	def attach(self, observer):
		self._observers.append(observer)

	def detach(self, observer):
		self._observers.remove(observer)

	def notify(self, notification):
		if notification == "update":
			for observer in self._observers:
				observer.update()
		elif notification == "hover":
			for observer in self._observers:
				observer.toggle_hover(self.active_pos)

	def update(self):
		if self.game.player and self.game.player.show_menu:
			self.toggle_menu(True)
			self.highlight()
		else:
			self.toggle_menu(False)
			if self.game.player:
				self.game.player.change_weapon(self.active_pos)

	def toggle_menu(self, visible):
		if visible:
			self.notify('update')
			[button.add(self.game.all_sprites) for button in self._observers]
			self.is_active = True
		else:
			[button.remove(self.game.all_sprites) for button in self._observers]
			self.is_active = False

	def highlight(self):
		mouse_pos = pg.mouse.get_pos()
		if ((WIDTH * mouse_pos[1]) / HEIGHT) > mouse_pos[0]:
			if ((mouse_pos[0] - WIDTH) / -WIDTH) * HEIGHT > mouse_pos[1]:
				self.active_pos = "left"
				self.notify("hover")
			else:
				self.active_pos = "down"
				self.notify("hover")
		else:
			if ((mouse_pos[0] - WIDTH) / -WIDTH) * HEIGHT > mouse_pos[1]:
				self.active_pos = "top"
				self.notify("hover")
			else:
				self.active_pos = "right"
				self.notify("hover")


class WeaponMenuElement(pg.sprite.Sprite, Observer):
	def __init__(self, game, pos):
		self.game = game
		pg.sprite.Sprite.__init__(self, [])

		height_dif = 0
		side_dif = 0
		self.scale = self.game.radialMenuImg.get_size()
		self.image = self.game.radialMenuImg
		self.rect = self.image.get_rect()
		self.pos_string = pos

		self.start_pos = vec(WIDTH / 2 + side_dif, HEIGHT / 2 + height_dif)
		self.orig_size = vec(self.image.get_rect()[2], self.image.get_rect()[3])
		if self.pos_string == 'right' or self.pos_string == 'left':
			self.orig_size = vec(self.orig_size[::-1])

		self.is_hovered = False
		self.hovered_x = 0
		self.hovered_y = 0

	def update(self):
		separation = 100
		side_dif = 0
		height_dif = 0
		if self.pos_string == 'top':
			height_dif = -separation
			self.image = pg.transform.smoothscale(self.game.radialMenuImg, self.scale)
		elif self.pos_string == 'down':
			height_dif = separation
			self.image = pg.transform.smoothscale(pg.transform.flip(self.game.radialMenuImg, False, True), self.scale)
		elif self.pos_string == 'left':
			side_dif = -separation + (self.orig_size[0] / 2)
			height_dif = - (self.orig_size[0] / 2)
			self.image = pg.transform.rotate(pg.transform.scale(self.game.radialMenuImg, self.scale), 90)
		elif self.pos_string == 'right':
			side_dif = separation + (self.orig_size[0] / 2)
			height_dif = - (self.orig_size[0] / 2)
			self.image = pg.transform.rotate(pg.transform.scale(self.game.radialMenuImg, self.scale), -90)

		cam_moved = self.game.camera.get_moved()
		self.pos = self.start_pos[0] - cam_moved[0] + side_dif + self.hovered_x, self.start_pos[1] - cam_moved[
			1] + height_dif + self.hovered_y
		self.rect.center = self.pos

	def hover(self):
		if not self.is_hovered:
			self.update()
			scale = 1.3
			self.scale = tuple([scale * x for x in self.scale])
			self.hovered_x = -int((self.image.get_rect()[2] * scale - self.orig_size.x) / 2)
			self.hovered_y = -int((self.image.get_rect()[3] * scale - self.orig_size.y) / 2)
			self.is_hovered = True

	def stop_hover(self):
		if self.is_hovered:
			if self.pos_string == 'right' or self.pos_string == 'left':
				self.scale = vec(self.orig_size[::-1])
			else:
				self.scale = self.orig_size
			self.hovered_x = 0
			self.hovered_y = 0
			self.is_hovered = False

	def toggle_hover(self, position):
		if position == self.pos_string:
			self.hover()
		else:
			self.stop_hover()
