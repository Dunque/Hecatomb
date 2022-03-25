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
    # Ejecutamos el juego
    director.execute()
    # Cuando se termine la ejecución, finaliza la librería
    pg.quit()
