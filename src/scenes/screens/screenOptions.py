import sys
import pygame as pg
from src.scenes.music import Music
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

class TextMusicVolume(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(HANSHAND_FONT, 42)
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 4)
        CenteredTextGUI.__init__(self, screen, font, WHITE, 'Volumen música', pos)

    def action(self):
        pass

class TextSoundVolume(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(HANSHAND_FONT, 42)
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 5)
        CenteredTextGUI.__init__(self, screen, font, WHITE, 'Volumen sonidos', pos)

    def action(self):
        pass

# ---------------------------------------------------------
# Botones

class ButtonMusicDown(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 0)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, '-')

    def action(self):
        print(f"Music volume DOWN")


class ButtonMusicUp(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 8)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, '+')

    def action(self):
        print(f"Music volume UP")


class ButtonSoundDown(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 1)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, '-')

    def action(self):
        print(f"Sound volume DOWN")


class ButtonSoundUp(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 9)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, '+')

    def action(self):
        print(f"Sound volume UP")


class ButtonDifficulty(ButtonGUI):
    difficulty = 1

    def __init__(self, screen):
        text = self.getText()
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 6)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, text)

    def getText(self):
        text = "Dificultad: "
        if ButtonDifficulty.difficulty == 0:
            text += "Fácil"
        elif ButtonDifficulty.difficulty == 1:
            text += "Normal"
        elif ButtonDifficulty.difficulty == 2:
            text += "Difícil"
        else:
            sys.exit("Invalid difficulty value")
        return text

    def changeDifficulty(self):
        ButtonDifficulty.difficulty = (ButtonDifficulty.difficulty + 1) % 3

    def changeButtonText(self):
        # Se vuelve a cargar el texto del botón
        text = self.getText()
        font = pg.font.Font(HANSHAND_FONT, 42)
        self.text = font.render(text, True, BROWN)
        pos = self.rect.center
        self.textRect = self.text.get_rect(center=pos)

    def action(self):
        self.changeDifficulty()
        self.changeButtonText()


class ButtonBackOptions(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, OPTIONS_MENU_LAYOUT, 7)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Volver')

    def action(self):
        Music.volumemusic(self, 1)
        self.screen.menu.showInitialScreen()

# ---------------------------------------------------------
# Pantalla

class OptionsScreenGUI(ScreenGUI):
    _instance = None

    def __new__(cls, menu):
        # Si la instancia no existe, creamos la instancia
        if cls._instance is None:
            cls._instance = super(OptionsScreenGUI, cls).__new__(cls)
        # Devolvemos la instancia
        return cls._instance

    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        textTitle = TextOptions(self)
        textMusicVolume = TextMusicVolume(self)
        buttonMusicDown = ButtonMusicDown(self)
        buttonMusicUp = ButtonMusicUp(self)
        textSoundVolume = TextSoundVolume(self)
        buttonSoundDown = ButtonSoundDown(self)
        buttonSoundUp = ButtonSoundUp(self)
        buttonDifficulty = ButtonDifficulty(self)
        buttonBack = ButtonBackOptions(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(textMusicVolume)
        self.elementsGUI.append(buttonMusicDown)
        self.elementsGUI.append(buttonMusicUp)
        self.elementsGUI.append(textSoundVolume)
        self.elementsGUI.append(buttonSoundDown)
        self.elementsGUI.append(buttonSoundUp)
        self.elementsGUI.append(buttonDifficulty)
        self.elementsGUI.append(buttonBack)
