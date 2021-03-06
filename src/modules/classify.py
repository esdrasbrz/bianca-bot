"""
Classe responsável por analisar e classificar as palavras no twitter criando uma
base de dados capaz de classificar a popularidade de um tweet
"""

from random import randint
import math

class Classify:
    def __init__(self, api, log):
        self.api = api
        self.log = log

        # diretório onde se encontra os arquivos do banco de dados
        self.PATH = '../bd/'

        # dicionário com as palavras encontradas e sua frequência
        self.dict = {}
        # lista com as palavras a serem ignoradas
        self.ignore = []
        # lista com os caracteres a serem removidos
        self.remover = []

        # carrega o BD para a memória
        self.open_bd()
 
    """
    Função para pegar um texto e separar em uma lista de palavras
    """
    def _get_words(self, text):
        return [palavra for linha in text.split('\n') for palavra in linha.split(' ')]

    """
    Verifica se a palavra é válida
    """
    def _check_word(self, palavra):
        palavra = palavra.lower()

        # ignora um link ou palavra específica
        if palavra[:4] == 'http' or palavra in self.ignore:
            return False
                    
        # remove os caracteres especificados
        for caracter in self.remover:
            palavra = palavra.replace(caracter, '')

        return palavra

    """
    Função para abrir o banco de dados, carregando os dados para o dict
    """
    def open_bd(self):
        self.dict = {}

        # abre o banco de dados lendo os termos encontrados anteriormente
        with open(self.PATH + 'dict_bd.txt', 'r') as arq:
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
        with open(self.PATH + 'palavras_ignorar.txt', 'r') as arq:
            self.ignore = arq.read().split('\n')

        self.log.append("Carregado palavras_ignorar com %d palavras." % len(self.ignore))
        self.log.flush()

        # lista com os caracteres a serem removidos
        self.remover = []
        with open(self.PATH + 'char_ignorar.txt', 'r') as arq:
            self.remover = list(arq.read())

        self.log.append("Carregado char_ignorar com %d caracteres." % len(self.remover))
        self.log.flush()


    """
    Função para salvar em um arquivo o dicionário
    """
    def save_bd(self):
        with open(self.PATH + 'dict_bd.txt', 'w') as arq:
            for palavra in self.dict:
                arq.write('%s:%d\n' % (palavra, self.dict[palavra]))

    def rt_fav_point(self):
        # recebe as últimas publicações, para classificar a primeira
        timeline = self.api.GetUserTimeline(count="50", exclude_replies=True, include_rts=False)

        # media das 5 primeiras
        media_rts = sum([timeline[i].retweet_count for i in range(1, 5)]) // 4
        media_fav = sum([timeline[i].favorite_count for i in range(1, 5)]) // 4

        # pega o último da timeline para fazer a análise
        status = timeline[0]
        
        # calcula o excedente de rts e favs
        n_rts = status.retweet_count - media_rts
        n_fav = status.favorite_count - media_fav

        self.log.append("Analisando o último tweet com relativo de %d RTs e %d favoritos." % (n_rts, n_fav))
        self.log.flush()

        # percorre as palavra se pelo menos um deles for positivo
        if n_rts > 0 or n_fav > 0:
            palavras = self._get_words(status.text)
            
            for palavra in palavras:
                palavra = self._check_word(palavra)
                if palavra:
                    antigo = self.dict[palavra]

                    if n_rts > 0: 
                        self.dict[palavra] += int(10 * n_rts**2 * math.log(antigo))
                    if n_fav > 0:
                        self.dict[palavra] += int(8 * n_fav**2 * math.log(antigo))

                    self.log.append("Atualizado palavra %s de %d para %d." % (palavra, antigo, self.dict[palavra]))
                    self.log.flush()
        else:
            self.log.append("Terminado sem atribuir pontuação.")

        self.save_bd()

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
                # cria o vetor de palavras
                palavras = self._get_words(result.text)

                for palavra in palavras:
                    palavra = self._check_word(palavra)
                    if palavra:
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
        count = 0

        # cria o vetor de palavras
        palavras = self._get_words(text)

        # percorre as palavras do texto
        for palavra in palavras:
            palavra = self._check_word(palavra)
            if palavra:
                if palavra not in self.dict:
                    self.dict[palavra] = 1
                else:
                    count += 1
                    nota += self.dict[palavra]

        if count > 0:
            nota = nota // count

        return nota
