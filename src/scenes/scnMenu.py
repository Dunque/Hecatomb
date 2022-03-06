import pygame as pg
from src.scenes.cutscenes.scnCutscene1 import Cutscene1
from src.scenes.resourceManager import ResourceManager
from src.scenes.scene import Scene
from src.scenes.survival.scnSurvival import Survival
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
# Clase ButtonGUI y los distintos botones

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


class ButtonAdventure(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(TOP_MARGIN, MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Aventura')

    def action(self):
        self.screen.menu.playAdventure()


class ButtonSurvival(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(TOP_MARGIN, MENU_LAYOUT, 1)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Supervivencia')

    def action(self):
        self.screen.menu.playSurvival()


class ButtonRecords(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(TOP_MARGIN, MENU_LAYOUT, 2)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Récords')

    def action(self):
        self.screen.menu.showRecordsScreen()


class ButtonOptions(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(TOP_MARGIN, MENU_LAYOUT, 3)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Opciones')

    def action(self):
        self.screen.menu.showOptionsScreen()


class ButtonCredits(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(TOP_MARGIN, MENU_LAYOUT, 4)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Créditos')

    def action(self):
        self.screen.menu.showCreditsScreen()


class ButtonExit(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(TOP_MARGIN, MENU_LAYOUT, 5)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Salir')

    def action(self):
        self.screen.menu.exitProgram()


# -------------------------------------------------
# Clase TextGUI y los distintos textos

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


class TextHecatomb(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(HANSHAND_FONT, 160)
        pos = (WIDTH/2, HEIGHT*3/10)
        CenteredTextGUI.__init__(self, screen, font, MAROON, 'HECATOMB', pos, 192)

    def action(self):
        pass


# ---------------------------------------------------------
# Clase ScreenGUI y las distintas pantallas

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


class MenuScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu.png')
        # Creamos los elementos GUI
        textTitle = TextHecatomb(self)
        buttonAdventure = ButtonAdventure(self)
        buttonSurvival = ButtonSurvival(self)
        buttonRecords = ButtonRecords(self)
        buttonOptions = ButtonOptions(self)
        buttonCredits = ButtonCredits(self)
        buttonExit = ButtonExit(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(buttonAdventure)
        self.elementsGUI.append(buttonSurvival)
        self.elementsGUI.append(buttonRecords)
        self.elementsGUI.append(buttonOptions)
        self.elementsGUI.append(buttonCredits)
        self.elementsGUI.append(buttonExit)


class RecordsScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        pass
        # Y los metemos en la lista
        pass


class OptionsScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        pass
        # Y los metemos en la lista
        pass


class CreditsScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        pass
        # Y los metemos en la lista
        pass


# ---------------------------------------------------------
# Clase Menu, la escena en sí

class Menu(Scene):

    def __init__(self, sceneManager):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, sceneManager)
        # Creamos la lista de pantallas
        self.screenList = []
        # Creamos las pantallas que vamos a tener y las metemos en la lista
        self.screenList.append(MenuScreenGUI(self))
        self.screenList.append(RecordsScreenGUI(self))
        self.screenList.append(OptionsScreenGUI(self))
        self.screenList.append(CreditsScreenGUI(self))
        # En que screen estamos actualmente
        self.showMenuScreen()

    def update(self, *args):
        return

    def events(self, eventList):
        # Se mira la lista de eventos
        for event in eventList:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.exitProgram()
            elif event.type == pg.QUIT:
                self.sceneManager.exitProgram()

        # Se pasa la lista de eventos a la pantalla actual
        self.screenList[self.currentScreen].events(eventList)

    def draw(self, screen):
        self.screenList[self.currentScreen].draw(screen)


    # -----------------------------------------------------
    # Métodos propios del menú

    def showMenuScreen(self):
        self.currentScreen = 0

    def playAdventure(self):
        scene = Cutscene1(self.sceneManager)
        self.sceneManager.stackScene(scene)

    def playSurvival(self):
        scene = Survival(self.sceneManager)
        self.sceneManager.stackScene(scene)

    def showRecordsScreen(self):
        self.currentScreen = 1
    
    def showOptionsScreen(self):
        self.currentScreen = 2

    def showCreditsScreen(self):
        self.currentScreen = 3

    def exitProgram(self):
        self.sceneManager.exitProgram()
