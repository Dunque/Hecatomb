import pygame as pg
from src.hud.hud import Hud
from src.map.cutscenemap import CutsceneMap
from src.scenes.levels.scnLevel import Level
from src.scenes.levels.scnLevel3 import Level3
from src.scenes.music import *
from src.scenes.resourceManager import ResourceManager
from src.settings.settings import *
from src.sprites.tileset import Tileset

from src.weapons.weapons import Gun, Sword

class Cutscene3(Level):

    def __init__(self, director):
        #Initialize superclass
        super(Cutscene3,self).__init__(director)

        #Player starts with the sword and the gun
        self.player.give_weapon(self.player.entityData.load_weapons())

    def load_data(self):

        super().load_data()

        #WEAPONS
        self.playerGunImg = ResourceManager.LoadSprite("./sprites/Weapons/gun.png")
        self.playerShotgunImg = ResourceManager.LoadSprite("./sprites/Weapons/shotgun.png")
        self.playerSwordImg = ResourceManager.LoadSprite("./sprites/Weapons/sword.png")

        #OBJECTS
        self.medkitImg = ResourceManager.LoadSprite("./sprites/Objects/medkit.png")
        self.chestImg = ResourceManager.LoadSprite("./sprites/Objects/chest.png")
        self.candelabroImg = ResourceManager.LoadSprite("./sprites/Objects/candelabro.png")
        self.exitImg = ResourceManager.LoadSprite("./sprites/Objects/exit.png")

        #BULLETS/AMMUNITION/EXPLOSIONS DATA
        self.gunBulletImg = ResourceManager.LoadSprite("./sprites/Fire_Ball/gun_bullet.png")
        
        self.fire_ballExplosionSheet = ResourceManager.LoadSprite("./sprites/Fire_Ball/Explosion.png")
        self.fire_ballExplosion2Sheet = ResourceManager.LoadSprite("./sprites/Fire_Ball/Explosion2.png")

        #NPC
        self.npc1Profile = ResourceManager.LoadSprite("./sprites/Player/profile1.png")
        self.tacoTruck = ResourceManager.LoadSprite("./sprites/NPC/tacotruck.png")
        self.tacoTruckTalking = ResourceManager.LoadSprite("./sprites/NPC/truckTalking.png")
        self.tacoProfile = ResourceManager.LoadSprite("./sprites/NPC/profileBoxTruck.png")

        #MAP BACKGROUNDS
        self.backgrounds = [ResourceManager.LoadSprite("./sprites/background8.png")]

        #MAP TILESET
        self.tileset = Tileset("./sprites/tilesetCitadel.png", (TILESIZE, TILESIZE), 0, 0)

        #Dialogue file
        self.dialogues_src = "./resources/text/dialogues3.txt"

        #Map generation
        self.map = CutsceneMap(self, './maps/cutscenemap3.txt', self.tileset, self.backgrounds)

        #Heads up display
        self.hud = Hud(self)

        # SOUNDS
        self.FIRE_BULLET_SOUND = pg.mixer.Sound("./sounds/Fire_4.wav")
        self.DEATH_SOUND = pg.mixer.Sound("./sounds/Game_Over.wav")
        self.CHANGE_SOUND = pg.mixer.Sound("./sounds/recharge.wav")
        self.ENEMY_DEATH_SOUND = pg.mixer.Sound("./sounds/Hit_1.wav")
        self.SWORD_SOUND = pg.mixer.Sound("./sounds/sword.wav")
        self.PLAYER_DAMAGE_SOUND = pg.mixer.Sound("./sounds/Fire_2.wav")
        self.EXPLOSION_SOUND = pg.mixer.Sound("./sounds/explosion.wav")
        self.DODGE_SOUND = pg.mixer.Sound("./sounds/roll.wav")
        self.WIN_ROOM_SOUND = pg.mixer.Sound("./sounds/win_sound.wav")
        self.HEAL_SOUND = pg.mixer.Sound("./sounds/heal.wav")
        self.OPEN_SOUND = pg.mixer.Sound("./sounds/chest_sound.wav")
        self.VOICE_SOUND_0 = pg.mixer.Sound("./sounds/voices/Crossbowman_See_001.wav")
        self.VOICE_SOUND_1 = pg.mixer.Sound("./sounds/voices/greetings-3.wav")
        self.VOICE_SOUND_2 = pg.mixer.Sound("./sounds/voices/joy-2.wav")
        self.VOICE_SOUND_3 = pg.mixer.Sound("./sounds/voices/doh_wav_cut.wav")
        self.VOICE_SOUND_4 = pg.mixer.Sound("./sounds/voices/Guard_See_001.wav")
        self.VOICE_SOUND_5 = pg.mixer.Sound("./sounds/voices/oh_yeah_wav_cut.wav")
        self.VOICE_SOUND_6 = pg.mixer.Sound("./sounds/voices/Hero_See_001.wav")
        self.VOICE_SOUND_7 = pg.mixer.Sound("./sounds/voices/Paladin_See_001.wav")
        self.VOICE_SOUND_8 = pg.mixer.Sound("./sounds/voices/greetings-1.wav")
        self.VOICE_SOUND_9 = pg.mixer.Sound("./sounds/voices/joy-1.wav")
        self.VOICE_SOUND_10 = pg.mixer.Sound("./sounds/voices/soldierintro.wav")

    # -----------------------------------------------------
    # Scene transitions

    def draw(self, screen):
        #Background color
        self.screen = screen
        self.screen.fill(BGCOLOR)

        #Sprites
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        #Hud
        for hud in self.all_hud:
            self.screen.blit(hud.image, self.camera.apply(hud))
        self.hud.drawDialogue()
        self.hud.drawMenu()
        self.hud.drawDineros()
        self.hud.draw_health(screen)

    def nextScene(self):
        pg.mouse.set_visible(True)
        scene = Level3(self.director)
        Music.changeMusic(self, 3)
        self.director.changeScene(scene)
