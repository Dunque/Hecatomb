import pygame as pg
pg.init()

# Define some colors (R, G, B)
NUCLEAR_WHTIE = (255, 255, 255)
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

MAROON = (128, 0, 0)
BROWN = (104, 30, 0)

# Game settings
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
TRUCK_HIT_RECT = pg.Rect(0, 0, 423, 255)

CAMERA_X = 0
CAMERA_Y = 0

# MOBS Settings
# Fire Ball settings

#ANIMATION STUFF
#player sprite size
CHARACTER_SPRITE_SIZE = 96

# SOUNDS
FIRE_BULLET_SOUND = pg.mixer.Sound("./sounds/Fire_4.wav")
DEATH_SOUND = pg.mixer.Sound("./sounds/Game_Over.wav")
CHANGE_SOUND = pg.mixer.Sound("./sounds/recharge.wav")
ENEMY_DEATH_SOUND = pg.mixer.Sound("./sounds/Hit_1.wav")
SWORD_SOUND = pg.mixer.Sound("./sounds/sword.wav")
PLAYER_DAMAGE_SOUND = pg.mixer.Sound("./sounds/Fire_2.wav")
EXPLOSION_SOUND = pg.mixer.Sound("./sounds/explosion.wav")
DODGE_SOUND = pg.mixer.Sound("./sounds/roll.wav")
WIN_ROOM_SOUND=pg.mixer.Sound("./sounds/win_sound.wav")
#SPRITE LAYERS top > bottom
HUD_LAYER = 9
PICKUP_LAYER = 8
WEAPON_LAYER = 7
CHARACTER_LAYER = 6
WALL_LAYER = 1
FLOOR_LAYER = 0



#TODO borrar esta trapallada

ROCK_IMAGE= pg.image.load("./sprites/RockPile.png")




# ---------------------------------------------------------
# GUI settings

# Font settings
HANSHAND_FONT = 'resources/fonts/hanshand.ttf'

# Button settings
BUTTON_IMAGE = 'resources/images/gold_button.png'

BUTTON_WIDTH = 400
BUTTON_HEIGHT = 90
BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)

BUTTON_SEP_X = 80
BUTTON_SEP_Y = 45

# Main menu layout
MAIN_MENU_Y0 = HEIGHT/2
MAIN_MENU_LAYOUT = (2, 3)

# Other menus layout
OTHER_MENU_Y0 = HEIGHT*38/100

RECORDS_MENU_LAYOUT = (1, 1)
OPTIONS_MENU_LAYOUT = (1, 1)
CREDITS_MENU_LAYOUT = (1, 6)

PAUSE_MENU_LAYOUT = (1, 4)
LOSING_MENU_LAYOUT = (1, 2)
