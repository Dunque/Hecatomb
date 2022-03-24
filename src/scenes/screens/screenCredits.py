import pygame as pg
from src.scenes.guiElems import *
from src.scenes.guiUtils import UtilsGUI
from src.settings.settings import *


# ---------------------------------------------------------
# Textos

class TextCredits(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(GUI_FONT, 112)
        pos = (WIDTH/2, HEIGHT/5)
        CenteredTextGUI.__init__(self, screen, font, MAROON, 'Créditos', pos)

    def action(self):
        pass

class TextAuthor(CenteredTextGUI):
    def __init__(self, screen, n, name):
        font = pg.font.Font(GUI_FONT, 50)
        pos = (WIDTH/2, OTHER_MENU_Y0 + n*80)
        CenteredTextGUI.__init__(self, screen, font, WHITE, name, pos)

    def action(self):
        pass

# ---------------------------------------------------------
# Botones

class ButtonBackCredits(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, 0, CREDITS_MENU_LAYOUT, 5)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Volver')

    def action(self):
        self.screen.menu.showInitialScreen()

# ---------------------------------------------------------
# Pantalla

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
