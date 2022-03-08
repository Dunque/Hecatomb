import pygame as pg
from src.scenes.guiElems import *
from src.scenes.resourceManager import ResourceManager
from src.scenes.scene import Scene
from src.settings.settings import *


# ---------------------------------------------------------
# Botones

class ButtonContinue(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(OTHER_MENU_Y0, PAUSE_MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Continuar')

    def action(self):
        self.screen.menu.continueGame()


class ButtonOptions(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(OTHER_MENU_Y0, PAUSE_MENU_LAYOUT, 1)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Opciones')

    def action(self):
        self.screen.menu.showOptionsScreen()


class ButtonRestart(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(OTHER_MENU_Y0, PAUSE_MENU_LAYOUT, 2)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Reiniciar')

    def action(self):
        self.screen.menu.restartScene()


class ButtonExitToMenu(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(OTHER_MENU_Y0, PAUSE_MENU_LAYOUT, 3)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Salir al menú')

    def action(self):
        self.screen.menu.exitToMenu()


# ---------------------------------------------------------
# Botones

class ButtonBack(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(OTHER_MENU_Y0, OPTIONS_MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Volver')

    def action(self):
        self.screen.menu.showInitialScreen()


# ---------------------------------------------------------
# Textos

class TextPause(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(HANSHAND_FONT, 112)
        pos = (WIDTH/2, HEIGHT/5)
        CenteredTextGUI.__init__(self, screen, font, MAROON, 'Pausa', pos)

    def action(self):
        pass


class TextOptions(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(HANSHAND_FONT, 112)
        pos = (WIDTH/2, HEIGHT/5)
        CenteredTextGUI.__init__(self, screen, font, MAROON, 'Opciones', pos)

    def action(self):
        pass


# ---------------------------------------------------------
# Pantallas

class InitialScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        textTitle = TextPause(self)
        buttonContinue = ButtonContinue(self)
        buttonOptions = ButtonOptions(self)
        buttonRestart = ButtonRestart(self)
        buttonExitToMenu = ButtonExitToMenu(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(buttonContinue)
        self.elementsGUI.append(buttonOptions)
        self.elementsGUI.append(buttonRestart)
        self.elementsGUI.append(buttonExitToMenu)


class OptionsScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        textTitle = TextOptions(self)
        buttonBack = ButtonBack(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(buttonBack)


# ---------------------------------------------------------
# Clase PauseMenu, la escena en sí

class PauseMenu(Scene):

    def __init__(self, sceneManager):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, sceneManager)
        # Creamos la lista de pantallas
        self.screenList = []
        # Creamos las pantallas que vamos a tener y las metemos en la lista
        self.screenList.append(InitialScreenGUI(self))
        self.screenList.append(OptionsScreenGUI(self))
        # En que screen estamos actualmente
        self.showInitialScreen()

    def update(self, *args):
        return

    def events(self, eventList):
        # Se mira la lista de eventos
        for event in eventList:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:    # Tecla Esc, continuar
                    self.continueGame()
            elif event.type == pg.QUIT:
                self.sceneManager.exitProgram()

        # Se pasa la lista de eventos a la pantalla actual
        self.screenList[self.currentScreen].events(eventList)

    def draw(self, screen):
        self.screenList[self.currentScreen].draw(screen)


    # -----------------------------------------------------
    # Métodos propios de la escena

    def showInitialScreen(self):
        self.currentScreen = 0

    def continueGame(self):
        self.sceneManager.exitScene()
    
    def showOptionsScreen(self):
        self.currentScreen = 1
    
    def restartScene(self):
        self.sceneManager.exitScene()
        self.sceneManager.resetTopScene()

    def exitToMenu(self):
        self.sceneManager.exitScene()
        self.sceneManager.exitScene()
