import pygame as pg
import sys
from scene import *
from settings import *
from sprites import *
from tilemap import *

class Level1(Scene):
    def __init__(self, sceneManager):
        #Initialize superclass
        Scene.__init__(self, sceneManager)

        #Loads all sprite and sound data
        self.load_data()

        #Initialize sprite groups
        self.all_sprites = pg.sprite.Group()
        self.background_SG = pg.sprite.Group()
        self.walls_SG = pg.sprite.Group()
        self.mobs_SG = pg.sprite.Group()
        self.bully_SG = pg.sprite.Group()
        self.player_SG = pg.sprite.Group()
        self.fireBalls_SG = pg.sprite.Group()
        self.bullets_SG = pg.sprite.Group()
        self.weapons_SG = pg.sprite.Group()
        self.floor = pg.sprite.Group()
        self.menus = []

        self.player = None

        #Generate a map
        self.map.generateMap()

    def load_data(self):
        #MAP DATA
        self.map = Map(self, './maps/map4.txt')

        #PLAYER DATA
        self.playerWalkSheet = pg.image.load("./sprites/Player/playerWalkSheet.png").convert_alpha()
        self.playerIdleSheet = pg.image.load("./sprites/Player/playerIdleSheet.png").convert_alpha()
        self.playerDodgeSheet =  pg.image.load("./sprites/Player/playerDodgeSheet.png").convert_alpha()
        self.playerDeathSheet =  pg.image.load("./sprites/Player/playerDeathSheet.png").convert_alpha()
        self.playerGunImg = pg.image.load("./sprites/Weapons/gun.png").convert_alpha()
        self.playerSwordImg = pg.image.load("./sprites/Weapons/sword.png").convert_alpha()

        # MOB DATA
        self.wormWalkSheet = pg.image.load("./sprites/Worm/Walk.png").convert_alpha()
        self.wormIdleSheet = pg.image.load("./sprites/Worm/Idle.png").convert_alpha()
        self.wormHitSheet = pg.image.load("./sprites/Worm/GetHit.png").convert_alpha()
        self.wormDeathSheet = pg.image.load("./sprites/Worm/Death.png").convert_alpha()
        self.wormAttackSheet = pg.image.load("./sprites/Worm/Attack.png").convert_alpha()
        #BULLETS/AMMUNITION DATA
        self.bulletImg = pg.image.load("./sprites/Fire_Ball/bullet.png").convert_alpha()
        self.fire_ballMoveSheet = pg.image.load(
            "./sprites/Fire_Ball/Move.png").convert_alpha()
        self.fire_ballExplosionSheet = pg.image.load(
            "./sprites/Fire_Ball/Explosion.png").convert_alpha()

        #BULLY DATA
        self.BullyWalkSheet = pg.image.load("./sprites/Bully/moverDer.png").convert_alpha()
        self.BullyIdleSheet = pg.image.load("./sprites/Bully/quieto.png").convert_alpha()
        self.BullyDeathSheet = pg.image.load("./sprites/Bully/morir.png").convert_alpha()
        self.BullyAttackSheet = pg.image.load("./sprites/Bully/atacarderecha.png").convert_alpha()

        #HUD
        self.radialMenuImg = pg.image.load(
            "./sprites/Hud/radial_menu.png").convert_alpha()
        self.gunCrosshairImg = pg.image.load(
            "./sprites/Hud/gun_crosshair.png").convert_alpha()

    def update(self, time):
        self.dt = time
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.mobs_SG, False, collide_hit_rect)
        hits = pg.sprite.spritecollide(self.player, self.bully_SG, False, collide_hit_rect)
        for hit in hits:
            hit.currentState = "ATTACK"
        for menu in self.menus:
            menu.update()

        self.map.update()

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

    def events(self, eventList):
        # catch all events here
        for event in eventList:
            if event.type == pg.QUIT:
                self.sceneManager.exitScene()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.sceneManager.exitScene()
