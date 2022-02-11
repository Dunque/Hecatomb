import sys
import pygame as pg
from os import path
from pygame.locals import *
from src.settings import *
from src.sprites import Player, Wall, Mouse
from src.tilemap import Map, Camera
from src.scenes.scene import Scene

class Act1(Scene):

    def __init__(self, scene_manager):
        self.screen = pg.display.get_surface()
        self.scene_manager = scene_manager

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
    
        self.load_data()
        self.new()

    def load_data(self):
        self.map = Map('map.txt')
        self.crosshair_img = pg.image.load(path.join(IMG_DIR, CROSSHAIR_IMG)).convert_alpha()

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

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        # self.camera.update(self.player)
        self.camera.update(pg.mouse.get_pos(), self.map)
        # game loop - set self.playing = False to end the game
        self.dt = self.clock.tick(FPS) / 1000

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, RED, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, RED, (0, y), (WIDTH, y))

    def cast_click(self, pos):
        for sprite in self.player_sprites:
            sprite.on_click(pos)

    def on_scene_enter(self):
        pass

    def on_scene_quit(self):
        pass

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.QUIT:
            self.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit()
        elif event.type == pg.MOUSEBUTTONUP:
            self.cast_click(self.camera.get_cell(pg.mouse.get_pos()))

    def render(self,screen):
        self.screen.fill(GREY)
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()