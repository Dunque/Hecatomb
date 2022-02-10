import sys
import pygame as pg
from os import path
from pygame.locals import *
from src.settings import *
from src.sprites import Player, Wall, Mouse
from src.tilemap import Map, Camera
from src.SceneManager import *
from src.scenes.act1 import *
from src.scenes.act2 import *
from src.scenes.menu import *

pg.init()

sm = SceneManager()
menu = Menu(sm)
act1 = Act1(sm)
act2 = Act2(sm)

sm.set_scene(act2,0)
sm.go_to(0)
sm.loop()

pg.quit()
