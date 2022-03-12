import pygame as pg
from src.hud.hud import Hud
from src.map.cutscenemap import CutsceneMap
from src.scenes.levels.scnLevel import Level
from src.settings.settings import *
from src.hud.hud import Hud
from src.scenes.music import *
from src.sprites.tileset import Tileset

class Cutscene4(Level):

    def __init__(self, director):
        #Initialize superclass
        super(Cutscene4,self).__init__(director)

    def load_data(self):
        #PLAYER DATA
        self.playerWalkSheet = pg.image.load("./sprites/Player/playerWalkSheet.png").convert_alpha()
        self.playerIdleSheet = pg.image.load("./sprites/Player/playerIdleSheet.png").convert_alpha()
        self.playerDodgeSheet =  pg.image.load("./sprites/Player/playerDodgeSheet.png").convert_alpha()
        self.playerDeathSheet =  pg.image.load("./sprites/Player/playerDeathSheet.png").convert_alpha()
        self.playerTalkingSheet =  pg.image.load("./sprites/Player/playerTalkingSheet.png").convert_alpha()

        #WEAPONS
        self.playerGunImg = pg.image.load("./sprites/Weapons/gun.png").convert_alpha()
        self.playerShotgunImg = pg.image.load("./sprites/Weapons/shotgun.png").convert_alpha()
        self.playerSwordImg = pg.image.load("./sprites/Weapons/sword.png").convert_alpha()

        #OBJECTS
        self.medkitImg = pg.image.load("./sprites/Objects/medkit.png").convert_alpha()
        self.chestImg = pg.image.load("./sprites/Objects/chest.png").convert_alpha()
        self.candelabroImg = pg.image.load("./sprites/Objects/candelabro.png").convert_alpha()
        self.exitImg = pg.image.load("./sprites/Objects/exit.png").convert_alpha()

        #BULLETS/AMMUNITION/EXPLOSIONS DATA
        self.gunBulletImg = pg.image.load("./sprites/Fire_Ball/gun_bullet.png").convert_alpha()
        self.fire_ballMoveSheet = pg.image.load("./sprites/Fire_Ball/Move.png").convert_alpha()
        self.fire_ballExplosionSheet = pg.image.load("./sprites/Fire_Ball/Explosion.png").convert_alpha()
        self.fire_ballExplosion2Sheet = pg.image.load("./sprites/Fire_Ball/Explosion2.png").convert_alpha()

        #HUD
        self.radialMenuImg = pg.image.load("./sprites/Hud/radial_menu.png").convert_alpha()
        self.abrirImg = pg.image.load("./sprites/Hud/abrir.png").convert_alpha()
        self.hablarImg = pg.image.load("./sprites/Hud/hablar.png").convert_alpha()
        self.gunCrosshairImg = pg.image.load("./sprites/Hud/gun_crosshair.png").convert_alpha()
        self.shotgunCrosshairImg = pg.image.load("./sprites/Hud/shotgun_crosshair.png").convert_alpha()
        self.dialogueBox = pg.image.load("./sprites/Hud/dialoguebox.png").convert_alpha()
        self.dialogueContinuation = pg.image.load("./sprites/Hud/continuation.png").convert_alpha()
        self.game_font = pg.freetype.Font("./sprites/Hud/impostor.ttf", 24)
        self.light_mask = pg.transform.scale(pg.image.load("./sprites/Hud/light_350_soft.png").convert_alpha(), (1500, 1500))

        #NPC
        self.npc1Profile = pg.image.load("./sprites/Player/profile1.png").convert_alpha()

        # EYE DATA
        self.eyeWalkSheet = pg.image.load("./sprites/Eye/eye_ball_4.png").convert_alpha()
        self.eyeDeathSheet = pg.image.load("./sprites/Eye/eye_boom_4.png").convert_alpha()

        # WORM DATA
        self.wormWalkSheet = pg.image.load("./sprites/Worm/Walk.png").convert_alpha()
        self.wormIdleSheet = pg.image.load("./sprites/Worm/Idle.png").convert_alpha()
        self.wormHitSheet = pg.image.load("./sprites/Worm/GetHit.png").convert_alpha()
        self.wormDeathSheet = pg.image.load("./sprites/Worm/Death.png").convert_alpha()
        self.wormAttackSheet = pg.image.load("./sprites/Worm/Attack.png").convert_alpha()

        #Khan DATA
        self.khanWalkSheet = pg.image.load("./sprites/Khan/khanWalkSheet.png").convert_alpha()
        self.khanDeathSheet = pg.image.load("./sprites/Khan/khanDeathSheet.png").convert_alpha()

        self.khan2WalkSheet = pg.image.load("./sprites/Khan/khan2WalkSheet.png").convert_alpha()
        self.khan2DeathSheet = pg.image.load("./sprites/Khan/khan2DeathSheet.png").convert_alpha()

        #HERALD DATA
        self.heraldWalkSheet = pg.image.load("./sprites/Herald/herald2WalkSheet.png").convert_alpha()
        self.heraldDeathSheet = pg.image.load("./sprites/Herald/herald2DeathSheet.png").convert_alpha()

        self.herald2WalkSheet = pg.image.load("./sprites/Herald/heraldWalkSheet.png").convert_alpha()
        self.herald2DeathSheet = pg.image.load("./sprites/Herald/heraldDeathSheet.png").convert_alpha()

        #MAP BACKGROUNDS
        self.backgrounds = [pg.image.load("./sprites/background1.png").convert_alpha()]

        #MAP TILESET
        self.tileset = Tileset("./sprites/tilesetAshlands.png", (TILESIZE, TILESIZE), 0, 0)

        #Dialogue file
        self.dialogues_src = "./resources/text/dialogues.txt"

        #Map generation
        self.map = CutsceneMap(self, './maps/cutscenemap4.txt', self.tileset, self.backgrounds)

        #Heads up display
        self.hud = Hud(self)

    # -----------------------------------------------------
    # Scene transitions

    def nextScene(self):
        self.director.exitScene()