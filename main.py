import pygame
from scenemanager import *
from level1 import *

if __name__ == '__main__':

    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    sm = SceneManager()
    # Creamos la escena con la pantalla inicial
    scene1 = Level1(sm)
    # Le decimos al director que apile esta escena
    sm.stackScene(scene1)
    # Y ejecutamos el juego
    sm.execute()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
