import pygame as pg
from src.settings.settings import *
from src.scenes.scene import *
from pygame.locals import *


class Music():

    def __init__(self):
        pg.mixer.music.load("./sounds/menu_music.mp3")
        pg.mixer.music.play(-1)

    def changemusic(self, num):

        if (num==0):
            pg.mixer.music.stop
            pg.mixer.music.load("./sounds/music/menu_music.mp3")
            pg.mixer.music.play(-1)
        elif (num==1):
            pg.mixer.music.stop
            pg.mixer.music.load("./sounds/music/level_music_1.mp3")
            pg.mixer.music.play(-1)
        elif (num==2):
            pg.mixer.music.stop
            pg.mixer.music.load("./sounds/music/level_music_2.mp3")
            pg.mixer.music.play(-1)

    def volumemusic(self, num):
        pg.mixer.music.set_volume(num)


