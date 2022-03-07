import pygame as pg
from src.scenes.cutscenes.scnCutscene1 import Cutscene1
from src.scenes.guiElems import *
from src.scenes.resourceManager import ResourceManager
from src.scenes.scene import Scene
from src.scenes.survival.scnSurvival import Survival
from src.settings.settings import *


# ---------------------------------------------------------
# Botones

class ButtonAdventure(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(MAIN_MENU_Y0, MAIN_MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Aventura')

    def action(self):
        self.screen.menu.playAdventure()


class ButtonSurvival(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(MAIN_MENU_Y0, MAIN_MENU_LAYOUT, 1)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Supervivencia')

    def action(self):
        self.screen.menu.playSurvival()


class ButtonRecords(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(MAIN_MENU_Y0, MAIN_MENU_LAYOUT, 2)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Récords')

    def action(self):
        self.screen.menu.showRecordsScreen()


class ButtonOptions(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(MAIN_MENU_Y0, MAIN_MENU_LAYOUT, 3)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Opciones')

    def action(self):
        self.screen.menu.showOptionsScreen()


class ButtonCredits(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(MAIN_MENU_Y0, MAIN_MENU_LAYOUT, 4)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Créditos')

    def action(self):
        self.screen.menu.showCreditsScreen()


class ButtonExit(ButtonGUI):
    def __init__(self, screen):
        pos = ButtonGUI.calculatePosition(MAIN_MENU_Y0, MAIN_MENU_LAYOUT, 5)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Salir')

    def action(self):
        self.screen.menu.exitProgram()


# ---------------------------------------------------------
# Textos

class TextHecatomb(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(HANSHAND_FONT, 160)
        pos = (WIDTH/2, HEIGHT*3/10)
        CenteredTextGUI.__init__(self, screen, font, MAROON, 'HECATOMB', pos, 192)

    def action(self):
        pass


# ---------------------------------------------------------
# Pantallas

class InitialScreenGUI(ScreenGUI):
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
        self.screenList.append(InitialScreenGUI(self))
        self.screenList.append(RecordsScreenGUI(self))
        self.screenList.append(OptionsScreenGUI(self))
        self.screenList.append(CreditsScreenGUI(self))
        # En que screen estamos actualmente
        self.showInitialScreen()

    def update(self, *args):
        return

    def events(self, eventList):
        # Se mira la lista de eventos
        for event in eventList:
            if event.type == pg.QUIT:
                self.sceneManager.exitProgram()

        # Se pasa la lista de eventos a la pantalla actual
        self.screenList[self.currentScreen].events(eventList)

    def draw(self, screen):
        self.screenList[self.currentScreen].draw(screen)


    # -----------------------------------------------------
    # Métodos propios de la escena

    def showInitialScreen(self):
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
