import pygame as pg
from src.settings.settings import *

vec = pg.math.Vector2


class Wall(pg.sprite.Sprite):
    def __init__(self, scene, x, y, tileset):
        self._layer = WALL_LAYER
        self.groups = scene.all_sprites, scene.walls_SG
        pg.sprite.Sprite.__init__(self, self.groups)

        self.scene = scene
        self.image = tileset
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)

        #tilemap position
        self.x = x
        self.y = y

        #Global position
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Floor(pg.sprite.Sprite):
    def __init__(self, scene, x, y, tileset):
        self._layer = FLOOR_LAYER
        self.groups = scene.all_sprites, scene.floors_SG
        pg.sprite.Sprite.__init__(self, self.groups)

        self.scene = scene
        self.image = tileset
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)

        #tilemap position
        self.x = x
        self.y = y

        #Global position
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Door(Wall):
    def __init__(self, scene, x, y, tileset):
        self.origImage = tileset
        super(Door, self).__init__(scene, x, y, tileset)

    def open(self):
        # In order to open the door we remove the image and
        # remove it from "walls" group
        self.scene.walls_SG.remove(self)
        self.scene.all_sprites.remove(self)

    def close(self):
        # In order to close the door we add the image and
        # add it to the "walls" group
        self.scene.walls_SG.add(self)
        self.scene.all_sprites.add(self)

        self.groups = self.scene.all_sprites, self.scene.walls_SG

        self.image = self.origImage
