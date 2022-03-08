import pygame as pg
from src.scenes.sceneManager import SceneManager
from src.scenes.scnIntro import Intro


if __name__ == '__main__':

    # Inicializamos la librería de pygame
    pg.init()
    # Creamos el director
    sm = SceneManager()
    # Creamos la escena con la pantalla inicial
    scene = Intro(sm)
    # Le decimos al director que apile esta escena
    sm.stackScene(scene)

    #--------------------------------------------------------------------------
    # TODO: ignorar esto, solo para faciliar pruebas (borrar al final)
    
    import sys
    from src.scenes.scnMenu import Menu
    from src.scenes.levels.scnLevel1 import Level1
    from src.scenes.levels.scnLevel2 import Level2
    from src.scenes.levels.scnLevel3 import Level3

    if len(sys.argv) > 2:
        sys.exit("error: demasiados args")
    elif len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 2:
        sm.changeScene(Menu(sm))
        if sys.argv[1] == '0':
            pass
        elif sys.argv[1] == '1':
            sm.stackScene(Level1(sm))
        elif sys.argv[1] == '2':
            sm.stackScene(Level2(sm))
        elif sys.argv[1] == '3':
            sm.stackScene(Level3(sm))
        else:
            sys.exit("error: posibles valores de arg: {0, 1, 2, 3}")
    #--------------------------------------------------------------------------

    # Ejecutamos el juego
    sm.execute()
    # Cuando se termine la ejecución, finaliza la librería
    pg.quit()
