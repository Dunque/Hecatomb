import pygame as pg
from src.scenes.resourceManager import ResourceManager
from src.scenes.scene import Scene
from src.settings.settings import *


# ---------------------------------------------------------
# Clase abstracta ElementGUI

class ElementGUI:
    def __init__(self, screen, rectangle):
        self.screen = screen
        self.rect = rectangle

    def setPosition(self, position):
        (positionx, positiony) = position
        self.rect.left = positionx
        self.rect.bottom = positiony
    
    def setCenterPosition(self, position):
        self.rect.center = position

    def positionInElement(self, position):
        (positionx, positiony) = position
        if ((positionx>=self.rect.left) and (positionx<=self.rect.right) 
            and (positiony>=self.rect.top) and (positiony<=self.rect.bottom)):
            return True
        else:
            return False

    def draw(self):
        raise NotImplemented("Tiene que implementar el metodo draw.")

    def action(self):
        raise NotImplemented("Tiene que implementar el metodo action.")


# ---------------------------------------------------------
# Clase ButtonGUI

class ButtonGUI(ElementGUI):
    def __init__(self, screen, imageName, size, position, text):
        # Se carga la imagen del botón
        self.image = ResourceManager.LoadImage(imageName, -1)
        self.image = pg.transform.scale(self.image, size)

        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        ElementGUI.__init__(self, screen, self.image.get_rect())

        # Se coloca el rectángulo en su posición
        self.setCenterPosition(position)

        # Se carga el texto del botón
        font = pg.font.Font(HANSHAND_FONT, 42)
        self.text = font.render(text, True, BROWN)
        self.textRect = self.text.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)

    @staticmethod
    def calculatePosition(y0, menuSize, n):
        """Calcula la posición del centro del rectángulo que ocupa el n-ésimo botón 
        (n = 0, 1, 2...) en un menú de tamaño menuSize, empezando en la altura y0"""

        (cols, rows) = menuSize
        assert (n+1 <= cols*rows), f"There are more buttons than positions ({cols*rows} positions)"

        dx = BUTTON_WIDTH + BUTTON_SEP_X
        dy = BUTTON_HEIGHT + BUTTON_SEP_Y
        x0 = WIDTH/2 - (cols-1)*dx/2
        col = n // rows
        row = n % rows

        return (x0 + col*dx, y0 + row*dy)


# ---------------------------------------------------------
# Clase TextGUI y CenteredTextGUI

class TextGUI(ElementGUI):
    def __init__(self, screen, font, color, text, position):
        # Se crea la imagen del texto
        self.image = font.render(text, True, color)
        # Se llama al método de la clase padre con el rectángulo que ocupa el texto
        ElementGUI.__init__(self, screen, self.image.get_rect())
        # Se coloca el rectángulo en su posición
        self.setPosition(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class CenteredTextGUI(ElementGUI):
    def __init__(self, screen, font, color, text, position, alpha=255):
        # Se crea la imagen del texto
        self.image = font.render(text, True, color)
        self.image.set_alpha(alpha)
        # Se llama al método de la clase padre con el rectángulo que ocupa el texto
        ElementGUI.__init__(self, screen, self.image.get_rect())
        # Se coloca el rectángulo en su posición
        self.setCenterPosition(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# ---------------------------------------------------------
# Clase ScreenGUI

class ScreenGUI:
    def __init__(self, menu, imageName):
        self.menu = menu
        # Se carga la imagen de fondo
        self.image = ResourceManager.LoadImage(imageName)
        self.image = pg.transform.scale(self.image, (WIDTH, HEIGHT))
        # Se tiene una lista de elementos GUI
        self.elementsGUI = []

    def events(self, eventList):
        for event in eventList:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.elementClick = None
                for element in self.elementsGUI:
                    if element.positionInElement(event.pos):
                        self.elementClick = element
            if event.type == pg.MOUSEBUTTONUP:
                for element in self.elementsGUI:
                    if element.positionInElement(event.pos):
                        if (element == self.elementClick):
                            element.action()

    def draw(self, screen):
        # Dibujamos primero la imagen de fondo
        screen.blit(self.image, self.image.get_rect())
        # Después los botones
        for element in self.elementsGUI:
            element.draw(screen)
