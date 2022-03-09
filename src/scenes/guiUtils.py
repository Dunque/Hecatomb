import pygame as pg
from src.settings.settings import *


# -------------------------------------------------
# Clase guiUtils

class UtilsGUI(object):

    @staticmethod
    def calculatePosition(y0, sepY, menuSize, n):
        """Calcula la posición del centro del rectángulo que ocupa el n-ésimo botón 
        (n = 0, 1, 2...) en un menú de tamaño menuSize, empezando en la altura y0, 
        separándolos en el eje Y con sepY"""

        (cols, rows) = menuSize
        assert (n+1 <= cols*rows), f"There are more buttons than positions ({cols*rows} positions)"

        dx = BUTTON_WIDTH + BUTTON_SEP_X
        dy = BUTTON_HEIGHT + sepY
        x0 = WIDTH/2 - (cols-1)*dx/2
        col = n // rows
        row = n % rows

        return (x0 + col*dx, y0 + row*dy)
