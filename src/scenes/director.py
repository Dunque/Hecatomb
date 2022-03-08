import pygame as pg
from src.settings.settings import *
from src.scenes.scene import *
from pygame.locals import *


class Director():

    def __init__(self):
        # Inicializamos la pantalla y el modo gráfico
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # Pila de escenas
        self.stack = []
        # Flag que nos indica cuando quieren salir de la escena
        self.exit_scene = False
        # Reloj
        self.clock = pg.time.Clock()


    def loop(self, scene):

        self.exit_scene = False

        # Eliminamos todos los eventos producidos antes de entrar en el bucle
        pg.event.clear()
        
        # El bucle del juego, las acciones que se realicen se harán en cada escena
        while not self.exit_scene:

            # Sincronizar el juego a 60 fps
            elapsed_time = self.clock.tick(FPS) / 1000

            # Pasamos los eventos a la escena
            scene.events(pg.event.get())

            # Actualiza la escena
            scene.update(elapsed_time)

            # Se dibuja en pantalla
            scene.draw(self.screen)
            pg.display.flip()


    def execute(self):

        # Mientras haya escenas en la pila, ejecutaremos la de arriba
        while (len(self.stack)>0):

            # Se coge la escena a ejecutar como la que esté en la cima de la pila
            scene = self.stack[len(self.stack)-1]

            # Ejecutamos el bucle de eventos hasta que termine la escena
            self.loop(scene)


    def exitScene(self):
        # Indicamos en el flag que se quiere salir de la escena
        self.exit_scene = True
        # Eliminamos la escena actual de la pila (si la hay)
        if (len(self.stack)>0):
            self.stack.pop()

    def exitProgram(self):
        # Vaciamos la lista de escenas pendientes
        self.stack = []
        self.exit_scene = True

    def changeScene(self, scene):
        self.exitScene()
        # Ponemos la escena pasada en la cima de la pila
        self.stack.append(scene)

    def stackScene(self, scene):
        self.exit_scene = True
        # Ponemos la escena pasada en la cima de la pila (por encima de la actual)
        self.stack.append(scene)

    def resetTopScene(self):
        # Cogemos la escena que esté en la cima de la pila
        scene = self.stack[-1]
        # Reiniciamos la escena
        scene.reset()
