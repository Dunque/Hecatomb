import pygame as pg
from src.scenes.resourceManager import ResourceManager
from src.scenes.scene import Scene
from src.scenes.scnMenu import Menu
from src.settings.settings import *


class Intro(Scene):

    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, director)
        # Se carga la imagen de fondo
        self.image = ResourceManager.LoadImage('resources/images/intro.png')
        self.image = pg.transform.scale(self.image, (WIDTH, HEIGHT))

    def update(self, *args):
        return

    def events(self, eventList):
        # Se mira la lista de eventos
        for event in eventList:
            if event.type == pg.KEYDOWN:            # Cualquier tecla, menú principal
                self.nextScene()
            elif event.type == pg.MOUSEBUTTONDOWN:  # Cualquier botón del ratón, menú principal
                self.nextScene()
            elif event.type == pg.QUIT:
                self.director.exitProgram()

    def draw(self, screen):
        # Dibujamos imagen de fondo
        screen.blit(self.image, self.image.get_rect())

        # Dibujamos título del juego
        font = pg.font.Font(HANSHAND_FONT, 224)
        text = font.render('HECATOMB', True, MAROON)
        textRect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, textRect)

        # Dibujamos mensaje
        font = pg.font.Font(HANSHAND_FONT, 48)
        text = font.render('Pulse cualquier tecla para continuar', True, BLACK)
        textRect = text.get_rect(center=(WIDTH/2, HEIGHT/3*2))
        screen.blit(text, textRect)


    # -----------------------------------------------------
    # Métodos propios de la escena

    def nextScene(self):
        scene = Menu(self.director)
        self.director.changeScene(scene)
