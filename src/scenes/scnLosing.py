import pygame as pg
from src.scenes.guiElems import *
from src.scenes.guiUtils import UtilsGUI
from src.scenes.scene import Scene
from src.settings.settings import *


# ---------------------------------------------------------
# Botones

class ButtonRestart(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, LOSING_MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Reiniciar')

    def action(self):
        self.screen.menu.restartScene()


class ButtonExitToMenu(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, LOSING_MENU_LAYOUT, 1)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Salir al menú')

    def action(self):
        self.screen.menu.exitToMenu()


# ---------------------------------------------------------
# Textos

class TextLosing(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(GUI_FONT, 112)
        pos = (WIDTH/2, HEIGHT/5)
        CenteredTextGUI.__init__(self, screen, font, MAROON, '¡Has muerto!', pos)

    def action(self):
        pass


# ---------------------------------------------------------
# Pantallas

class InitialScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        textTitle = TextLosing(self)
        buttonRestart = ButtonRestart(self)
        buttonExitToMenu = ButtonExitToMenu(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(buttonRestart)
        self.elementsGUI.append(buttonExitToMenu)


# ---------------------------------------------------------
# Clase LosingMenu, la escena en sí

class LosingMenu(Scene):

    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, director)
        # Creamos la lista de pantallas
        self.screenList = []
        # Creamos las pantallas que vamos a tener y las metemos en la lista
        self.screenList.append(InitialScreenGUI(self))
        # En que screen estamos actualmente
        self.showInitialScreen()

    def update(self, *args):
        return

    def events(self, eventList):
        # Se mira la lista de eventos
        for event in eventList:
            if event.type == pg.QUIT:
                self.director.exitProgram()

        # Se pasa la lista de eventos a la pantalla actual
        self.screenList[self.currentScreen].events(eventList)

    def draw(self, screen):
        self.screenList[self.currentScreen].draw(screen)


    # -----------------------------------------------------
    # Scene transitions

    def showInitialScreen(self):
        self.currentScreen = 0
    
    def restartScene(self):
        self.director.exitScene()
        self.director.resetTopScene()

    def exitToMenu(self):
        self.director.exitScene()
        self.director.exitScene()
