import pygame as pg
from src.scenes.resourceManager import ResourceManager
from src.scenes.scene import Scene
from src.scenes.scnMenu import Menu
from src.settings.settings import *


class Intro(Scene):

    def __init__(self, sceneManager):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, sceneManager)
        # Se carga la imagen de fondo
        self.image = ResourceManager.LoadImage('resources/images/intro.png')
        self.image = pg.transform.scale(self.image, (WIDTH, HEIGHT))

    def update(self, *args):
        return

    def events(self, eventList):
        # Se mira la lista de eventos
        for event in eventList:
            if event.type == pg.KEYDOWN:
                self.nextScene()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.nextScene()
            elif event.type == pg.QUIT:
                self.sceneManager.exitProgram()

    def draw(self, screen):
        # Dibujamos imagen de fondo
        screen.blit(self.image, self.image.get_rect())

        # Dibujamos título del juego
        font = pg.font.Font(HANSHAND_FONT, 224)
        text = font.render('HECATOMB', True, MAROON)
        text.set_alpha(192)
        textRect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, textRect)

        # Dibujamos mensaje
        font = pg.font.Font(HANSHAND_FONT, 48)
        text = font.render('Pulse cualquier tecla para continuar', True, BLACK)
        textRect = text.get_rect(center=(WIDTH/2, HEIGHT/3*2))
        screen.blit(text, textRect)


    # --------------------------------------
    # Métodos propios de la escena

    def nextScene(self):
        scene = Menu(self.sceneManager)
        self.sceneManager.changeScene(scene)
