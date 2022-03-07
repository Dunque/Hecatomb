import pygame as pg
from src.scenes.levels.scnLevel1 import Level1
from src.scenes.resourceManager import ResourceManager
from src.scenes.scene import Scene
from src.scenes.scnPause import PauseMenu
from src.settings.settings import *


class Cutscene1(Scene):

    def __init__(self, sceneManager):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, sceneManager);
        # Creamos la imagen de fondo
        # self.image = ResourceManager.LoadImage('resources/images/intro.png')

    def update(self, *args):
        return

    def events(self, eventList):
        # Se mira la lista de eventos
        for event in eventList:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:    # Tecla Esc, menú de pausa
                    self.pauseScene()
                elif event.key == pg.K_n:       # Tecla N, siguiente escena (solo para debug)
                    self.nextScene()
            elif event.type == pg.QUIT:
                self.sceneManager.exitProgram()

    def draw(self, screen):
        # Dibujamos imagen de fondo
        # screen.blit(self.image, self.image.get_rect())
        screen.fill(BLUE)

        # Dibujamos nombre de escena (para debug)
        font = pg.font.Font(HANSHAND_FONT, 192)
        text = font.render('Cutscene1', True, BLACK)
        textRect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, textRect)


    # -----------------------------------------------------
    # Métodos propios de la escena

    def pauseScene(self):
        scene = PauseMenu(self.sceneManager)
        self.sceneManager.stackScene(scene)

    def nextScene(self):
        scene = Level1(self.sceneManager)
        self.sceneManager.changeScene(scene)
