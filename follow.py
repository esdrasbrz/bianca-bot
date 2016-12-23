"""
Classe com as funcoes para seguir novas pessoas com base em postagens e seguidores em comum

@author Esdras R. Carmo
"""

from random import randint

class Follow:
    """
    Construtor que recebe a api twitter
    """
    def __init__(self, api, log):
        self.api = api
        self.log = log


    """
    Encontra novas pessoas por base em postagens

    Terms contem os termos que deverao ser pesquisado, que
    retornara count resultados para checagem
    """
    def follow_by_search(self, term="medicina", count="10"):
        search = self.api.GetSearch(term=term, count=count)

        # percorre os resultados
        for result in search:
            post = result.text

            # Printa o resultado no log
            self.log.append(post)
            self.log.append("")
            self.log.append(result.user.screen_name)
            self.log.append("")

            # segue o usuário
            self.api.CreateFriendship(result.user.id)
            self.log.append("Seguido com sucesso!")


    """
    Encontra novas pessoas através de tendências nos trends em uma quantidade aleatória
    """
    def follow_by_trend(self, count="10"):
        self.log.append("follow_by_trend: count = %s" %count)

        # pesquisa os trendings topics com id de campinas
        trends = self.api.GetTrendsWoeid(455828)
 
        # pega um trending topic aleatorio
        index = randint(0, len(trends)-1)
        query = trends[index].query

        # pesquisa com a query encontrada
        self.follow_by_search(term=query, count=count)
