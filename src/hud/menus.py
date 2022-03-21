import pygame as pg
from src.settings.settings import *
from operator import sub
from abc import ABC, abstractmethod
from src.weapons.weapons import Gun, Shotgun, Sword

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
	def __init__(self, scene):
		self.scene = scene

		self.image = self.scene.playerSwordImg
		self.rect = self.image.get_rect()

		self.start_pos = vec(WIDTH / 2, HEIGHT / 2)

		self.is_active = False

		self._observers = []

		self.top_element = WeaponMenuElement(self.scene, 'top')
		self.down_element = WeaponMenuElement(self.scene, 'down')
		self.left_element = WeaponMenuElement(self.scene, 'left')
		self.right_element = WeaponMenuElement(self.scene, 'right')

		self.attach(self.down_element)

		self.active_pos = None
		self.final_pos = None
		self.update()

	def add_weapon(self, weapon):
		if weapon is Gun:
			self.attach(self.top_element)
		elif weapon is Shotgun:
			self.attach(self.left_element)
		elif weapon is Sword:
			self.attach(self.right_element)

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
		if self.scene.player and self.scene.player.show_menu:
			self.toggle_menu(True)
			self.highlight()
		else:
			self.toggle_menu(False)
			if self.scene.player:
				self.scene.player.change_weapon(self.active_pos)

	def toggle_menu(self, visible):
		if visible:
			self.notify('update')
			[button.add(self.scene.all_hud) for button in self._observers]
			self.is_active = True
		else:
			[button.remove(self.scene.all_hud) for button in self._observers]
			self.is_active = False

	def highlight(self):
		mouse_pos = pg.mouse.get_pos()
		if ((WIDTH * mouse_pos[1]) / HEIGHT) > mouse_pos[0]:
			if ((mouse_pos[0] - WIDTH) / -WIDTH) * HEIGHT > mouse_pos[1] and self.left_element in self._observers:
				self.active_pos = "left"
				self.notify("hover")
			elif ((mouse_pos[0] - WIDTH) / -WIDTH) * HEIGHT < mouse_pos[1]:
				self.active_pos = "down"
				self.notify("hover")
		else:
			if ((mouse_pos[0] - WIDTH) / -WIDTH) * HEIGHT > mouse_pos[1] and self.top_element in self._observers:
				self.active_pos = "top"
				self.notify("hover")
			elif self.right_element in self._observers:
				self.active_pos = "right"
				self.notify("hover")


class WeaponMenuElement(pg.sprite.Sprite, Observer):
	def __init__(self, scene, pos):
		self._layer = HUD_LAYER
		self.scene = scene
		pg.sprite.Sprite.__init__(self, [])

		height_dif = 0
		side_dif = 0
		self.scale = self.scene.radialMenuImg.get_size()
		self.pos_string = pos

		if self.pos_string == 'right':
			self.image = self.scene.swordRadialMenuImg
		elif self.pos_string == 'left':
			self.image = self.scene.shotgunRadialMenuImg
		elif self.pos_string == 'top':
			self.image = self.scene.gunRadialMenuImg
		elif self.pos_string == 'down':
			self.image = self.scene.manoRadialMenuImg
		self.rect = self.image.get_rect()


		self.start_pos = vec(WIDTH / 2 + side_dif, HEIGHT / 2 + height_dif)
		self.orig_size = vec(self.image.get_rect()[2], self.image.get_rect()[3])


		self.is_hovered = False
		self.hovered_x = 0
		self.hovered_y = 0

	def update(self):
		separation = 100
		side_dif = 0
		height_dif = 0
		if self.pos_string == 'top':
			height_dif = -separation
			self.image = pg.transform.smoothscale(self.scene.gunRadialMenuImg, self.scale)
		elif self.pos_string == 'down':
			height_dif = separation
			self.image = pg.transform.smoothscale(self.scene.manoRadialMenuImg, self.scale)
		elif self.pos_string == 'left':
			side_dif = -100
			height_dif = 0
			self.image = pg.transform.scale(self.scene.shotgunRadialMenuImg, (self.scale[1],self.scale[0]))
		elif self.pos_string == 'right':
			side_dif = 100
			height_dif = 0
			self.image = pg.transform.scale(self.scene.swordRadialMenuImg, (self.scale[1],self.scale[0]))

		cam_moved = self.scene.camera.get_moved()
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
