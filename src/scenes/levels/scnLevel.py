import time

import pygame as pg
from src.scenes.music import *
from src.scenes.recordManager import updateRecords
from src.scenes.resourceManager import ResourceManager
from src.scenes.scene import Scene
from src.scenes.scnLosing import LosingMenu
from src.scenes.scnPause import PauseMenu
from src.scenes.score import getScore
from src.settings.settings import *


class Level(Scene):

    def __init__(self, director):
        #Initialize superclass
        Scene.__init__(self, director)

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

        self.text_menu = None
        self.has_menu = False
        self.draw_dineros = False
        self.time_dineros = None
        self.show_time_dineros = 3

        # Dialogue variables
        self.resetDialogue()

        #Loads all sprite and sound data
        self.load_data()
    
    def reset(self):
        self.__init__(self.director)

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

            from src.scenes.survival.scnSurvival import \
                Survival  # TODO: para evitar bucle en imports

            # Si estamos en Survival
            if type(self) == Survival:
                # Actualizamos mejores puntuaciones
                currentScore = getScore()
                updateRecords(currentScore)
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
        self.drawDialogue()
        self.drawDineros()
        self.hud.draw_health(screen)

    def drawDialogue(self):
        if not self.dialogue_cooldown and self.dialogue:
            letter = self.dialogue.pop(0)
            self.dialogue_cooldown = 5
            self.text_lines[self.dialogue_line].append(letter)
        if self.dialogue_cooldown:
            self.dialogue_cooldown -= 1

        y_offset0 = 250
        y_offset1 = 300
        y_offset2 = 350

        phrase0 = ''.join(self.text_lines[0])
        phrase1 = ''.join(self.text_lines[1])
        phrase2 = ''.join(self.text_lines[2])

        text_surface0, rect0 = self.game_font.render(phrase0, (200, 200, 200))
        text_surface1, rect1 = self.game_font.render(phrase1, (200, 200, 200))
        text_surface2, rect2 = self.game_font.render(phrase2, (200, 200, 200))
        self.screen.blit(text_surface0, (WIDTH / 2 - 500, (HEIGHT / 2) + y_offset0))
        self.screen.blit(text_surface1, (WIDTH / 2 - 500, (HEIGHT / 2) + y_offset1))
        self.screen.blit(text_surface2, (WIDTH / 2 - 500, (HEIGHT / 2) + y_offset2))

        if self.active_dialogue and len(self.text_lines[self.dialogue_line]) >= self.dialogue_length:
            if len(self.remainder_dialogue) > 0:
                self.active_dialogue = False
                self.dialogue_line += 1
                self.updateDialogue(self.remainder_dialogue)
            else:
                self.dialogue_continuation = True

    def updateDialogue(self, textLine):
        self.dialogue_continuation = False
        self.total_lines = len(textLine)
        if not self.active_dialogue:
            self.completly_finished = False
            if self.dialogue_line == 0:
                self.firstBatch=textLine[:3]
                self.remainderBatch=textLine[3:]
                self.total_lines_batch = len(self.firstBatch)
                textLine = self.firstBatch

            self.player.stopMovement()
            self.active_dialogue = True
            self.lines = len(textLine)
            self.dialogue = list(textLine[0])
            self.remainder_dialogue = textLine[1:]
            self.dialogue_length = len(self.dialogue)
        elif self.dialogue_line == self.total_lines_batch - 1 and len(self.text_lines[self.dialogue_line]) >= self.dialogue_length and not self.skip_dialogue:
            self.active_dialogue = False
            self.prev_text = []
            if not self.has_menu:
                self.text_lines[0] = []
                self.text_lines[1] = []
                self.text_lines[2] = []
            self.dialogue_line = 0
            if len(self.remainderBatch) > 0:
                self.updateDialogue(self.remainderBatch)
            else:
                self.completly_finished = True
        elif len(self.text_lines[0]) >= 2:
            self.skip_dialogue = True
            self.dialogue_cooldown = 0

    def stopText(self):
        self.skip_dialogue = False

    def resetDialogue(self):
        self.dialogue = None
        self.remainder_dialogue = None
        self.active_dialogue = False
        self.skip_dialogue = False
        self.dialogue_cooldown = 0
        self.prev_text = []
        self.text_line0 = []
        self.text_line1 = []
        self.text_line2 = []
        self.text_lines = [self.text_line0, self.text_line1, self.text_line2]
        self.dialogue_length = 0
        self.dialogue_line = 0
        self.lines = 0
        self.completly_finished = False
        self.dialogue_continuation = False
        if self.player:
            self.player.allowMovement()

    def drawMenu(self):
        if self.text_menu:
            phrase5 = ''.join(self.text_line0)
            phrase0 = self.text_menu[0]
            phrase1 = self.text_menu[1]
            phrase2 = self.text_menu[2]
            phrase3 = self.text_menu[3]
            phrase4 = self.text_menu[4]
            text_surface5, rect5 = self.game_font.render(phrase5, (200, 200, 200))
            text_surface0, rect0 = self.game_font.render(phrase0, (200, 200, 200))
            text_surface1, rect1 = self.game_font.render(phrase1, (200, 200, 200))
            text_surface2, rect2 = self.game_font.render(phrase2, (200, 200, 200))
            text_surface3, rect3 = self.game_font.render(phrase3, (200, 200, 200))
            text_surface4, rect4 = self.game_font.render(phrase4, (200, 200, 200))
            self.screen.blit(text_surface0, (WIDTH / 2 + 230, (HEIGHT / 2) - 130))
            self.screen.blit(text_surface1, (WIDTH / 2 + 230, (HEIGHT / 2) - 70))
            self.screen.blit(text_surface2, (WIDTH / 2 + 230, (HEIGHT / 2) - 10))
            self.screen.blit(text_surface3, (WIDTH / 2 + 230, (HEIGHT / 2) + 50))
            self.screen.blit(text_surface4, (WIDTH / 2 + 230, (HEIGHT / 2) + 140))
            self.screen.blit(text_surface5, (WIDTH / 2 - 500, (HEIGHT / 2) + 250))

    def drawDineros(self):
        if self.draw_dineros:
            if not self.time_dineros:
                self.time_dineros = time.time()
            time_fin = time.time()
            self.hud.dineros.activate()
            text_surface5, rect5 = self.game_font.render(str(self.player.los_dineros)+'$', (200, 200, 200))
            #self.game_font.set_bold(True)
            self.screen.blit(text_surface5, (WIDTH / 2 - 680, (HEIGHT / 2) - 340))
            if time_fin - self.time_dineros > self.show_time_dineros:
                self.draw_dineros = False
                self.time_dineros = None
                self.hud.dineros.deactivate()


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
        Music.volumemusic(self, 0.25)
        self.director.stackScene(scene)
    
    def losingScene(self):
        pg.mouse.set_visible(True)
        scene = LosingMenu(self.director)
        self.director.stackScene(scene)

    def nextScene(self):
        pass
