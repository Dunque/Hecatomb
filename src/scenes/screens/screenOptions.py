import pygame as pg
from src.scenes.guiElems import *
from src.scenes.guiUtils import UtilsGUI
from src.settings.settings import *


# TODO: dónde y cómo declarar esta variable?
global difficulty
difficulty = 0


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

class ButtonDifficulty(ButtonGUI):
    def __init__(self, screen):
        self.screen = screen

        assert difficulty in range(3), f"Invalid difficulty value (value = {difficulty})"
        text = "Dificultad: "
        if difficulty == 0:
            text += "Fácil"
        elif difficulty == 1:
            text += "Normal"
        elif difficulty == 2:
            text += "Difícil"

        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, text)

    @staticmethod
    def changeDifficulty():
        global difficulty
        difficulty = (difficulty + 1) % 3
        print(f"new {difficulty = }")   # TODO: borrar

    def changeButtonText(self):
        assert difficulty in range(3), f"Invalid difficulty value (value = {difficulty})"
        text = "Dificultad: "
        if difficulty == 0:
            text += "Fácil"
        elif difficulty == 1:
            text += "Normal"
        elif difficulty == 2:
            text += "Difícil"

        # Se carga el texto del botón
        font = pg.font.Font(HANSHAND_FONT, 42)
        self.text = font.render(text, True, BROWN)
        pos = self.rect.center
        self.textRect = self.text.get_rect(center=pos)
        print(f"new {self.text = }")   # TODO: borrar
        
    def action(self):
        self.changeDifficulty()
        self.changeButtonText()


class ButtonBackOptions(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 1)
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
        buttonDifficulty = ButtonDifficulty(self)
        buttonBack = ButtonBackOptions(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(buttonDifficulty)
        self.elementsGUI.append(buttonBack)
