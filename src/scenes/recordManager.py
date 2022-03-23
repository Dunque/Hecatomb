from src.settings.settings import *

# Módulo para relizar accesos a archivo con records


def getRecord(n):
    "Devuelve la n-ésima mejor puntuación, n = {1, 2, 3}"

    with open(RECORDS_FILE, 'r') as f:
        scores = f.readline().split(',')
    return scores[n-1]


def updateRecords(score):
    "Actualiza el archivo de records teniendo en cuenta el nuevo score"

    with open(RECORDS_FILE, 'r') as f:
        scores = f.readline().split(',')

    scores = [int(x) for x in scores]

    if score <= scores[-1]:
        return

    scores.append(score)
    scores.sort(reverse=True)
    scores = scores[:3]

    scores = [str(x) for x in scores]
    
    with open(RECORDS_FILE, 'w') as f:
        f.write(scores[0])
        for x in scores[1:]:
            f.write(',' + x)
