import pygame as pg
from settings import *
from anim import *
from entitydata import *

import math
from random import uniform

vec = pg.math.Vector2

class Pickup(pg.sprite.Sprite):
    def __init__(self, scene, x, y, image):
        self._layer = PICKUP_LAYER
        self.groups = scene.all_sprites, scene.walls_SG
        pg.sprite.Sprite.__init__(self, self.groups)

        self.scene = scene
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)

        #tilemap position
        self.x = x
        self.y = y

        #Global position
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE