# Módulo para manejar la dificultad del juego

# Modos de dificultad = {0: fácil, 1: normal, 2: difícil}

# Valor inicial de dificultad
global difficulty
difficulty = 1

# Puntuación por cada habitación superada
NUMBER_DIFFICULTIES = 3

# Cambiar dificultad
def changeDifficulty():
    global difficulty
    difficulty = (difficulty + 1) % NUMBER_DIFFICULTIES
