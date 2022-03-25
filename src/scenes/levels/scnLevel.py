import time

import pygame as pg
from src.scenes.music import *
from src.scenes.records import Records
from src.scenes.resourceManager import ResourceManager
from src.scenes.scene import Scene
from src.scenes.scnLosing import LosingMenu
from src.scenes.scnPause import PauseMenu
from src.scenes.score import Score
from src.settings.settings import *


class Level(Scene):

    def __init__(self, director):
        #Initialize superclass
        Scene.__init__(self, director)

        self.isSurvival = False

        #Initialize sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.all_hud = pg.sprite.LayeredUpdates()
        self.walls_SG = pg.sprite.LayeredUpdates()
        self.candelabros_SG = pg.sprite.LayeredUpdates()
        self.mobs_SG = pg.sprite.LayeredUpdates()
        self.player_SG = pg.sprite.LayeredUpdates()
        self.npc_SG = pg.sprite.LayeredUpdates()
        self.bullets_SG = pg.sprite.LayeredUpdates()
        self.explosions_SG = pg.sprite.LayeredUpdates()
        self.weapons_SG = pg.sprite.LayeredUpdates()
        self.floors_SG = pg.sprite.LayeredUpdates()
        self.chest_SG = pg.sprite.LayeredUpdates()
        self.menus = []

        self.screen = None

        self.player = None

        #Exit condition: player must interact with an amount of npcs to exit the level
        self.talkedCount = 0
        self.canExit = True

        #Loads all sprite and sound data
        self.load_data()
    
    def reset(self):
        self.__init__(self.director)
        print(1)
        self.player.entityData.reset()

    def load_data(self):
        #PLAYER DATA
        self.playerWalkSheet = ResourceManager.LoadSprite("./sprites/Player/playerWalkSheet.png")
        self.playerIdleSheet = ResourceManager.LoadSprite("./sprites/Player/playerIdleSheet.png")
        self.playerDodgeSheet =  ResourceManager.LoadSprite("./sprites/Player/playerDodgeSheet.png")
        self.playerDeathSheet =  ResourceManager.LoadSprite("./sprites/Player/playerDeathSheet.png")
        self.playerTalkingSheet =  ResourceManager.LoadSprite("./sprites/Player/playerTalkingSheet.png")

        #HUD
        self.radialMenuImg = ResourceManager.LoadSprite("./sprites/Hud/radial_menu.png")
        self.swordRadialMenuImg = ResourceManager.LoadSprite("./sprites/Hud/sword_radial_menu.png")
        self.gunRadialMenuImg = ResourceManager.LoadSprite("./sprites/Hud/gun_radial_menu.png")
        self.shotgunRadialMenuImg = ResourceManager.LoadSprite("./sprites/Hud/shotgun_radial_menu.png")
        self.manoRadialMenuImg = ResourceManager.LoadSprite("./sprites/Hud/mano_radial_menu.png")
        self.abrirImg = ResourceManager.LoadSprite("./sprites/Hud/abrir.png")
        self.hablarImg = ResourceManager.LoadSprite("./sprites/Hud/hablar.png")
        self.gunCrosshairImg = ResourceManager.LoadSprite("./sprites/Hud/gun_crosshair.png")
        self.shotgunCrosshairImg = ResourceManager.LoadSprite("./sprites/Hud/shotgun_crosshair.png")
        self.dialogueBox = ResourceManager.LoadSprite("./sprites/Hud/dialoguebox.png")
        self.dialogueOptions = ResourceManager.LoadSprite("./sprites/Hud/chatOpciones.png")
        self.dialogueOptionsPicker = ResourceManager.LoadSprite("./sprites/Hud/chatOpcionesPicker.png")
        self.dialogueContinuation = ResourceManager.LoadSprite("./sprites/Hud/continuation.png")
        self.dinerosImg = pg.transform.scale(ResourceManager.LoadSprite("./sprites/Hud/dineros.png"), (80, 80))
        self.game_font = pg.freetype.Font("./resources/fonts/main_font.ttf", 28)
        self.game_font.strong = True
        self.light_mask = pg.transform.scale(ResourceManager.LoadSprite("./sprites/Hud/light_350_soft.png"), (1500, 1500))

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


    def update(self, time):
        self.dt = time
        # update portion of the game loop
        self.all_sprites.update()
        self.all_hud.update()
        self.camera.update(self.player)

        # If player died
        if not self.player_SG.has(self.player):

            # Si estamos en Survival
            if self.isSurvival:
                # Actualizamos mejores puntuaciones
                currentScore = Score.getScore()
                Records.updateRecords(currentScore)
                # Go to SurvivalEnd
                self.nextScene()

            # Si estamos en Level1, Level2, Level3
            else:
                self.losingScene()


        for menu in self.menus:
            menu.update()

        self.map.update()

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
        self.hud.drawDineros()
        self.hud.draw_health(screen)


    def events(self, eventList):
        # Se mira la lista de eventos
        for event in eventList:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:    # Tecla Esc, menú de pausa
                    self.pauseScene()
                elif event.key == pg.K_n:       # Tecla N, siguiente escena (solo para debug)
                    self.nextScene()
            elif event.type == pg.QUIT:
                self.director.exitProgram()


    # -----------------------------------------------------
    # Scene transitions

    def pauseScene(self):
        pg.mouse.set_visible(True)
        scene = PauseMenu(self.director)
        Music.volumeMusic(self, 0.25)
        self.director.stackScene(scene)
    
    def losingScene(self):
        pg.mouse.set_visible(True)
        scene = LosingMenu(self.director)
        self.director.stackScene(scene)

    def nextScene(self):
        pass
