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
    def __init__(self, api, log, classify):
        self.api = api
        self.log = log
        self.classify = classify

    """
    Retorna uma lista de posts em trend aleatorio
    """
    def get_posts_trend_random(self):
        # pesquisa os trendings topics com id de campinas
        trends = self.api.GetTrendsWoeid(455828)

        # pega um trending topic aleatorio
        index = randint(0, len(trends)-1)
        query = trends[index].query

        # pesquisa com base na query
        search = self.api.GetSearch(term=query, count="100")
        return search

    """
    Retorna uma lista de posts da timeline
    """
    def get_posts_timeline(self):
        # pesquisa 100 posts da timeline
        timeline = self.api.GetHomeTimeline(count="100", exclude_replies=True)
        return timeline

    """
    Retorna uma tupla com melhor post e sua nota com base em uma lista passada por parâmetro
    """
    def get_best_post(self, search):
        # escolhe o melhor
        melhor_post = (search[0], self.classify.classify(search[0].text))
        for result in search:
            nota = self.classify.classify(result.text)

            if nota > melhor_post[1]:
                melhor_post = (result, nota)

        return melhor_post


    """
    Posta analisando um trend topic aleatório
    """
    def post_by_trends(self):
        # pesquisa com base na query
        search = self.get_posts_trend_random()

        # escolhe o melhor
        melhor_post = self.get_best_post(search)

        # verifica se o melhor post começa com RT, retirando-o
        text = melhor_post[0].text
        if text[:3] == 'RT ':
            text = text.split(':')[1][1:]

        # posta o melhor encontrado
        self.api.PostUpdate(text, media=melhor_post[0].media)
        self.log.append("Postado: %s" %text)
        self.log.append("Nota: %d" %melhor_post[1])


    """
    RT em conteudo com base nos trends topics
    """
    def rt_by_trends(self):
        # pega as postagens aleatoria
        search = self.get_posts_trend_random()

        # escolhe o melhor
        melhor_post = self.get_best_post(search)

        # Retwitta
        self.api.PostRetweet(melhor_post[0].id)
        self.log.append("RT de Trends: %s" %melhor_post[0].text)
        self.log.append("Nota: %d" %melhor_post[1])

    """
    RT em conteudo com base na timeline
    """
    def rt_by_timeline(self):
        # pega as postagens
        search = self.get_posts_timeline()

        # escolhe o melhor
        melhor_post = self.get_best_post(search)

        # RT
        self.api.PostRetweet(melhor_post[0].id)
        self.log.append("RT da Timeline: %s\n" %melhor_post[0].text)
        self.log.append("Nota: %d" %melhor_post[1])

    """
    Favorita um tweet aleatorio da timeline
    """
    def fav_by_timeline(self):
        search = self.get_posts_timeline()

        # escolhe o melhor
        melhor_post = self.get_best_post(search)

        # Favorita
        self.api.CreateFavorite(status_id = melhor_post[0].id)
        self.log.append("Favoritado da Timeline: %s\n" %melhor_post[0].text)
        self.log.append("Nota: %d" %melhor_post[1])

    """
    Favorita um tweet aleatorio dos trends
    """
    def fav_by_trends(self):
        search = self.get_posts_trend_random()

        # escolhe o melhor
        melhor_post = self.get_best_post(search)

        # Favorita
        self.api.CreateFavorite(status_id = melhor_post[0].id)
        self.log.append("Favoritado de Trends: %s\n" %melhor_post[0].text)
        self.log.append("Nota: %d" %melhor_post[1])
