import random
import pygame as pg
from src.scenes.cutscenes.scnCutscene1 import Cutscene1
from src.scenes.guiElems import *
from src.scenes.guiUtils import UtilsGUI
from src.scenes.music import *
from src.scenes.scene import Scene
from src.scenes.screens.screenCredits import CreditsScreenGUI
from src.scenes.screens.screenOptions import OptionsScreenGUI
from src.scenes.screens.screenRecords import RecordsScreenGUI
from src.scenes.survival.scnSurvival import Survival
from src.settings.settings import *


# ---------------------------------------------------------
# Elementos de la pantalla inicial
CLICK_SOUND = pg.mixer.Sound("./sounds/beep.wav")
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
        CLICK_SOUND.play()
        self.screen.menu.playAdventure()


class ButtonSurvival(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 1)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Supervivencia')

    def action(self):
        CLICK_SOUND.play()
        self.screen.menu.playSurvival()


class ButtonRecords(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 2)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Récords')

    def action(self):
        CLICK_SOUND.play()
        self.screen.menu.showRecordsScreen()


class ButtonOptions(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 3)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Opciones')

    def action(self):
        CLICK_SOUND.play()
        self.screen.menu.showOptionsScreen()


class ButtonCredits(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 4)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Créditos')

    def action(self):
        CLICK_SOUND.play()
        self.screen.menu.showCreditsScreen()


class ButtonExit(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 5)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Salir')

    def action(self):
        CLICK_SOUND.play()
        self.screen.menu.exitProgram()


# ---------------------------------------------------------
# Pantalla inicial

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
    # Transiciones de pantalla/escena

    def showInitialScreen(self):
        self.currentScreen = 0

    def playAdventure(self):
        scene = Cutscene1(self.director)
        Music.changemusic(self, 0)
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
