import pygame as pg
from src.hud.hud import Hud
from src.map.staticmap import StaticMap
from src.scenes.cutscenes.scnCutscene2 import Cutscene2
from src.scenes.scene import Scene
from src.scenes.scnLosing import LosingMenu
from src.scenes.scnPause import PauseMenu
from src.settings.settings import *
from src.entities.character import *
from src.map.randmap import *
from src.hud.hud import Hud, Line


class Level1(Scene):

    def __init__(self, director):
        #Initialize superclass
        Scene.__init__(self, director)

        #Initialize sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.all_hud = pg.sprite.LayeredUpdates()
        self.background_SG = pg.sprite.LayeredUpdates()
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
        self.iluminacion = True

        self.fog = pg.Surface((WIDTH, HEIGHT))

        #Exit condition: player must interact with an amount of npcs to exit the level
        self.talkedCount = 0
        self.canExit = False

        #Loads all sprite and sound data
        self.load_data()
    
    def reset(self):
        self.__init__(self.director)

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


        self.chestImg = pg.image.load("./sprites/Objects/chest.png").convert_alpha()
        self.candelabroImg = pg.image.load("./sprites/Objects/candelabro.png").convert_alpha()

        #BULLETS/AMMUNITION DATA
        self.gunBulletImg = pg.image.load("./sprites/Fire_Ball/gun_bullet.png").convert_alpha()
        self.fire_ballMoveSheet = pg.image.load(
            "./sprites/Fire_Ball/Move.png").convert_alpha()
        self.fire_ballExplosionSheet = pg.image.load(
            "./sprites/Fire_Ball/Explosion.png").convert_alpha()

        #HUD
        self.radialMenuImg = pg.image.load(
            "./sprites/Hud/radial_menu.png").convert_alpha()
        self.abrirImg = pg.image.load("./sprites/Hud/abrir.png").convert_alpha()
        self.hablarImg = pg.image.load("./sprites/Hud/hablar.png").convert_alpha()
        self.gunCrosshairImg = pg.image.load(
            "./sprites/Hud/gun_crosshair.png").convert_alpha()
        self.shotgunCrosshairImg = pg.image.load(
            "./sprites/Hud/shotgun_crosshair.png").convert_alpha()
        self.dialogueBox = pg.image.load("./sprites/Hud/dialoguebox.png").convert_alpha()
        self.dialogueContinuation = pg.image.load("./sprites/Hud/continuation.png").convert_alpha()
        self.game_font = pg.freetype.Font("./sprites/Hud/impostor.ttf", 24)
        self.light_mask = pg.transform.scale(pg.image.load("./sprites/Hud/light_350_soft.png").convert_alpha(), (1000, 1000))

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

        #HERALD DATA
        self.heraldWalkSheet = pg.image.load("./sprites/Herald/heraldWalkSheet.png").convert_alpha()
        self.heraldDeathSheet = pg.image.load("./sprites/Herald/heraldDeathSheet.png").convert_alpha()


        #MAP BACKGROUNDS
        self.background1 = pg.image.load("./sprites/background1.png").convert_alpha()
        self.background2 = pg.image.load("./sprites/background2.png").convert_alpha()
        self.background3 = pg.image.load("./sprites/background3.png").convert_alpha()
        self.background4 = pg.image.load("./sprites/background4.png").convert_alpha()

        self.dialogues_src = "./resources/text/dialogues.txt"

        self.exitImage = pg.image.load(
            "./sprites/Objects/exit.png").convert_alpha()

        #Map generation
        self.map = StaticMap(self, './maps/map1.txt')

        self.hud = Hud(self)

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

    def update(self, time):
        self.dt = time
        # update portion of the game loop
        self.all_sprites.update()
        self.all_hud.update()
        self.camera.update(self.player)

        # Si el jugado ha muerto
        if not self.player_SG.has(self.player):
            self.losingScene()

        #Exit condition
        if self.talkedCount >= 4:
            self.canExit = True

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

        #Fog
        if self.iluminacion:
            self.render_fog()
            for sprite in list(self.candelabros_SG):
                self.render_fog(sprite)
            self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

        #Hud
        for hud in self.all_hud:
            self.screen.blit(hud.image, self.camera.apply(hud))
        self.drawDialogue()
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
            self.text_lines[0] = []
            self.text_lines[1] = []
            self.text_lines[2] = []
            self.dialogue_line = 0
            self.player.allowMovement()
            if len(self.remainderBatch) > 0:
                self.updateDialogue(self.remainderBatch)
            else:
                self.completly_finished = True
        elif len(self.text_lines[0]) >= 2:
            self.skip_dialogue = True
            self.dialogue_cooldown = 0

    def stopText(self):
        self.skip_dialogue = False

    def render_fog(self, sprite = None):
        self.light_rect = self.light_mask.get_rect()
        if not sprite:
            self.fog.fill(LIGHTGREY)
            self.light_rect.center = self.camera.apply(self.player).center
        else:
            self.light_rect.center = self.camera.apply(sprite).center
        self.fog.blit(self.light_mask, self.light_rect)

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
    # Métodos propios de la escena

    def pauseScene(self):
        pg.mouse.set_visible(True)
        scene = PauseMenu(self.director)
        self.director.stackScene(scene)
    
    def losingScene(self):
        pg.mouse.set_visible(True)
        scene = LosingMenu(self.director)
        self.director.stackScene(scene)

    def nextScene(self):
        pg.mouse.set_visible(True)
        scene = Cutscene2(self.director)
        self.director.changeScene(scene)
