from src.settings.settings import *


# Módulo para realizar accesos a archivo con mejores puntuaciones

RECORDS_FILE = 'topScores.txt'
NUMBER_SCORES = 3


def getRecord(n):
    "Devuelve la n-ésima mejor puntuación"

    with open(RECORDS_FILE, 'r') as f:
        scores = f.readline().strip().split(',')

    score = int(scores[n-1].strip())
    return score


def updateRecords(score):
    "Actualiza el archivo con los records teniendo en cuenta el nuevo score"

    with open(RECORDS_FILE, 'r') as f:
        scores = f.readline().strip().split(',')

    scores = [int(x.strip()) for x in scores]

    if score <= scores[-1]:
        return

    scores.append(score)
    scores.sort(reverse=True)
    scores = scores[:NUMBER_SCORES]

    scores = [str(x) for x in scores]
    
    with open(RECORDS_FILE, 'w') as f:
        f.write(scores[0])
        for x in scores[1:]:
            f.write(',' + x)
