import pygame as pg
from resourceManager import *
from scene import *
from settings import *
from scnMenu import *


class Intro(Scene):

    def __init__(self, sceneManager):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, sceneManager);
        # Creamos la imagen de fondo
        self.image = ResourceManager.LoadImage('resources/images/intro.png')

    def update(self, *args):
        return

    def events(self, eventList):
        # Se mira si se quiere: salir, continuar
        for event in eventList:
            # En ese caso, se le indica al sceneManager
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:   # Tecla Esc, salir
                    self.exitProgram()
                else:                       # Cualquier otra tecla, continuar
                    self.nextScene()
            elif event.type == pg.MOUSEBUTTONDOWN:  # Click ratón, continuar
                self.nextScene()
            elif event.type == pg.QUIT:
                self.sceneManager.exitProgram()

    def draw(self, screen):
        # Dibujamos imagen de fondo
        screen.blit(self.image, self.image.get_rect())

        # Dibujamos título del juego y mensaje
        fontName = 'resources/fonts/hanshand.ttf'

        font = pg.font.Font(fontName, 192)
        text = font.render('HECATOMB', True, DARK_RED)
        text.set_alpha(192)
        textRect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, textRect)

        font = pg.font.Font(fontName, 48)
        text = font.render('Pulse cualquier tecla para continuar', True, BLACK)
        textRect = text.get_rect(center=(WIDTH/2, HEIGHT/3*2))
        screen.blit(text, textRect)


    #--------------------------------------
    # Metodos propios del menu

    def exitProgram(self):
        self.sceneManager.exitProgram()

    def nextScene(self):
        scene = Menu(self.sceneManager)
        self.sceneManager.changeScene(scene)
