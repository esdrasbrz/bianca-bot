"""
Arquivo para ordenar o banco de dados e salvar em um arquivo em ordem com maior ocorrência
"""

class TrendsWords:
    def __init__(self, classify, log):
        self.classify = classify
        self.log = log

        self.PATH = '../bd/'

    def generate(self):
        # percorre o dicionário criando uma lista para ordenar
        lista = []
        for palavra in self.classify.dict:
            try:
                lista.append((palavra, self.classify.dict[palavra]))
            except Exception:
                continue

        lista.sort(key=lambda tup: tup[1], reverse=True)

        # salva a lista em um arquivo de trends
        with open(self.PATH + 'trends_words.txt', 'w') as arq:
            arq.write('\n'.join(['%s:%d' % (tup[0], tup[1]) for tup in lista]))
