# -*- coding: utf-8 -*-
"""
Classe com as funcoes para postar novos conteudos no twitter, dar RT e favoritar

@author Esdras R. Carmo
"""

import re

class Post:
    """
    Construtor que recebe a api twitter
    """
    def __init__(self, api):
        self.api = api

    """
    Posta novo conteudo com base nos trends topics
    """
    def post(self):
        # pesquisa os trendings topics
        trends = self.api.GetTrendsWoeid(455828)

        # cria um filtro regex
        filtro = re.compile(r'\@')

        # percorre os resultados
        for trend in trends:
            print trend
