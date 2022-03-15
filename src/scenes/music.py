import pygame as pg
from src.settings.settings import *
from src.scenes.scene import *
from pygame.locals import *


class Music():



    def changemusic(self, num): #Cambia la musica que esta soando actualmente
        Music.volumemusic(self, 1)
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
        elif (num==3):
            pg.mixer.music.stop
            pg.mixer.music.load("./sounds/music/level_music_3.mp3")
            pg.mixer.music.play(-1)
        elif (num==4):
            pg.mixer.music.stop
            pg.mixer.music.load("./sounds/music/level_music_4.mp3")
            pg.mixer.music.play(-1)
        elif (num==5):
            pg.mixer.music.stop
            pg.mixer.music.load("./sounds/music/level_music_5.mp3")
            pg.mixer.music.play(-1)


    def volumemusic(self, num): #Controlamos el volumen de toda la musica
        pg.mixer.music.set_volume(num)

    def effectsvolume(self,num): #Controlamos el volumen de todos los efectos
        FIRE_BULLET_SOUND.set_volume(num)
        DEATH_SOUND.set_volume(num)
        CHANGE_SOUND.set_volume(num)
        ENEMY_DEATH_SOUND.set_volume(num)
        SWORD_SOUND.set_volume(num)
        PLAYER_DAMAGE_SOUND.set_volume(num)
        EXPLOSION_SOUND.set_volume(num)
        DODGE_SOUND.set_volume(num)
        WIN_ROOM_SOUND.set_volume(num)
    def getvolumemusic(self): #Devuelve el volumen actual de la musica
        return pg.mixer.music.get_volume


    def geteffectsvolume(self): #Devuelve el volumen actual de los efectos
        return FIRE_BULLET_SOUND.get_volume

