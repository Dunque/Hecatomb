import pygame as pg
from src.entities.character import Character
from src.hud.hud import Hud
from src.map.randmap import RandMap
from src.map.staticmap import StaticMap
from src.scenes.scene import Scene
from src.scenes.scnPause import PauseMenu
from src.scenes.survival.scnSurvivalEnd import SurvivalEnd
from src.settings.settings import *


class Survival(Scene):
    pg.mixer.music.play(-1)

    def __init__(self, director):
        #Initialize superclass
        Scene.__init__(self, director)

        #Initialize sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.background_SG = pg.sprite.LayeredUpdates()
        self.walls_SG = pg.sprite.LayeredUpdates()
        self.mobs_SG = pg.sprite.LayeredUpdates()
        self.player_SG = pg.sprite.LayeredUpdates()
        self.bullets_SG = pg.sprite.LayeredUpdates()
        self.weapons_SG = pg.sprite.LayeredUpdates()
        self.floors_SG = pg.sprite.LayeredUpdates()
        self.chest_SG = pg.sprite.LayeredUpdates()
        self.menus = []

        self.player = None

        #Loads all sprite and sound data
        self.load_data()
    
    def reset(self):
        self.__init__(self.director)

    def load_data(self):
        #PLAYER DATA
        self.playerWalkSheet = pg.image.load(
            "./sprites/Player/playerWalkSheet.png").convert_alpha()
        self.playerIdleSheet = pg.image.load(
            "./sprites/Player/playerIdleSheet.png").convert_alpha()
        self.playerDodgeSheet = pg.image.load(
            "./sprites/Player/playerDodgeSheet.png").convert_alpha()
        self.playerDeathSheet = pg.image.load(
            "./sprites/Player/playerDeathSheet.png").convert_alpha()
        self.playerGunImg = pg.image.load(
            "./sprites/Weapons/gun.png").convert_alpha()
        self.playerShotgunImg = pg.image.load(
            "./sprites/Weapons/shotgun.png").convert_alpha()
        self.playerSwordImg = pg.image.load(
            "./sprites/Weapons/sword.png").convert_alpha()
        self.chestImg = pg.image.load(
            "./sprites/Objects/chest.png").convert_alpha()

        #BULLETS/AMMUNITION DATA
        self.gunBulletImg = pg.image.load(
            "./sprites/Fire_Ball/gun_bullet.png").convert_alpha()
        self.fire_ballMoveSheet = pg.image.load(
            "./sprites/Fire_Ball/Move.png").convert_alpha()
        self.fire_ballExplosionSheet = pg.image.load(
            "./sprites/Fire_Ball/Explosion.png").convert_alpha()

        #HUD
        self.radialMenuImg = pg.image.load(
            "./sprites/Hud/radial_menu.png").convert_alpha()
        self.abrirImg = pg.image.load(
            "./sprites/Hud/abrir.png").convert_alpha()
        self.gunCrosshairImg = pg.image.load(
            "./sprites/Hud/gun_crosshair.png").convert_alpha()
        self.shotgunCrosshairImg = pg.image.load(
            "./sprites/Hud/shotgun_crosshair.png").convert_alpha()

        # WORM DATA
        self.wormWalkSheet = pg.image.load(
            "./sprites/Worm/Walk.png").convert_alpha()
        self.wormIdleSheet = pg.image.load(
            "./sprites/Worm/Idle.png").convert_alpha()
        self.wormHitSheet = pg.image.load(
            "./sprites/Worm/GetHit.png").convert_alpha()
        self.wormDeathSheet = pg.image.load(
            "./sprites/Worm/Death.png").convert_alpha()
        self.wormAttackSheet = pg.image.load(
            "./sprites/Worm/Attack.png").convert_alpha()

        #Khan DATA
        self.khanWalkSheet = pg.image.load(
            "./sprites/Khan/khanWalkSheet.png").convert_alpha()
        self.khanDeathSheet = pg.image.load(
            "./sprites/Khan/khanDeathSheet.png").convert_alpha()

        #HERALD DATA
        self.heraldWalkSheet = pg.image.load(
            "./sprites/Herald/heraldWalkSheet.png").convert_alpha()
        self.heraldDeathSheet = pg.image.load(
            "./sprites/Herald/heraldDeathSheet.png").convert_alpha()

        #MAP BACKGROUNDS
        self.background1 = pg.image.load(
            "./sprites/background1.png").convert_alpha()
        self.background2 = pg.image.load(
            "./sprites/background2.png").convert_alpha()
        self.background3 = pg.image.load(
            "./sprites/background3.png").convert_alpha()
        self.background4 = pg.image.load(
            "./sprites/background4.png").convert_alpha()

        #Map generation
        self.map = RandMap(self, './maps/rooms.txt')

        self.hud = Hud(self)

    def update(self, time):
        self.dt = time
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        if not self.player_SG.has(self.player):
            scene1 = Survival(self.director)
            self.director.changeScene(scene1)

        for menu in self.menus:
            menu.update()

        self.map.update()
        pg.display.set_caption(str(time))

    def draw(self, screen):
        self.screen = screen
        self.screen.fill(BGCOLOR)

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
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
    # Métodos propios de la escena

    def pauseScene(self):
        scene = PauseMenu(self.director)
        self.director.stackScene(scene)

    def nextScene(self):
        scene = SurvivalEnd(self.director)
        self.director.changeScene(scene)
