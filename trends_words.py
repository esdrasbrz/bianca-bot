"""
Arquivo para ordenar o banco de dados e salvar em um arquivo em ordem com maior ocorrência
"""

from classify import Classify
from log import Logger

log = Logger(identifier="trends")
classify = Classify(None, log)

# percorre o dicionário criando uma lista para ordenar
lista = []
for palavra in classify.dict:
    try:
        lista.append((palavra, classify.dict[palavra]))
    except Exception:
        continue

lista.sort(key=lambda tup: tup[1], reverse=True)

# salva a lista em um arquivo de trends
with open('trends_words.txt', 'w') as arq:
    arq.write('\n'.join(['%s:%d' % (tup[0], tup[1]) for tup in lista]))
