import pygame as pg
from src.hud.hud import Hud
from src.map.staticmap import StaticMap
from src.scenes.cutscenes.scnCutscene2 import Cutscene2
from src.scenes.levels.scnLevel import Level
from src.scenes.music import *
from src.scenes.resourceManager import ResourceManager
from src.settings.settings import *
from src.sprites.tileset import Tileset

from src.weapons.weapons import Sword

class Level1(Level):

    def __init__(self, director):
        #Initialize superclass
        super(Level1,self).__init__(director)

        #Fog
        self.fog = pg.Surface((WIDTH, HEIGHT))

        #Exit condition: player must interact with an amount of npcs to exit the level
        self.talkedCount = 0
        self.canExit = False

        #Player starts with the sword
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
                            ResourceManager.LoadSprite("./sprites/background4.png")]

        #MAP TILESET
        self.tileset = Tileset("./sprites/tilesetAshlands.png", (TILESIZE, TILESIZE), 0, 0)

        #Dialogue file
        self.dialogues_src = "./resources/text/dialogues1.txt"

        #Map generation
        self.map = StaticMap(self, './maps/map1.txt', self.tileset, self.backgrounds)

        #Heads up display
        self.hud = Hud(self)

    def update(self, time):
        super().update(time)

        #Exit condition
        if self.talkedCount >= 4:
            self.canExit = True

    def draw(self, screen):
        #Background color
        self.screen = screen
        self.screen.fill(BGCOLOR)

        #Sprites
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        #Fog, it must be rendered after the sprites but before the HUD
        self.render_fog()
        for sprite in list(self.candelabros_SG):
            self.render_fog(sprite)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

        #Hud
        for hud in self.all_hud:
            self.screen.blit(hud.image, self.camera.apply(hud))
        self.hud.drawDialogue()
        self.hud.drawMenu()
        self.hud.drawDineros()
        self.hud.draw_health(screen)


    def render_fog(self, sprite = None):
        self.light_rect = self.light_mask.get_rect()
        if not sprite:
            self.fog.fill(LIGHTGREY)
            self.light_rect.center = self.camera.apply(self.player).center
        else:
            self.light_rect.center = self.camera.apply(sprite).center
        self.fog.blit(self.light_mask, self.light_rect)

    # -----------------------------------------------------
    # Scene transitions

    def nextScene(self):
        pg.mouse.set_visible(True)
        scene = Cutscene2(self.director)
        Music.changeMusic(self, 0)
        self.director.changeScene(scene)
