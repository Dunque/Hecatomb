import pygame as pg
from src.scenes.resourceManager import *
from src.scenes.scene import *
from src.settings.settings import *


class SurvivalEnd(Scene):

    def __init__(self, sceneManager):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, sceneManager);
        # Creamos la imagen de fondo
        # self.image = ResourceManager.LoadImage('resources/images/intro.png')

    def update(self, *args):
        return

    def events(self, eventList):
        # Se mira si se quiere hacer algo
        for event in eventList:
            # En ese caso, se le indica al sceneManager
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:   # Tecla Esc, salir
                    self.exitProgram()
                elif event.key == K_n:      # Tecla N, siguiente escena (solo para debug)
                    self.nextScene()

            elif event.type == pg.QUIT:
                self.sceneManager.exitProgram()

    def draw(self, screen):
        # Dibujamos imagen de fondo
        # screen.blit(self.image, self.image.get_rect())
        screen.fill(GREEN)

        # Dibujamos nombre de escena (para debug)
        fontName = 'resources/fonts/hanshand.ttf'

        font = pg.font.Font(fontName, 192)
        text = font.render('SurvivalEnd', True, WHITE)
        textRect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, textRect)


    #--------------------------------------
    # Metodos propios del menu

    def exitProgram(self):
        self.sceneManager.exitProgram()

    def nextScene(self):
        self.sceneManager.exitScene()
