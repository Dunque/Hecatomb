# Clase para manejar la puntuación en modo Survival

class Score:
    # Valor inicial de la puntuación
    score = -1

    # Puntuación por cada habitación superada
    CLEARED_ROOM_SCORE = 1


    # Obtener puntuación
    @classmethod
    def getScore(cls):
        return cls.score

    # Reiniciar puntuación
    @classmethod
    def resetScore(cls):
        cls.score = -1

    # Sumar la puntuación por superar habitación
    @classmethod
    def addScoreClearedRoom(cls):
        cls.score += cls.CLEARED_ROOM_SCORE
