# -*- coding: utf-8 -*-
"""
Classe com as funcoes para seguir novas pessoas com base em postagens e seguidores em comum

@author Esdras R. Carmo
"""

import time

class Follow:
    """
    Construtor que recebe a api twitter
    """
    def __init__(self, api):
        self.api = api


    """
    Encontra novas pessoas por base em postagens

    Terms contem os termos que deverao ser pesquisado, que
    retornara count resultados para checagem
    """
    def follow_by_search(self, term="medicina", count="10"):
        search = self.api.GetSearch(term=term, count=count)

        # percorre os resultados
        for result in search:
            # Printa o resultado na tela
            print(result.text)
            print("")
            print(result.user.screen_name)
            print("")

            # verifica a opcao
            opcao = raw_input("Deseja seguir? (S ou N) ")

            if opcao == 'S' or opcao == 's':
                # segue o usuário
                self.api.CreateFriendship(result.user.id)
                print("Seguido com sucesso!")

            print("")
            print("")
