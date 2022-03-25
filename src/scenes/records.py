from src.settings.settings import *

# Clase para realizar accesos a archivo con mejores puntuaciones (records)

class Records:
    # Path del archivo con las mejores puntuaciones
    RECORDS_FILE = 'topScores.txt'

    # Número de mejores puntuaciones que se guardan
    NUMBER_SCORES = 3


    # Devuelve la n-ésima mejor puntuación
    @classmethod
    def getRecord(cls, n):
        with open(cls.RECORDS_FILE, 'r') as f:
            scores = f.readline().strip().split(',')

        score = int(scores[n-1].strip())
        return score

    # Actualiza el archivo con los records teniendo en cuenta el nuevo score
    @classmethod
    def updateRecords(cls, score):
        with open(cls.RECORDS_FILE, 'r') as f:
            scores = f.readline().strip().split(',')

        scores = [int(x.strip()) for x in scores]

        if score <= scores[-1]:
            return

        scores.append(score)
        scores.sort(reverse=True)
        scores = scores[:cls.NUMBER_SCORES]

        scores = [str(x) for x in scores]
        
        with open(cls.RECORDS_FILE, 'w') as f:
            f.write(scores[0])
            for x in scores[1:]:
                f.write(',' + x)
