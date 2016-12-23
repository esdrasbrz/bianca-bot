"""
Classe responsável por analisar e classificar as palavras no twitter criando uma
base de dados capaz de classificar a popularidade de um tweet
"""

from random import randint

class Classify:
    def __init__(self, api, log):
        self.api = api
        self.log = log

        # dicionário com as palavras encontradas e sua frequência
        self.dict = {}

        # lista com as palavras a serem ignoradas
        self.ignore = []
        with open('palavras_ignorar.txt', 'r') as arq:
            self.ignore = arq.read().split('\n')

    """
    Função para analisar os trends topics do twitter 
    """
    def analyze(self):
        self.log.append("Iniciando análise")

        # pesquisa os trendings topics com id de campinas
        trends = self.api.GetTrendsWoeid(455828)

        for trend in trends:
            # lista com os posts possiveis
            possiveis = []
    
            # pega a query
            query = trend.query
            self.log.append("Analisando query: %s" % query)
            self.log.flush()

            # pesquisa com base na query
            search = self.api.GetSearch(term=query, count="100", lang='pt')

            # percorre a pesquisa classificando as palavras encontradas
            for result in search:
                for palavra in result.text.split(' '):
                    if palavra not in self.ignore:
                        if palavra not in self.dict:
                            self.dict[palavra] = 1
                        else:
                            self.dict[palavra] += 1

        self.log.append("Finalizando análise com %d palavras no dicionário." % len(self.dict))

    """
    Classifica o texto com base no banco de dados armazenado. Retorna um inteiro, quanto maior, melhor
    """
    def classify(self, text):
        nota = 0

        # percorre as palavras do texto
        for palavra in text:
            if palavra not in self.ignore:
                if palavra not in self.dict:
                    self.dict[palavra] = 1
                else:
                    nota += self.dict[palavra]

        return nota
