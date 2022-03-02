import pygame as pg
from src.settings.settings import *
from src.scenes.scene import *
from pygame.locals import *


class SceneManager():

    def __init__(self):
        # Inicializamos la pantalla y el modo grafico
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # Pila de scenes
        self.stack = []
        # Flag que nos indica cuando quieren salir de la scene
        self.exit_scene = False
        # Reloj
        self.clock = pg.time.Clock()


    def loop(self, scene):

        self.exit_scene = False

        # Eliminamos todos los events producidos antes de entrar en el loop
        pg.event.clear()
        
        # El loop del juego, las acciones que se realicen se harán en cada scene
        while not self.exit_scene:

            # Sincronizar el juego a 60 fps
            elapsed_time = self.clock.tick(FPS) / 1000

            # Pasamos los events a la scene
            scene.events(pg.event.get())

            # Actualiza la scene
            scene.update(elapsed_time)

            # Se dibuja en pantalla
            scene.draw(self.screen)
            pg.display.flip()


    def execute(self):

        # Mientras haya scenes en la stack, executeemos la de arriba
        while (len(self.stack)>0):

            # Se coge la scene a execute como la que este en la cima de la stack
            scene = self.stack[len(self.stack)-1]

            # Ejecutamos el loop de events hasta que termine la scene
            self.loop(scene)


    def exitScene(self):
        # Indicamos en el flag que se quiere salir de la scene
        self.exit_scene = True
        # Eliminamos la scene actual de la stack (si la hay)
        if (len(self.stack)>0):
            self.stack.pop()

    def exitProgram(self):
        # Vaciamos la lista de scenes pendientes
        self.stack = []
        self.exit_scene = True

    def changeScene(self, scene):
        self.exitScene()
        # Ponemos la scene pasada en la cima de la stack
        self.stack.append(scene)

    def stackScene(self, scene):
        self.exit_scene = True
        # Ponemos la scene pasada en la cima de la stack
        #  (por encima de la actual)
        self.stack.append(scene)

