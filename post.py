# -*- coding: utf-8 -*-
"""
Classe com as funcoes para postar novos conteudos no twitter, dar RT e favoritar

@author Esdras R. Carmo
"""

import re
from random import randint

class Post:
    """
    Construtor que recebe a api twitter
    """
    def __init__(self, api):
        self.api = api

    """
    Posta novo conteudo com base nos trends topics
    """
    def post_by_trends(self):
        # pesquisa os trendings topics com id de campinas
        trends = self.api.GetTrendsWoeid(455828)

        # lista com os posts possiveis
        possiveis = []

        # cria um filtro regex para retirar mentions
        mentions_filter = re.compile(r'\@')

        # pega um trending topic aleatorio
        index = randint(0, len(trends)-1)
        query = trends[index].query

        # pesquisa com base na query
        search = self.api.GetSearch(term=query, count="100")
        for result in search:
            # verifica o filtro de mentions
            if mentions_filter.search(result.text) is None:
                possiveis.append(result)

        # pega uma postagem aleatoria
        index = randint(0, len(possiveis)-1)

        # posta a mensagem
        self.api.PostUpdate(possiveis[index].text)
