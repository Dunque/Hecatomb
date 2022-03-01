import pygame as pg
from src.scenes.sceneManager import *
from src.scenes.scnIntro import *

from src.scenes.scnMenu import *
from src.scenes.levels.scnLevel1 import *
from src.scenes.levels.scnLevel2 import *
from src.scenes.levels.scnLevel3 import *


if __name__ == '__main__':

    # Inicializamos la libreria de pygame
    pg.init()
    # Creamos el director
    sm = SceneManager()
    # Creamos la escena con la pantalla inicial
    scene = Intro(sm)
    # Le decimos al director que apile esta escena
    sm.stackScene(scene)

    # TODO: ignorar esto, solo para faciliar pruebas (borrar al final)
    if len(sys.argv) > 2:
        print("error: demasiados args")
        exit()
    elif len(sys.argv) == 2:
        sm.changeScene(Menu(sm))
        if sys.argv[1] == '1':
            sm.stackScene(Level1(sm))
        elif sys.argv[1] == '2':
            sm.stackScene(Level2(sm))
        elif sys.argv[1] == '3':
            sm.stackScene(Level3(sm))
        else:
            print("error: posibles valores de arg: {1, 2, 3}")
            exit()

    # Y ejecutamos el juego
    sm.execute()
    # Cuando se termine la ejecución, finaliza la librería
    pg.quit()
