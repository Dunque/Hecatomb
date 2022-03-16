import pygame as pg
from src.hud.hud import Hud
from src.map.staticmap import StaticMap
from src.scenes.cutscenes.scnCutscene3 import Cutscene3
from src.scenes.levels.scnLevel import Level
from src.scenes.music import *
from src.scenes.resourceManager import ResourceManager
from src.settings.settings import *
from src.sprites.tileset import Tileset


class Level2(Level):

    def __init__(self, director):
        #Initialize superclass
        super(Level2,self).__init__(director)

    def load_data(self):
        #PLAYER DATA
        self.playerWalkSheet = ResourceManager.LoadSprite("./sprites/Player/playerWalkSheet.png")
        self.playerIdleSheet = ResourceManager.LoadSprite("./sprites/Player/playerIdleSheet.png")
        self.playerDodgeSheet =  ResourceManager.LoadSprite("./sprites/Player/playerDodgeSheet.png")
        self.playerDeathSheet =  ResourceManager.LoadSprite("./sprites/Player/playerDeathSheet.png")
        self.playerTalkingSheet =  ResourceManager.LoadSprite("./sprites/Player/playerTalkingSheet.png")

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

        #HUD
        self.radialMenuImg = ResourceManager.LoadSprite("./sprites/Hud/radial_menu.png")
        self.abrirImg = ResourceManager.LoadSprite("./sprites/Hud/abrir.png")
        self.hablarImg = ResourceManager.LoadSprite("./sprites/Hud/hablar.png")
        self.gunCrosshairImg = ResourceManager.LoadSprite("./sprites/Hud/gun_crosshair.png")
        self.shotgunCrosshairImg = ResourceManager.LoadSprite("./sprites/Hud/shotgun_crosshair.png")
        self.dialogueBox = ResourceManager.LoadSprite("./sprites/Hud/dialoguebox.png")
        self.dialogueContinuation = ResourceManager.LoadSprite("./sprites/Hud/continuation.png")
        self.game_font = pg.freetype.Font("./sprites/Hud/impostor.ttf", 24)
        self.light_mask = pg.transform.scale(ResourceManager.LoadSprite("./sprites/Hud/light_350_soft.png"), (1500, 1500))

        #NPC
        self.npc1Profile = ResourceManager.LoadSprite("./sprites/Player/profile1.png")

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
        self.dialogues_src = "./resources/text/dialogues.txt"

        #Map generation
        self.map = StaticMap(self, './maps/map2.txt', self.tileset, self.backgrounds)

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

    def nextScene(self):
        pg.mouse.set_visible(True)
        scene = Cutscene3(self.director)
        Music.changemusic(self, 0)
        self.director.changeScene(scene)
