import pygame as pg
from sceneManager import *
from scnIntro import *

if __name__ == '__main__':

    # Inicializamos la libreria de pygame
    pg.init()
    # Creamos el director
    sm = SceneManager()
    # Creamos la escena con la pantalla inicial
    scene = Intro(sm)
    # Le decimos al director que apile esta escena
    sm.stackScene(scene)
    # Y ejecutamos el juego
    sm.execute()
    # Cuando se termine la ejecución, finaliza la librería
    pg.quit()
