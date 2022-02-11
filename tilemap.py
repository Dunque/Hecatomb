import pygame as pg
from settings import *

vec = pg.math.Vector2

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

        self.width_height = vec(width,height)
        self.halfs = vec(int(WIDTH / 2), int(HEIGHT / 2))
        self.def_cords = vec(CAMERA_X, CAMERA_Y)

        self.def_cords = vec(CAMERA_X, CAMERA_Y)
        
        self.x = 0
        self.y = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def get_moved(self):
        return self.x, self.y

    def update(self, target):
        self.x = -target.rect.centerx + int(WIDTH / 2)
        self.y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        self.x = min(0, self.x)  # left
        self.y = min(0, self.y)  # top
        self.x = max(-(self.width - WIDTH), self.x)  # right
        self.y = max(-(self.height - HEIGHT), self.y)  # bottom

        #self.camera = pg.Rect(self.def_cords.x, self.def_cords.y, self.width_height.x, self.width_height.y)

        self.camera = pg.Rect(self.x, self.y, self.width, self.height)
