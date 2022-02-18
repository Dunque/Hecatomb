import pygame as pg
from settings import *
from operator import sub
vec = pg.math.Vector2


class WeaponMenu:
	def __init__(self, game):
		self.game = game

		self.image = self.game.playerSwordImg
		self.rect = self.image.get_rect()

		self.start_pos = vec(WIDTH / 2, HEIGHT / 2)

		self.is_active = False

		self.update()

		self.top_option = WeaponMenuElement(self.game, 'top')
		self.down_option = WeaponMenuElement(self.game, 'down')
		self.left_option = WeaponMenuElement(self.game, 'left')
		self.right_option = WeaponMenuElement(self.game, 'right')

		self.active_pos = None
		self.final_pos = None

	def update(self):
		if self.is_active:
			self.highlight()
			if pg.mouse.get_pressed()[0]:
				self.toggle_menu()
				#self.final_pos = self.active_pos
				self.game.player.change_weapon(self.active_pos)

	def toggle_menu(self):
		if not self.is_active:
			self.top_option.add(self.game.all_sprites)
			self.down_option.add(self.game.all_sprites)
			self.left_option.add(self.game.all_sprites)
			self.right_option.add(self.game.all_sprites)
			self.is_active = True
		else:
			self.top_option.remove(self.game.all_sprites)
			self.down_option.remove(self.game.all_sprites)
			self.left_option.remove(self.game.all_sprites)
			self.right_option.remove(self.game.all_sprites)
			self.is_active = False

	def highlight(self):
		mouse_pos = pg.mouse.get_pos()
		if ((WIDTH * mouse_pos[1]) / HEIGHT) > mouse_pos[0]:
			if ((mouse_pos[0] - WIDTH) / -WIDTH) * HEIGHT > mouse_pos[1]:
				self.active_pos = 3  # Izquierda
				self.left_option.hover()
				self.top_option.stop_hover()
				self.down_option.stop_hover()
				self.right_option.stop_hover()
			else:
				self.active_pos = 2  # Abajo
				self.down_option.hover()
				self.top_option.stop_hover()
				self.left_option.stop_hover()
				self.right_option.stop_hover()
		else:
			if ((mouse_pos[0] - WIDTH) / -WIDTH) * HEIGHT > mouse_pos[1]:
				self.active_pos = 0  # Arriba
				self.top_option.hover()
				self.down_option.stop_hover()
				self.left_option.stop_hover()
				self.right_option.stop_hover()
			else:
				self.active_pos = 1  # Derecha
				self.right_option.hover()
				self.top_option.stop_hover()
				self.down_option.stop_hover()
				self.left_option.stop_hover()


class WeaponMenuElement(pg.sprite.Sprite, WeaponMenu):
	def __init__(self, game, pos):
		self.game = game
		pg.sprite.Sprite.__init__(self, [])

		height_dif = 0
		side_dif = 0
		self.scale = self.game.radialMenuImg.get_size()
		self.image = self.game.radialMenuImg
		self.rect = self.image.get_rect()
		self.pos_string = pos

		self.rect = self.image.get_rect()
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
			self.image = pg.transform.smoothscale(pg.transform.flip(
				self.game.radialMenuImg, False, True), self.scale)
		elif self.pos_string == 'left':
			side_dif = -separation + (self.orig_size[0] / 2)
			height_dif = - (self.orig_size[0] / 2)
			self.image = pg.transform.rotate(
				pg.transform.scale(self.game.radialMenuImg, self.scale), 90)
		elif self.pos_string == 'right':
			side_dif = separation + (self.orig_size[0] / 2)
			height_dif = - (self.orig_size[0] / 2)
			self.image = pg.transform.rotate(
				pg.transform.scale(self.game.radialMenuImg, self.scale), -90)

		cam_moved = self.game.camera.get_moved()
		self.pos = self.start_pos[0] - cam_moved[0] + side_dif + \
                    self.hovered_x, self.start_pos[1] - \
                    cam_moved[1] + height_dif + self.hovered_y
		self.rect.center = self.pos

	def hover(self):
		if not self.is_hovered:
			scale = 1.3
			self.scale = tuple([scale*x for x in self.scale])
			self.hovered_x = - \
				int((self.image.get_rect()[2]*scale - self.orig_size.x) / 2)
			self.hovered_y = - \
				int((self.image.get_rect()[3]*scale - self.orig_size.y) / 2)
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
