import pygame as pg
from cards import Card

from settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.player_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((TILESIZE, TILESIZE))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.pos = vec(x, y) * TILESIZE
		self.card = Card(game)

	def update(self):
		self.rect.topleft = (self.pos.x, self.pos.y)

	def on_click(self, mouse_pos):
		if int(self.pos.x / TILESIZE) == mouse_pos[0] and int(self.pos.y / TILESIZE) == mouse_pos[1]:
			self.show_card(self.game)
		else:
			self.hide_card(self.game)

	def show_card(self, game):
		self.card.activate()
		pg.sprite.Group.add(game.all_sprites, self.card)

	def hide_card(self, game):
		self.card.destroy()
		pg.sprite.Group.remove(game.all_sprites, self.card)


class Wall(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.walls
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((TILESIZE, TILESIZE))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.pos = vec(x, y)
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE


class Mouse(pg.sprite.Sprite):
	def __init__(self, game, pos):
		self.groups = game.all_sprites, game.walls
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.crosshair_img
		self.rect = self.image.get_rect()
		self.rect.x = pos[0] * TILESIZE
		self.rect.y = pos[1] * TILESIZE

	def update(self):
		cam_moved = self.game.camera.get_moved()
		x, y = pg.mouse.get_pos()
		relative_positions = x - cam_moved[0], y - cam_moved[1]
		tiled_position = vec(int(relative_positions[0] / TILESIZE), int(relative_positions[1] / TILESIZE))
		map_size = self.game.map.get_size()
		if relative_positions[0] < 0:
			tiled_position.x = 0
		elif relative_positions[0] > (map_size[0] - 1) * TILESIZE:
			tiled_position.x = map_size[0] - 1
		if relative_positions[1] < 0:
			tiled_position.y = 0
		elif relative_positions[1] > (map_size[1] - 1) * TILESIZE:
			tiled_position.y = map_size[1] - 1
		self.rect.topleft = (tiled_position.x * TILESIZE, tiled_position.y * TILESIZE)
