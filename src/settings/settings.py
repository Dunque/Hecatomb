import pygame as pg
pg.init()
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

MAROON = (128, 0, 0)
BROWN = (104, 30, 0)

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
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

CAMERA_X = 0
CAMERA_Y = 0

# MOBS Settings
# Fire Ball settings

#ANIMATION STUFF
#player sprite size
CHARACTER_SPRITE_SIZE = 96

#SPRITE LAYERS top > bottom
HUD_LAYER = 9
PICKUP_LAYER = 8
WEAPON_LAYER = 7
CHARACTER_LAYER = 6
WALL_LAYER = 1
FLOOR_LAYER = 0

FIRE_BULLET_SOUND =pg.mixer.Sound("./sounds/Fire_4.wav")
DEATH_SOUND =pg.mixer.Sound("./sounds/Game_Over.wav")
CHANGE_SOUND =pg.mixer.Sound("./sounds/recharge.wav")
ENEMY_DEATH_SOUND= pg.mixer.Sound("./sounds/Hit_1.wav")
SWORD_SOUND=pg.mixer.Sound("./sounds/sword.wav")
music =pg.mixer.music.load("./sounds/level_music.mp3")
#TODO borrar esta trapallada

ROCK_IMAGE= pg.image.load("./sprites/RockPile.png")