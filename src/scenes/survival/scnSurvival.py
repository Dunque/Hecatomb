import random
from random import choice

import pygame as pg
from src.hud.hud import Hud
from src.map.randmap import RandMap
from src.scenes.levels.scnLevel import Level
from src.scenes.music import *
from src.scenes.resourceManager import ResourceManager
from src.scenes.scnPause import PauseMenu
from src.scenes.score import Score
from src.scenes.survival.scnSurvivalEnd import SurvivalEnd
from src.settings.settings import *
from src.sprites.tileset import Tileset
from src.weapons.weapons import Gun, Shotgun, Sword


class Survival(Level):

    def __init__(self, director):
        #Initialize superclass
        super(Survival, self).__init__(director)

        self.isSurvival = True

        #Player starts with all weapons
        self.player.give_weapon(Sword)
        self.player.give_weapon(Gun)
        self.player.give_weapon(Shotgun)

        # Reset survival score
        Score.resetScore()

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

        # EYE DATA
        self.eyeWalkSheet = ResourceManager.LoadSprite("./sprites/Eye/eye_ball_4.png")
        self.eyeDeathSheet = ResourceManager.LoadSprite("./sprites/Eye/eye_boom_4.png")

        # WORM DATA
        self.wormWalkSheet = ResourceManager.LoadSprite("./sprites/Worm/Walk.png")
        self.wormDeathSheet = ResourceManager.LoadSprite("./sprites/Worm/Death.png")
        self.wormAttackSheet = ResourceManager.LoadSprite("./sprites/Worm/Attack.png")

        #Khan DATA
        self.khanWalkSheet = ResourceManager.LoadSprite("./sprites/Khan/khanWalkSheet.png")
        self.khanDeathSheet = ResourceManager.LoadSprite("./sprites/Khan/khanDeathSheet.png")

        self.khan2WalkSheet = ResourceManager.LoadSprite("./sprites/Khan/khan2WalkSheet.png")
        self.khan2DeathSheet = ResourceManager.LoadSprite("./sprites/Khan/khan2DeathSheet.png")

        #HERALD DATA
        self.heraldWalkSheet = ResourceManager.LoadSprite("./sprites/Herald/herald2WalkSheet.png")
        self.heraldDeathSheet = ResourceManager.LoadSprite("./sprites/Herald/herald2DeathSheet.png")

        self.herald2WalkSheet = ResourceManager.LoadSprite("./sprites/Herald/heraldWalkSheet.png")
        self.herald2DeathSheet = ResourceManager.LoadSprite("./sprites/Herald/heraldDeathSheet.png")

        #MAP BACKGROUNDS
        self.backgrounds = [ResourceManager.LoadSprite("./sprites/background1.png"),
                            ResourceManager.LoadSprite("./sprites/background2.png"),
                            ResourceManager.LoadSprite("./sprites/background3.png"),
                            ResourceManager.LoadSprite("./sprites/background4.png"),
                            ResourceManager.LoadSprite("./sprites/background5.png"),
                            ResourceManager.LoadSprite("./sprites/background6.png"),
                            ResourceManager.LoadSprite("./sprites/background7.png"),
                            ResourceManager.LoadSprite("./sprites/background8.png"),
                            ResourceManager.LoadSprite("./sprites/background9.png"),
                            ResourceManager.LoadSprite("./sprites/background10.png")]

        #MAP TILESET
        self.tilesets = [Tileset("./sprites/tilesetAshlands.png", (TILESIZE, TILESIZE), 0, 0),
                         Tileset("./sprites/tilesetForest.png", (TILESIZE, TILESIZE), 0, 0),
                         Tileset("./sprites/tilesetCitadel.png", (TILESIZE, TILESIZE), 0, 0)]
                         
        self.tileset = choice(self.tilesets)

        #Dialogue file
        self.dialogues_src = "./resources/text/dialogues1.txt"

        #Map generation
        self.map = RandMap(self, './maps/rooms.txt',
                             self.tileset, self.backgrounds)

        #Heads up display
        self.hud = Hud(self)

    # -----------------------------------------------------
    # Scene transitions

    def pauseScene(self):
        pg.mouse.set_visible(True)
        scene = PauseMenu(self.director)
        Music.volumeMusic(self,0.25)
        self.director.stackScene(scene)

    def nextScene(self):
        pg.mouse.set_visible(True)
        m = random.randint(1,5)
        Music.changeMusic(self,m)
        scene = SurvivalEnd(self.director)
        self.director.stackScene(scene)
