import pygame as pg
import sys
from src.scenes.scene import *
from src.settings.settings import *
from src.entities.character import *
from src.map.tilemap import *
from src.hud.hud import Hud, Line
from src.scenes.cutscenes.scnCutscene2 import *


class Level1(Scene):
    def __init__(self, sceneManager):
        #Initialize superclass
        Scene.__init__(self, sceneManager)

        #Initialize sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.background_SG = pg.sprite.LayeredUpdates()
        self.walls_SG = pg.sprite.LayeredUpdates()
        self.mobs_SG = pg.sprite.LayeredUpdates()
        self.player_SG = pg.sprite.LayeredUpdates()
        self.npc_SG = pg.sprite.LayeredUpdates()
        self.bullets_SG = pg.sprite.LayeredUpdates()
        self.weapons_SG = pg.sprite.LayeredUpdates()
        self.floors_SG = pg.sprite.LayeredUpdates()
        self.chest_SG = pg.sprite.LayeredUpdates()
        self.menus = []

        self.screen = None

        self.player = None

        #Loads all sprite and sound data
        self.load_data()

    def load_data(self):
        #PLAYER DATA
        self.playerWalkSheet = pg.image.load("./sprites/Player/playerWalkSheet.png").convert_alpha()
        self.playerIdleSheet = pg.image.load("./sprites/Player/playerIdleSheet.png").convert_alpha()
        self.playerDodgeSheet =  pg.image.load("./sprites/Player/playerDodgeSheet.png").convert_alpha()
        self.playerDeathSheet =  pg.image.load("./sprites/Player/playerDeathSheet.png").convert_alpha()
        self.playerGunImg = pg.image.load("./sprites/Weapons/gun.png").convert_alpha()
        self.playerShotgunImg = pg.image.load("./sprites/Weapons/shotgun.png").convert_alpha()
        self.playerSwordImg = pg.image.load("./sprites/Weapons/sword.png").convert_alpha()
        self.chestImg = pg.image.load("./sprites/Objects/chest.png").convert_alpha()

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

        #NPC
        self.npc1Profile = pg.image.load("./sprites/Player/profile1.png").convert_alpha()

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

        #Map generation
        self.map = Map(self, './maps/rooms.txt')

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
        self.camera.update(self.player)

        if not self.player_SG.has(self.player):
            scene1 = Level1(self.sceneManager)
            self.sceneManager.changeScene(scene1)
            
        # hits = pg.sprite.spritecollide(self.player, self.mobs_SG, False, collide_hit_rect)
        # for hit in hits:
        #     hit.currentState = "ATTACKING"
        for menu in self.menus:
            menu.update()

        self.map.update()
        pg.display.set_caption(str(time))

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self, screen):
        self.screen = screen
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
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

        text_surface0, rect0 = self.game_font.render(phrase0, (255, 255, 255))
        text_surface1, rect1 = self.game_font.render(phrase1, (255, 255, 255))
        text_surface2, rect2 = self.game_font.render(phrase2, (255, 255, 255))
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

    def events(self, eventList):
        # catch all events here
        for event in eventList:
            if event.type == pg.QUIT:
                pg.mouse.set_visible(True)
                self.sceneManager.exitScene()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.mouse.set_visible(True)
                    self.sceneManager.exitScene()
                elif event.key == K_n:          # Tecla N, siguiente escena (solo para debug)
                    self.nextScene()


    #--------------------------------------
    # Metodos propios

    def nextScene(self):
        scene = Cutscene2(self.sceneManager)
        self.sceneManager.changeScene(scene)
