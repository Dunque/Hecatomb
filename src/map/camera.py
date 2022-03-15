import pygame as pg
from random import randint
from src.entities.player import *
from src.settings.settings import *

vec = pg.math.Vector2

class Camera:
    def __init__(self, width, height):
        self.rect = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

        self.width_height = vec(width, height)
        self.halfs = vec(int(WIDTH / 2), int(HEIGHT / 2))
        self.def_cords = vec(0, 0)

        self.x = 0
        self.y = 0

        #Camera shake
        self.doShake = False
        self.shakeMaxTime = 0
        self.shakeTimer = 0
        self.shakeAmount = 0

    def apply(self, entity):
        return entity.rect.move(self.rect.topleft)

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

        # Shake logic
        if self.doShake:
            if (self.shakeTimer <= self.shakeMaxTime):
                self.shakeTimer += 1
                self.x += randint(0, self.shakeAmount) - \
                    self.shakeAmount // 2
                self.y += randint(0, self.shakeAmount) - \
                    self.shakeAmount // 2
            else:
                self.doShake = False
                self.shakeMaxTime = 0
                self.shakeTimer = 0
                self.shakeAmount = 0

        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def cameraShake(self, amount, time):
        self.doShake = True
        self.shakeAmount = amount
        self.shakeMaxTime = time