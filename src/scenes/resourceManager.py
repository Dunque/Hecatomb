import pygame, os
from pygame.locals import *


# -------------------------------------------------
# Clase ResourceManager

# En este caso se implementa como una clase vacía, solo con métodos de clase
class ResourceManager(object):
    resources = {}

    @classmethod
    def LoadImage(cls, name, colorKey=None):
        # Si el name de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la image indicando la carpeta en la que está
            # fullName = os.path.join('imagenes', name)
            fullName = os.path.join(name)
            try:
                image = pygame.image.load(fullName)
            except pygame.error as message:
                print ('Cannot load image:', fullName)
                raise (SystemExit, message)
            image = image.convert()
            if colorKey is not None:
                if colorKey is -1:
                    colorKey = image.get_at((0,0))
                image.set_colorkey(colorKey, RLEACCEL)
            # Se almacena
            cls.resources[name] = image
            # Se devuelve
            return image

    @classmethod
    def LoadFileCoordinates(cls, name):
        # Si el name de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            # fullName = os.path.join('imagenes', name)
            fullName = os.path.join(name)
            pfile=open(fullName,'r')
            data=pfile.read()
            pfile.close()
            # Se almacena
            cls.resources[name] = data
            # Se devuelve
            return data
