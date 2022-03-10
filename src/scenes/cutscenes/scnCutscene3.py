import pygame as pg
from src.scenes.levels.scnLevel3 import Level3
from src.scenes.resourceManager import ResourceManager
from src.scenes.scene import Scene
from src.scenes.scnPause import PauseMenu
from src.settings.settings import *
from src.scenes.music import *

class Cutscene3(Scene):

    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, director);
        # Creamos la imagen de fondo
        # self.image = ResourceManager.LoadImage('resources/images/intro.png')
    
    def reset(self):
        self.__init__(self.director)

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
                self.director.exitProgram()

    def draw(self, screen):
        # Dibujamos imagen de fondo
        # screen.blit(self.image, self.image.get_rect())
        screen.fill(BLUE)

        # Dibujamos nombre de escena (para debug)
        font = pg.font.Font(HANSHAND_FONT, 192)
        text = font.render('Cutscene3', True, BLACK)
        textRect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, textRect)


    # -----------------------------------------------------
    # Métodos propios de la escena

    def pauseScene(self):
        scene = PauseMenu(self.director)
        Music.volumemusic(self, 0.25)
        self.director.stackScene(scene)

    def nextScene(self):
        scene = Level3(self.director)
        Music.changemusic(self, 3)
        self.director.changeScene(scene)
