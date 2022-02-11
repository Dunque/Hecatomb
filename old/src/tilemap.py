import pygame as pg
from .settings import *

vec = pg.math.Vector2


class Map:
	def __init__(self, filename):
		self.data = []
		self.min_x, self.max_x, self.min_y, self.max_y = 0, 0, 0, 0
		with open(MAP_DIR+filename, 'rt') as map_file:
			for line in map_file:
				if line.startswith("[DATA]") or line == "\n":
					break
				self.data.append(line.strip())
			for data in map_file:
				data_array = data.strip().split("=")
				if data_array[0].strip() == 'min_x':
					self.min_x = int(data_array[1])
				elif data_array[0].strip() == 'max_x':
					self.max_x = int(data_array[1])
				elif data_array[0].strip() == 'min_y':
					self.min_y = int(data_array[1])
				elif data_array[0].strip() == 'max_y':
					self.max_y = int(data_array[1])

		self.tilewidth = len(self.data[0])
		self.tileheight = len(self.data)
		self.width = self.tilewidth * TILESIZE
		self.height = self.tileheight * TILESIZE

	def get_size(self):
		return self.tilewidth, self.tileheight


class Camera:
	def __init__(self, width, height):
		self.camera = pg.Rect(0, 0, width, height)
		self.width_height = vec(width,height)
		self.halfs = vec(int(WIDTH / 2), int(HEIGHT / 2))
		self.def_cords = vec(CAMERA_X, CAMERA_Y)
		self.border = vec(X_BORDER, Y_BORDER)
		self.multiplier = MOVEMENT_MULTIPLIER

	def get_cell(self, pos):
		return int((pos[0] / TILESIZE) - (self.def_cords.x / TILESIZE)), int((pos[1] / TILESIZE) - (self.def_cords.y / TILESIZE))

	def get_moved(self):
		return self.def_cords.x, self.def_cords.y

	def apply(self, entity):
		return entity.rect.move(self.camera.topleft)

	def update(self, target, map_cords):
		x = -target[0] + self.halfs.x
		y = -target[1] + self.halfs.y
		x_limit = (self.border.x * self.halfs.x) / 100
		y_limit = (self.border.y * self.halfs.y) / 100

		if x > x_limit and map_cords.max_x > self.def_cords.x:
			multiplier = int((x - x_limit) / ((self.halfs.x - x_limit) / self.multiplier))
			self.def_cords.x += 1 * multiplier
		elif x < -x_limit and map_cords.min_x < self.def_cords.x:
			multiplier = int((-x - x_limit) / ((self.halfs.x - x_limit) / self.multiplier))
			self.def_cords.x -= 1 * multiplier
		if y > y_limit and map_cords.max_y > self.def_cords.y:
			multiplier = int((y - y_limit) / ((self.halfs.y - y_limit) / self.multiplier))
			self.def_cords.y += 1 * multiplier
		elif y < -y_limit and map_cords.min_y < self.def_cords.y:
			multiplier = int((-y - y_limit) / ((self.halfs.y - y_limit) / self.multiplier))
			self.def_cords.y -= 1 * multiplier

		self.camera = pg.Rect(self.def_cords.x, self.def_cords.y, self.width_height.x, self.width_height.y)
