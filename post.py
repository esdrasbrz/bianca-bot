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
    Retorna um post aleatorio em trend aleatorio
    """
    def get_post_trend_random(self):
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

        # retorna a postagem
        return possiveis[index]

    """
    Posta novo conteudo com base nos trends topics
    """
    def post_by_trends(self):
        # pega a postagem aleatoria
        post = self.get_post_trend_random()

        # posta a mensagem
        self.api.PostUpdate(post.text)

    """
    RT em conteudo com base nos trends topics
    """
    def rt_by_trends(self):
        # pega a postagem aleatoria
        post = self.get_post_trend_random()

        # Retwitta
        self.api.PostRetweet(post.id)
