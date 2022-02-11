import sys
from tty import setcbreak
import pygame as pg
from os import path
from pygame.locals import *
from src.settings import *
from src.sprites import Player, Wall, Mouse
from src.tilemap import Map, Camera
from src.scenes.scene import Scene
from src.characters import *

class Act2(Scene):

    def __init__(self, scene_manager):
        self.screen = pg.display.get_surface()
        self.scene_manager = scene_manager

        self.jugador1 = Jugador()
        self.grupoJugadores = pg.sprite.Group( self.jugador1)
        self.jugador1.establecerPosicion((200, 551))
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pg.sprite.Group( self.jugador1)
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pg.sprite.Group( self.jugador1)

    def on_scene_enter(self):
        pass

    def on_scene_quit(self):
        pass

    def handle_event(self, event_list):
        # Miramos a ver si hay algun evento de salir del programa
        for event in event_list:
            # Si se quiere salir, se le indica al scene_manager
            if event.type == pygame.QUIT:
                self.scene_manager.quit_program()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_w,  K_s,    K_a,    K_d)

    def update(self, time):

        # Actualizamos los Sprites dinamicos
        # De esta forma, se simula que cambian todos a la vez
        # Esta operación de update ya comprueba que los movimientos sean correctos
        #  y, si lo son, realiza el movimiento de los Sprites
        self.grupoSpritesDinamicos.update(self.jugador1, time)


    def render(self):
        self.screen.fill(TURQUOISE)
        self.grupoSprites.draw(self.screen)
