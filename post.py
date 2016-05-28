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
    Posta novo conteudo com base no termo de pesquisa
    """
    def post(self, term="medicina", count="100"):
        # pesquisa o termo com count resultados
        search = self.api.GetSearch(term=term, count=count)

        # cria um filtro regex
        filtro = re.compile(r'\@')

        # percorre os resultados
        for result in search:
            text = result.text

            # filtra o resultado
            if filtro.search(text) is None:
                print(text)
