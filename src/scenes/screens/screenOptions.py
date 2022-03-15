import pygame as pg
from src.scenes.guiElems import *
from src.scenes.guiUtils import UtilsGUI
from src.settings.settings import *


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
# Botones

class ButtonBackOptions(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Volver')

    def action(self):
        self.screen.menu.showInitialScreen()

# ---------------------------------------------------------
# Pantalla

class OptionsScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        textTitle = TextOptions(self)
        buttonBack = ButtonBackOptions(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(buttonBack)
