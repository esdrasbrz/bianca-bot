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

        # abre o banco de dados lendo os termos encontrados anteriormente
        with open('dict_bd.txt', 'r') as arq:
            linhas = arq.read().split('\n')

            for linha in linhas:
                try:
                    linha = linha.split(':')
                    self.dict[linha[0]] = int(linha[1])
                except Exception:
                    continue

        self.log.append("Iniciado banco de dados com %d palavras." % len(self.dict))
        self.log.flush()

        # lista com as palavras a serem ignoradas
        self.ignore = []
        with open('palavras_ignorar.txt', 'r') as arq:
            self.ignore = arq.read().split('\n')

        # lista com os caracteres a serem removidos
        self.remover = list(".,/?;:'\"[]{}\\|-_=+`~!@#$%^&*()1234567890")

    """
    Função para salvar em um arquivo o dicionário
    """
    def save_bd(self):
        with open('dict_bd.txt', 'w') as arq:
            for palavra in self.dict:
                arq.write('%s:%d\n' % (palavra, self.dict[palavra]))


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
                    # ignora um link
                    if palavra[:4] == 'http':
                        continue
                    
                    # remove os caracteres especificados
                    for caracter in self.remover:
                        palavra = palavra.replace(caracter, '')

                    if palavra and palavra not in self.ignore:
                        if palavra not in self.dict:
                            self.dict[palavra] = 1
                        else:
                            self.dict[palavra] += 1

        self.save_bd()
        self.log.append("Finalizando análise com %d palavras no dicionário." % len(self.dict))
        self.log.flush()

    """
    Classifica o texto com base no banco de dados armazenado. Retorna um inteiro, quanto maior, melhor
    """
    def classify(self, text):
        nota = 0

        # percorre as palavras do texto
        for palavra in text:
            # ignora um link
            if palavra[:4] == 'http':
                continue
                    
            # remove os caracteres especificados
            for caracter in self.remover:
                palavra = palavra.replace(caracter, '')

            if palavra and palavra not in self.ignore:
                if palavra not in self.dict:
                    self.dict[palavra] = 1
                else:
                    nota += self.dict[palavra]

        return nota
