import pygame as pg
from src.settings.settings import *
from src.scenes.scene import *
from pygame.locals import *


class Music():

    def changeMusic(self, num): #Cambia la musica que esta soando actualmente
        Music.volumeMusic(self, 1)
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


    def volumeMusic(self, num): #Controlamos el volumen de toda la musica
        pg.mixer.music.set_volume(num)

    def effectsVolume(self,num,scene): #Controlamos el volumen de todos los efectos
        scene.FIRE_BULLET_SOUND.set_volume(num)
        scene.DEATH_SOUND.set_volume(num)
        scene.CHANGE_SOUND.set_volume(num)
        scene.ENEMY_DEATH_SOUND.set_volume(num)
        scene.SWORD_SOUND.set_volume(num)
        scene.PLAYER_DAMAGE_SOUND.set_volume(num)
        scene.EXPLOSION_SOUND.set_volume(num)
        scene.DODGE_SOUND.set_volume(num)
        scene.WIN_ROOM_SOUND.set_volume(num)
        scene.HEAL_SOUND.set_volume(num)
        scene.VOICE_SOUND_0.set_volume(num)
        scene.VOICE_SOUND_1.set_volume(num)
        scene.VOICE_SOUND_2.set_volume(num)
        scene.VOICE_SOUND_3.set_volume(num)
        scene.VOICE_SOUND_4.set_volume(num)
        scene.VOICE_SOUND_5.set_volume(num)
        scene.VOICE_SOUND_6.set_volume(num)
        scene.VOICE_SOUND_7.set_volume(num)
        scene.VOICE_SOUND_8.set_volume(num)
        scene.VOICE_SOUND_9.set_volume(num)
        scene.VOICE_SOUND_10.set_volume(num)

    def getVolumeMusic(self): #Devuelve el volumen actual de la musica
        return pg.mixer.music.get_volume()

    def getEffectsVolume(self): #Devuelve el volumen actual de los efectos
        return FIRE_BULLET_SOUND.get_volume()

    def playVoice(self,scene,num):
        if (num == 0):
            scene.VOICE_SOUND_0.play()
        elif (num == 1):
            scene.VOICE_SOUND_1.play()
        elif (num == 2):
            scene.VOICE_SOUND_2.play()
        elif (num == 3):
            scene.VOICE_SOUND_3.play()
        elif (num == 4):
            scene.VOICE_SOUND_4.play()
        elif (num == 5):
            scene.VOICE_SOUND_5.play()
        elif (num == 6):
            scene.VOICE_SOUND_6.play()
        elif (num == 7):
            scene.VOICE_SOUND_7.play()
        elif (num == 8):
            scene.VOICE_SOUND_8.play()
        elif (num == 9):
            scene.VOICE_SOUND_9.play()
        elif (num == 10):
            scene.VOICE_SOUND_10.play()
