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

        #Initialize sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.background_SG = pg.sprite.LayeredUpdates()
        self.walls_SG = pg.sprite.LayeredUpdates()
        self.mobs_SG = pg.sprite.LayeredUpdates()
        self.player_SG = pg.sprite.LayeredUpdates()
        self.fireBalls_SG = pg.sprite.LayeredUpdates()
        self.bullets_SG = pg.sprite.LayeredUpdates()
        self.weapons_SG = pg.sprite.LayeredUpdates()
        self.floors_SG = pg.sprite.LayeredUpdates()
        self.menus = []

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

        #BULLETS/AMMUNITION DATA
        self.gunBulletImg = pg.image.load("./sprites/Fire_Ball/gun_bullet.png").convert_alpha()
        self.fire_ballMoveSheet = pg.image.load(
            "./sprites/Fire_Ball/Move.png").convert_alpha()
        self.fire_ballExplosionSheet = pg.image.load(
            "./sprites/Fire_Ball/Explosion.png").convert_alpha()

        #HUD
        self.radialMenuImg = pg.image.load(
            "./sprites/Hud/radial_menu.png").convert_alpha()
        self.gunCrosshairImg = pg.image.load(
            "./sprites/Hud/gun_crosshair.png").convert_alpha()
        self.shotgunCrosshairImg = pg.image.load(
            "./sprites/Hud/shotgun_crosshair.png").convert_alpha()

        # MOB DATA
        self.wormWalkSheet = pg.image.load("./sprites/Worm/Walk.png").convert_alpha()
        self.wormIdleSheet = pg.image.load("./sprites/Worm/Idle.png").convert_alpha()
        self.wormHitSheet = pg.image.load("./sprites/Worm/GetHit.png").convert_alpha()
        self.wormDeathSheet = pg.image.load("./sprites/Worm/Death.png").convert_alpha()
        self.wormAttackSheet = pg.image.load("./sprites/Worm/Attack.png").convert_alpha()

        #BULLY DATA
        self.BullyWalkSheet = pg.image.load("./sprites/Bully/mover.png").convert_alpha()
        self.BullyIdleSheet = pg.image.load("./sprites/Bully/quieto.png").convert_alpha()
        self.BullyDeathSheet = pg.image.load("./sprites/Bully/morir.png").convert_alpha()
        self.BullyAttackSheet = pg.image.load("./sprites/Bully/ataq.png").convert_alpha()

        #MAP BACKGROUNDS
        self.background1 = pg.image.load("./sprites/background1.png").convert_alpha()
        self.background2 = pg.image.load("./sprites/background2.png").convert_alpha()
        self.background3 = pg.image.load("./sprites/background3.png").convert_alpha()
        self.background4 = pg.image.load("./sprites/background4.png").convert_alpha()

        #Map generation
        self.map = Map(self, './maps/rooms.txt')

    def update(self, time):
        self.dt = time
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.mobs_SG, False, collide_hit_rect)
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
