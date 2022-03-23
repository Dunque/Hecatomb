# Módulo para manejar la puntuación en modo Survival

# Valor inicial de la puntuación
global score

# Puntuación por cada habitación superada
CLEARED_ROOM_SCORE = 1

# Obtener puntuación
def getScore():
    global score
    return score

# Reiniciar puntuación
def resetScore():
    global score
    score = 0

# Sumar la puntuación por superar habitación
def addScoreClearedRoom():
    global score
    score += CLEARED_ROOM_SCORE
