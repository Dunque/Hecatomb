import sys

# Clase para manejar la dificultad del juego
# Modos de dificultad = {0: fácil, 1: normal, 2: difícil}

class Difficulty:
    # Valor inicial de dificultad
    difficulty = 1

    # Número de dificultades
    NUMBER_DIFFICULTIES = 3


    # Cambiar dificultad
    @classmethod
    def changeDifficulty(cls):
        cls.difficulty = (cls.difficulty + 1) % cls.NUMBER_DIFFICULTIES

    # Devolver nombre de dificultad
    @classmethod
    def getDifficultyName(cls):
        if cls.difficulty == 0:
            text = "Facil"
        elif cls.difficulty == 1:
            text = "Normal"
        elif cls.difficulty == 2:
            text = "Dificil"
        else:
            sys.exit("Invalid difficulty value")
        return text
