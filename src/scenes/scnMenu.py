import pygame as pg
import random
from src.scenes.cutscenes.scnCutscene1 import Cutscene1
from src.scenes.guiElems import *
from src.scenes.guiUtils import UtilsGUI
from src.scenes.scene import Scene
from src.scenes.survival.scnSurvival import Survival
from src.settings.settings import *
from src.scenes.music import *

# ---------------------------------------------------------
# Elementos de pantalla Menu

class TextHecatomb(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(HANSHAND_FONT, 160)
        pos = (WIDTH/2, HEIGHT*3/10)
        CenteredTextGUI.__init__(self, screen, font, MAROON, 'HECATOMB', pos)

    def action(self):
        pass


class ButtonAdventure(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Aventura')

    def action(self):
        self.screen.menu.playAdventure()


class ButtonSurvival(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 1)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Supervivencia')

    def action(self):
        self.screen.menu.playSurvival()


class ButtonRecords(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 2)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Récords')

    def action(self):
        self.screen.menu.showRecordsScreen()


class ButtonOptions(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 3)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Opciones')

    def action(self):
        self.screen.menu.showOptionsScreen()


class ButtonCredits(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 4)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Créditos')

    def action(self):
        self.screen.menu.showCreditsScreen()


class ButtonExit(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 5)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Salir')

    def action(self):
        self.screen.menu.exitProgram()


                 # ---------------------------------------------------------
# Elementos de pantalla Records

class TextRecords(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(HANSHAND_FONT, 112)
        pos = (WIDTH/2, HEIGHT/5)
        CenteredTextGUI.__init__(self, screen, font, MAROON, 'Récords', pos)

    def action(self):
        pass


class ButtonBackRecords(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, RECORDS_MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Volver')

    def action(self):
        self.screen.menu.showInitialScreen()


# ---------------------------------------------------------
# Elementos de pantalla Options

class TextOptions(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(HANSHAND_FONT, 112)
        pos = (WIDTH/2, HEIGHT/5)
        CenteredTextGUI.__init__(self, screen, font, MAROON, 'Opciones', pos)

    def action(self):
        pass


class ButtonBackOptions(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Volver')

    def action(self):
        self.screen.menu.showInitialScreen()


# ---------------------------------------------------------
# Elementos de pantalla Credits

class TextCredits(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(HANSHAND_FONT, 112)
        pos = (WIDTH/2, HEIGHT/5)
        CenteredTextGUI.__init__(self, screen, font, MAROON, 'Créditos', pos)

    def action(self):
        pass

class TextAuthor(CenteredTextGUI):
    def __init__(self, screen, n, name):
        font = pg.font.Font(HANSHAND_FONT, 50)
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, 0, CREDITS_MENU_LAYOUT, n)
        CenteredTextGUI.__init__(self, screen, font, WHITE, name, pos)

    def action(self):
        pass


class ButtonBackCredits(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, 0, CREDITS_MENU_LAYOUT, 5)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Volver')

    def action(self):
        self.screen.menu.showInitialScreen()


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
        textTitle = TextRecords(self)
        buttonBack = ButtonBackRecords(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(buttonBack)


class OptionsScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        textTitle = TextOptions(self)
        buttonBack = ButtonBackOptions(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(buttonBack)


class CreditsScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        textTitle = TextCredits(self)
        textAuthor0 = TextAuthor(self, 0, 'Roi Santos Ríos')
        textAuthor1 = TextAuthor(self, 1, 'Antón Concheiro Fernández')
        textAuthor2 = TextAuthor(self, 2, 'Iago Fernández Garrido')
        textAuthor3 = TextAuthor(self, 3, 'Jorge Rivadulla Brey')
        textAuthor4 = TextAuthor(self, 4, 'Xes Garbajosa Fernández')
        buttonBack = ButtonBackCredits(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(textAuthor0)
        self.elementsGUI.append(textAuthor1)
        self.elementsGUI.append(textAuthor2)
        self.elementsGUI.append(textAuthor3)
        self.elementsGUI.append(textAuthor4)
        self.elementsGUI.append(buttonBack)


# ---------------------------------------------------------
# Clase Menu, la escena en sí

class Menu(Scene):

    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, director)
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
                self.director.exitProgram()

        # Se pasa la lista de eventos a la pantalla actual
        self.screenList[self.currentScreen].events(eventList)

    def draw(self, screen):
        self.screenList[self.currentScreen].draw(screen)


    # -----------------------------------------------------
    # Métodos propios de la escena

    def showInitialScreen(self):
        self.currentScreen = 0

    def playAdventure(self):
        scene = Cutscene1(self.director)
        self.director.stackScene(scene)

    def playSurvival(self):
        m = random.randint(1, 5)
        Music.changemusic(self,m)
        scene = Survival(self.director)
        self.director.stackScene(scene)

    def showRecordsScreen(self):
        self.currentScreen = 1
    
    def showOptionsScreen(self):
        self.currentScreen = 2

    def showCreditsScreen(self):
        self.currentScreen = 3

    def exitProgram(self):
        self.director.exitProgram()
