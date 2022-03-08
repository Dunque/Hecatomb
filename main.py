import pygame as pg
from src.scenes.director import Director
from src.scenes.scnIntro import Intro


if __name__ == '__main__':

    # Inicializamos la librería de pygame
    pg.init()
    # Creamos el director
    director = Director()
    # Creamos la escena con la pantalla inicial
    scene = Intro(director)
    # Le decimos al director que apile esta escena
    director.stackScene(scene)

    #--------------------------------------------------------------------------
    # TODO: ignorar esto, solo para faciliar pruebas (borrar al final)
    
    import sys
    from src.scenes.scnMenu import Menu
    from src.scenes.levels.scnLevel1 import Level1
    from src.scenes.levels.scnLevel2 import Level2
    from src.scenes.levels.scnLevel3 import Level3
    from src.scenes.cutscenes.scnCutscene1 import Cutscene1
    from src.scenes.scnPause import PauseMenu

    if len(sys.argv) > 2:
        sys.exit("error: demasiados args")
    elif len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 2:
        director.changeScene(Menu(director))
        
        if sys.argv[1] == 'menu':
            pass
        elif sys.argv[1] == 'l1':
            director.stackScene(Level1(director))
        elif sys.argv[1] == 'l2':
            director.stackScene(Level2(director))
        elif sys.argv[1] == 'l3':
            director.stackScene(Level3(director))
        elif sys.argv[1] == 'pause':
            director.stackScene(Cutscene1(director))
            director.stackScene(PauseMenu(director))

        else:
            sys.exit("error: posibles valores de arg: {menu, l1, l2, l3, pause}")
    #--------------------------------------------------------------------------

    # Ejecutamos el juego
    director.execute()
    # Cuando se termine la ejecución, finaliza la librería
    pg.quit()
