import pygame as pg
from src.hud.hud import Hud
from src.map.cutscenemap import CutsceneMap
from src.scenes.levels.scnLevel import Level
from src.scenes.music import *
from src.scenes.resourceManager import ResourceManager
from src.settings.settings import *
from src.sprites.tileset import Tileset

from src.weapons.weapons import Shotgun, Gun, Sword

class Cutscene4(Level):

    def __init__(self, director):
        #Initialize superclass
        super(Cutscene4,self).__init__(director)

        #Player starts with all weapons
        self.player.give_weapon(Sword)
        self.player.give_weapon(Gun)
        self.player.give_weapon(Shotgun)

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
        self.backgrounds = [ResourceManager.LoadSprite("./sprites/background9.png")]

        #MAP TILESET
        self.tileset = Tileset("./sprites/tilesetCitadel.png", (TILESIZE, TILESIZE), 0, 0)

        #Dialogue file
        self.dialogues_src = "./resources/text/dialogues4.txt"

        #Map generation
        self.map = CutsceneMap(self, './maps/cutscenemap4.txt', self.tileset, self.backgrounds)

        #Heads up display
        self.hud = Hud(self)

    # -----------------------------------------------------
    # Scene transitions

    def nextScene(self):
        self.director.exitScene()
