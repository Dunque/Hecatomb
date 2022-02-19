import pygame as pg
import sys
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.player = None

    def load_data(self):
        #MAP DATA
        self.map = Map(self, './maps/map4.txt')

        #PLAYER DATA
        self.playerWalkSheet = pg.image.load("./sprites/playerWalkSheet.png").convert_alpha()
        self.playerIdleSheet = pg.image.load("./sprites/playerIdleSheet.png").convert_alpha()
        self.playerDodgeSheet =  pg.image.load("./sprites/playerDodgeSheet.png").convert_alpha()
        self.playerDeathSheet =  pg.image.load("./sprites/playerDeathSheet.png").convert_alpha()
        self.playerGunImg = pg.image.load("./sprites/gun.png").convert_alpha()
        self.playerSwordImg = pg.image.load("./sprites/sword.png").convert_alpha()

        #HUD
        self.radialMenuImg = pg.image.load("./sprites/radial_menu.png").convert_alpha()

        # MOB DATA
        self.wormWalkSheet = pg.image.load("./sprites/Worm/Walk.png").convert_alpha()
        self.wormIdleSheet = pg.image.load("./sprites/Worm/Idle.png").convert_alpha()
        self.wormHitSheet = pg.image.load("./sprites/Worm/GetHit.png").convert_alpha()
        self.wormDeathSheet = pg.image.load("./sprites/Worm/Death.png").convert_alpha()
        self.wormAttackSheet = pg.image.load("./sprites/Worm/Attack.png").convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.menus = []

        self.map.generateMap()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            hit.currentState = "ATTACK"
        for menu in self.menus:
            menu.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
 
