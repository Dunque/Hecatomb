import pygame as pg
from src.scenes.recordManager import getRecord
from src.scenes.guiElems import *
from src.scenes.guiUtils import UtilsGUI
from src.settings.settings import *


# ---------------------------------------------------------
# Textos

class TextRecords(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(GUI_FONT, 112)
        pos = (WIDTH/2, HEIGHT/5)
        CenteredTextGUI.__init__(self, screen, font, MAROON, 'Récords', pos)

    def action(self):
        pass

class TextBestScores(CenteredTextGUI):
    def __init__(self, screen):
        font = pg.font.Font(GUI_FONT, 50)
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, 0, RECORDS_MENU_LAYOUT, 0)
        CenteredTextGUI.__init__(self, screen, font, WHITE, 'Mejores puntuaciones:', pos)

    def action(self):
        pass


# ---------------------------------------------------------
# Botones

class Board1(ButtonGUI):
    def __init__(self, screen):
        scoreText = getRecord(1)
        # pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0 + 50, 0, RECORDS_MENU_LAYOUT, 3)
        pos = (1000, 350)
        ButtonGUI.__init__(self, screen, 'resources/images/button_yellow.png', (600, 160), pos, scoreText)

    def changeButtonText(self):
        # Se vuelve a cargar el texto
        scoreText = getRecord(1)
        font = pg.font.Font(GUI_FONT, 42)
        self.text = font.render(scoreText, True, BROWN)
        pos = self.rect.center
        self.textRect = self.text.get_rect(center=pos)

    def action(self):
        # self.changeButtonText()    # TODO: sacar de aquí esto
        pass

class Board2(ButtonGUI):
    def __init__(self, screen):
        scoreText = getRecord(2)
        # pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0 + 50, 0, RECORDS_MENU_LAYOUT, 4)
        pos = (1000, 550)
        ButtonGUI.__init__(self, screen, 'resources/images/button_blue.png', (600, 160), pos, scoreText)

    def changeButtonText(self):
        # Se vuelve a cargar el texto
        scoreText = getRecord(2)
        font = pg.font.Font(GUI_FONT, 42)
        self.text = font.render(scoreText, True, BROWN)
        pos = self.rect.center
        self.textRect = self.text.get_rect(center=pos)

    def action(self):
        # self.changeButtonText()    # TODO: sacar de aquí esto
        pass

class Board3(ButtonGUI):
    def __init__(self, screen):
        scoreText = getRecord(3)
        # pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0 + 50, 0, RECORDS_MENU_LAYOUT, 5)
        pos = (1000, 750)
        ButtonGUI.__init__(self, screen, 'resources/images/button_red.png', (600, 160), pos, scoreText)

    def changeButtonText(self):
        # Se vuelve a cargar el texto
        scoreText = getRecord(3)
        font = pg.font.Font(GUI_FONT, 42)
        self.text = font.render(scoreText, True, BROWN)
        pos = self.rect.center
        self.textRect = self.text.get_rect(center=pos)

    def action(self):
        # self.changeButtonText()    # TODO: sacar de aquí esto
        pass


class ButtonBackRecords(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(OTHER_MENU_Y0, BUTTON_SEP_Y, RECORDS_MENU_LAYOUT, 1)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Volver')

    def action(self):
        # recordManager.updateRecords(10)   # TODO: borrar, debug
        self.screen.menu.showInitialScreen()

# ---------------------------------------------------------
# Pantalla

class RecordsScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        textTitle = TextRecords(self)
        textBestScores = TextBestScores(self)
        boardRecord1 = Board1(self)
        boardRecord2 = Board2(self)
        boardRecord3 = Board3(self)
        buttonBack = ButtonBackRecords(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(textBestScores)
        self.elementsGUI.append(boardRecord1)
        self.elementsGUI.append(boardRecord2)
        self.elementsGUI.append(boardRecord3)
        self.elementsGUI.append(buttonBack)
