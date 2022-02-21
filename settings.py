import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)

# game settings
WIDTH = 1600  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 900  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Hecatomb"
BGCOLOR = DARKGREY

# Map settings
TILESIZE = 64
ROOMWIDTH = 24
ROOMHEIGHT = 16

GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

CAMERA_X = 0
CAMERA_Y = 0

# MOBS Settings
# Fire Ball settings
FIRE_BALL_SPEED = 500
FIRE_BALL_LIFETIME = 1000
FIRE_BALL_RATE = 150
KICKBACK = 200
FIRE_BALL_SPREAD = 5

#ANIMATION STUFF
#player sprite size
SPRITESIZE = 96

#SPRITE LAYERS top > bottom
HUD_LAYER = 9
WEAPON_LAYER = 8
CHARACTER_LAYER = 7
WALL_LAYER = 1
FLOOR_LAYER = 0

#TODO borrar esta trapallada

ROCK_IMAGE= pg.image.load("./sprites/RockPile.png")