import pygame as pg
from src.scenes.recordManager import RecordManager
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
        pos = (WIDTH*3/4, 300)
        CenteredTextGUI.__init__(self, screen, font, WHITE, 'Mejores puntuaciones', pos)

    def action(self):
        pass


# ---------------------------------------------------------
# Botones

class BoardWithScore(ButtonGUI):
    def __init__(self, screen, n):
        self.n = n
        image = self.getBoardImage()
        pos = (WIDTH*3/4, 420 + (n-1)*160)
        scoreText = str(RecordManager.getRecord(self.n))
        ButtonGUI.__init__(self, screen, image, (500, 130), pos, scoreText)
    
    def getBoardImage(self):
        if self.n == 1:
            return 'resources/images/button_yellow.png'
        elif self.n == 2:
            return 'resources/images/button_blue.png'
        elif self.n == 3:
            return 'resources/images/button_red.png'

    def changeText(self):
        # Se vuelve a cargar el texto
        scoreText = str(RecordManager.getRecord(self.n))
        font = pg.font.Font(GUI_FONT, 42)
        self.text = font.render(scoreText, True, BROWN)
        pos = self.rect.center
        self.textRect = self.text.get_rect(center=pos)

    def refresh(self):
        self.changeText()

    def action(self):
        pass


class ButtonBackRecords(ButtonGUI):
    def __init__(self, screen):
        pos = UtilsGUI.calculatePosition(MAIN_MENU_Y0, BUTTON_SEP_Y, MAIN_MENU_LAYOUT, 2)
        ButtonGUI.__init__(self, screen, BUTTON_IMAGE, BUTTON_SIZE, pos, 'Volver')

    def action(self):
        self.screen.menu.showInitialScreen()

# ---------------------------------------------------------
# Pantalla

class RecordsScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_blur.png')
        # Creamos los elementos GUI
        textTitle = TextRecords(self)
        textBestScores = TextBestScores(self)
        boardRecord1 = BoardWithScore(self, 1)
        boardRecord2 = BoardWithScore(self, 2)
        boardRecord3 = BoardWithScore(self, 3)
        buttonBack = ButtonBackRecords(self)
        # Y los metemos en la lista
        self.elementsGUI.append(textTitle)
        self.elementsGUI.append(textBestScores)
        self.elementsGUI.append(boardRecord1)
        self.elementsGUI.append(boardRecord2)
        self.elementsGUI.append(boardRecord3)
        self.elementsGUI.append(buttonBack)
