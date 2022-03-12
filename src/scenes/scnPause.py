import pygame as pg
from src.scenes.guiElems import *
from src.scenes.guiUtils import UtilsGUI
from src.scenes.scene import Scene
from src.settings.settings import *
from src.scenes.music import *

# ---------------------------------------------------------
# Botones

class ButtonContinue(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, PAUSE_MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Continuar')

    def action(self):
        Music.volumemusic(self, 1)
        self.screen.menu.continueGame()


class ButtonOptions(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, PAUSE_MENU_LAYOUT, 1)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Opciones')

    def action(self):
        self.screen.menu.showOptionsScreen()


class ButtonRestart(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, PAUSE_MENU_LAYOUT, 2)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Reiniciar')

    def action(self):
        Music.volumemusic(self,1)
        Music.effectsvolume(self,0.25)
        self.screen.menu.restartScene()


class ButtonExitToMenu(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, PAUSE_MENU_LAYOUT, 3)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Salir al menú')

    def action(self):
        Music.changemusic(self, 0)
        self.screen.menu.exitToMenu()


# ---------------------------------------------------------
# Botones

class ButtonBack(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 0)
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


# ---------------------------------------------------------
# Textos

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


# ---------------------------------------------------------
# Pantallas

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

    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, director)
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
                self.director.exitProgram()

        # Se pasa la lista de eventos a la pantalla actual
        self.screenList[self.currentScreen].events(eventList)

    def draw(self, screen):
        self.screenList[self.currentScreen].draw(screen)


    # -----------------------------------------------------
    # Scene transitions

    def showInitialScreen(self):
        self.currentScreen = 0

    def continueGame(self):
        self.director.exitScene()
    
    def showOptionsScreen(self):
        self.currentScreen = 1
    
    def restartScene(self):
        self.director.exitScene()
        self.director.resetTopScene()

    def exitToMenu(self):
        self.director.exitScene()
        self.director.exitScene()
