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
WIDTH = 1280   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 720  # 16 * 48 or 32 * 24 or 64 * 12
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
SPRITESIZE = 96

ARBOL_IMAGE=pg.image.load("./sprites/arbol_rosa.png")
ARBOL_IMAGE1=pg.image.load("./sprites/arbol_rosa_1.png")
ARBOL_IMAGE2=pg.image.load("./sprites/arbol_rosa_2.png")
ARBOL_IMAGE3=pg.image.load("./sprites/arbol_rosa_3.png")
ARBOL_IMAGE4=pg.image.load("./sprites/arbol_rosa_4.png")
BOX_IMAGE= pg.image.load("./sprites/Box.png")
FENCE_IMAGE= pg.image.load("./sprites/fence.png")
ROCK_IMAGE= pg.image.load("./sprites/RockPile.png")
GROUND_IMAGE= pg.image.load("./sprites/hierba.png")
ARBUSTO_IMAGE_1=pg.image.load("./sprites/sheet_040.png")
ARBUSTO_IMAGE_2=pg.image.load("./sprites/sheet_041.png")
ROCK_IMAGE_2=pg.image.load("./sprites/sheet_042.png")
ROCK_IMAGE_3=pg.image.load("./sprites/sheet_043.png")
ROCK_IMAGE_4=pg.image.load("./sprites/sheet_045.png")
ROCK_IMAGE_5=pg.image.load("./sprites/sheet_046.png")
