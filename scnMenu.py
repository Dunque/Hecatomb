import pygame
from pygame.locals import *
from scene import *
from resourceManager import *
from settings import *
from scnCutscene1 import *
from scnSurvival import *

# -------------------------------------------------
# Clase abstracta ElementGUI

class ElementGUI:
    def __init__(self, screen, rectangle):
        self.screen = screen
        self.rect = rectangle

    def setPosition(self, position):
        (positionx, positiony) = position
        self.rect.left = positionx
        self.rect.bottom = positiony

    def positionInElement(self, position):
        (positionx, positiony) = position
        if (positionx>=self.rect.left) and (positionx<=self.rect.right) and (positiony>=self.rect.top) and (positiony<=self.rect.bottom):
            return True
        else:
            return False

    def draw(self):
        raise NotImplemented("Tiene que implementar el metodo draw.")
    def action(self):
        raise NotImplemented("Tiene que implementar el metodo action.")


# -------------------------------------------------
# Clase ButtonGUI y los distintos botones

class ButtonGUI(ElementGUI):
    def __init__(self, screen, imageName, position):
        # Se carga la image del boton
        self.image = ResourceManager.LoadImage(imageName,-1)
        self.image = pygame.transform.scale(self.image, (331, 75))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        ElementGUI.__init__(self, screen, self.image.get_rect())
        # Se coloca el rectangle en su position
        self.setPosition(position)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class ButtonGUI(ElementGUI):
    def __init__(self, screen, imageName, position):
        # Se carga la image del boton
        self.image = ResourceManager.LoadImage(imageName,-1)
        self.image = pygame.transform.scale(self.image, (332, 75))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        ElementGUI.__init__(self, screen, self.image.get_rect())
        # Se coloca el rectangle en su position
        self.setPosition(position)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class ButtonMenu(ElementGUI):
    def __init__(self, screen, n, text):
        # Se carga la image del boton
        imageName = 'resources/images/gold_button.png'
        self.image = ResourceManager.LoadImage(imageName,-1)
        self.image = pygame.transform.scale(self.image, (332, 75))
        # Se llama al método de la clase padre con el rectángulo que ocupa el button
        center = (WIDTH/2, HEIGHT/3 + n * 102)
        imageRect = self.image.get_rect(center=center)
        ElementGUI.__init__(self, screen, imageRect)
        # Se coloca el rectangle en su position
        self.setPosition(imageRect.bottomleft)

        # Se carga el texto del button (TODO: arreglar esto, muy mejorable)
        fontName = 'resources/fonts/hanshand.ttf'
        font = pg.font.Font(fontName, 42)
        self.text = font.render(text, True, BLACK)
        self.textRect = self.text.get_rect(center=center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)

class ButtonAdventure(ButtonMenu):
    def __init__(self, screen):
        ButtonMenu.__init__(self, screen, 0, 'Adventure')
    def action(self):
        self.screen.menu.playAdventure()

class ButtonSurvival(ButtonMenu):
    def __init__(self, screen):
        ButtonMenu.__init__(self, screen, 1, 'Survival')
    def action(self):
        self.screen.menu.playSurvival()

class ButtonRecords(ButtonMenu):
    def __init__(self, screen):
        ButtonMenu.__init__(self, screen, 2, 'Records')
    def action(self):
        # self.screen.menu.exitProgram()
        None

class ButtonCredits(ButtonMenu):
    def __init__(self, screen):
        ButtonMenu.__init__(self, screen, 3, 'Credits')
    def action(self):
        # self.screen.menu.exitProgram()
        None

class ButtonOptions(ButtonMenu):
    def __init__(self, screen):
        ButtonMenu.__init__(self, screen, 4, 'Options')
    def action(self):
        # self.screen.menu.exitProgram()
        None

class ButtonExit(ButtonMenu):
    def __init__(self, screen):
        ButtonMenu.__init__(self, screen, 5, 'Exit')
    def action(self):
        self.screen.menu.exitProgram()

# -------------------------------------------------
# Clase TextGUI y los distintos textos

class TextGUI(ElementGUI):
    def __init__(self, screen, font, color, text, position):
        # Se crea la image del text
        self.image = font.render(text, True, color)
        # Se llama al método de la clase padre con el rectángulo que ocupa el text
        ElementGUI.__init__(self, screen, self.image.get_rect())
        # Se coloca el rectangle en su position
        self.setPosition(position)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class TextPlay(TextGUI):
    def __init__(self, screen):
        # La font la debería cargar el estor de recursos
        font = pygame.font.SysFont('arial', 26);
        TextGUI.__init__(self, screen, font, (0, 0, 0), 'Jugar', (WIDTH/2, HEIGHT/2-50))
    def action(self):
        self.screen.menu.nextScene()

class TextExit(TextGUI):
    def __init__(self, screen):
        # La font la debería cargar el estor de recursos
        font = pygame.font.SysFont('arial', 26);
        TextGUI.__init__(self, screen, font, (0, 0, 0), 'Salir', (WIDTH/2, HEIGHT/2+50))
    def action(self):
        self.screen.menu.exitProgram()

# -------------------------------------------------
# Clase ScreenGUI y las distintas pantallas

class ScreenGUI:
    def __init__(self, menu, imageName):
        self.menu = menu
        # Se carga la image de fondo
        self.image = ResourceManager.LoadImage(imageName)
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        # Se tiene una lista de elements GUI
        self.elementsGUI = []

    def events(self, eventList):
        for event in eventList:
            if event.type == MOUSEBUTTONDOWN:
                self.elementClick = None
                for element in self.elementsGUI:
                    if element.positionInElement(event.pos):
                        self.elementClick = element
            if event.type == MOUSEBUTTONUP:
                for element in self.elementsGUI:
                    if element.positionInElement(event.pos):
                        if (element == self.elementClick):
                            element.action()

    def draw(self, screen):
        # Dibujamos primero la image de fondo
        screen.blit(self.image, self.image.get_rect())
        # Después los botones
        for element in self.elementsGUI:
            element.draw(screen)

class InitialScreenGUI(ScreenGUI):
    def __init__(self, menu):
        ScreenGUI.__init__(self, menu, 'resources/images/menu_image.png')
        # Creamos los botones y los metemos en la lista
        buttonAdventure = ButtonAdventure(self)
        buttonSurvival = ButtonSurvival(self)
        buttonRecords = ButtonRecords(self)
        buttonCredits = ButtonCredits(self)
        buttonOptions = ButtonOptions(self)
        buttonExit = ButtonExit(self)
        self.elementsGUI.append(buttonAdventure)
        self.elementsGUI.append(buttonSurvival)
        self.elementsGUI.append(buttonRecords)
        self.elementsGUI.append(buttonCredits)
        self.elementsGUI.append(buttonOptions)
        self.elementsGUI.append(buttonExit)
        # Creamos el text y lo metemos en la lista
        # textPlay = TextPlay(self)
        # textExit = TextExit(self)
        # self.elementsGUI.append(textPlay)
        # self.elementsGUI.append(textExit)

# -------------------------------------------------
# Clase Menu, la escena en sí

class Menu(Scene):

    def __init__(self, sceneManager):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, sceneManager);
        # Creamos la lista de pantallas
        self.screenList = []
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.screenList.append(InitialScreenGUI(self))
        # En que screen estamos actualmente
        self.showInitialScreen()

    def update(self, *args):
        return

    def events(self, eventList):
        # Se mira si se quiere salir de esta escena
        for event in eventList:
            # Si se quiere salir, se le indica al sceneManager
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exitProgram()
            elif event.type == pygame.QUIT:
                self.sceneManager.exitProgram()

        # Se pasa la lista de events a la screen actual
        self.screenList[self.currentScreen].events(eventList)

    def draw(self, screen):
        self.screenList[self.currentScreen].draw(screen)


    #--------------------------------------
    # Metodos propios del menu

    def exitProgram(self):
        self.sceneManager.exitProgram()

    def playAdventure(self):
        scene = Cutscene1(self.sceneManager)
        self.sceneManager.stackScene(scene)

    def playSurvival(self):
        scene = Survival(self.sceneManager)
        self.sceneManager.stackScene(scene)

    def showInitialScreen(self):
        self.currentScreen = 0

    # def mostrarPantallaConfiguracion(self):
    #    self.currentScreen = ...
