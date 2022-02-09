import sys
import pygame as pg
from os import path
from settings import *
from sprites import Player, Wall, Mouse
from tilemap import Map, Camera


class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		pg.key.set_repeat(500, 100)
		self.load_data()

	def load_data(self):
		game_folder = path.dirname(__file__)
		image_folder = path.join(game_folder, 'img')
		self.map = Map(path.join(game_folder, 'map.txt'))
		self.crosshair_img = pg.image.load(path.join(image_folder, CROSSHAIR_IMG)).convert_alpha()

	def new(self):
		self.all_sprites = pg.sprite.Group()
		self.player_sprites = pg.sprite.Group()
		self.cards = pg.sprite.Group()
		self.mouse = pg.sprite.Group()
		self.walls = pg.sprite.Group()

		for row, tiles in enumerate(self.map.data):
			for col, tile in enumerate(tiles):
				if tile == '1':
					Wall(self, col, row)
				elif tile == 'P':
					self.player = Player(self, col, row)

		self.mouse = Mouse(self, pg.mouse.get_pos())
		self.camera = Camera(self.map.width, self.map.height)

	def run(self):
		# game loop - set self.playing = False to end the game
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.update()
			self.draw()

	def quit(self):
		pg.quit()
		sys.exit()

	def update(self):
		self.all_sprites.update()
		# self.camera.update(self.player)
		self.camera.update(pg.mouse.get_pos(), self.map)

	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):
			pg.draw.line(self.screen, RED, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pg.draw.line(self.screen, RED, (0, y), (WIDTH, y))

	def draw(self):
		self.screen.fill(GREY)
		#self.draw_grid()
		for sprite in self.all_sprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		pg.display.flip()

	# print(pg.mouse.get_pos()[0])

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()
			elif event.type == pg.MOUSEBUTTONUP:
				self.cast_click(self.camera.get_cell(pg.mouse.get_pos()))

	def cast_click(self, pos):
		for sprite in self.player_sprites:
			sprite.on_click(pos)

	def show_start_screen(self):
		pass

	def show_go_screen(self):
		pass


# create the game object
g = Game()
g.show_start_screen()
while True:
	g.new()
	g.run()
	g.show_go_screen()
