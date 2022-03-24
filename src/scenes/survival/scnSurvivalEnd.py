import pygame as pg
from src.scenes.resourceManager import ResourceManager
from src.scenes.scene import Scene
from src.settings.settings import *


class SurvivalEnd(Scene):

    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, director);
        # Creamos la imagen de fondo
        # self.image = ResourceManager.LoadImage('resources/images/intro.png')

    def update(self, *args):
        return

    def events(self, eventList):
        # Se mira la lista de eventos
        for event in eventList:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_n:       # Tecla N, siguiente escena (solo para debug)
                    self.exitScene()
            elif event.type == pg.QUIT:
                self.director.exitProgram()

    def draw(self, screen):
        # Dibujamos imagen de fondo
        # screen.blit(self.image, self.image.get_rect())
        screen.fill(GREEN)

        # Dibujamos nombre de escena (para debug)
        font = pg.font.Font(GUI_FONT, 192)
        text = font.render('SurvivalEnd', True, BLACK)
        textRect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, textRect)


    # -----------------------------------------------------
    # Scene transitions

    def exitScene(self):
        self.director.exitScene()
