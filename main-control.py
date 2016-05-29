# -*- coding: utf-8 -*-
"""
Arquivo principal do BOT, que possui controle das opcoes

@author Esdras R. Carmo
"""

import twitter
from follow import Follow
from post import Post

## Constantes do APP
CONSUMER_KEY = "iG3uFTZS7iNqGVlroey3cV5os"
CONSUMER_SECRET = "bUZmQxZnaZLfPKeUIRC7EsfpK6S06RUwFHtGqWaaWnduXsC55C"
ACCESS_TOKEN = "736567186169430016-AoxkDtl5irWfSp6XryCDDdKmziOiRsI"
ACCESS_TOKEN_SECRET = "v1X0bORIMR9yYDdpTNUgJMyJuEIHLJA3fnQZy77TKgWjK"


## Abre a conexao
print("Conectando-se")
api = twitter.Api(consumer_key        = CONSUMER_KEY,    \
                  consumer_secret     = CONSUMER_SECRET, \
                  access_token_key    = ACCESS_TOKEN,    \
                  access_token_secret = ACCESS_TOKEN_SECRET)
print("Conectado com sucesso!")
print("")

# instancia as classes
post = Post(api)
follow = Follow(api)

while True:
    ## Imprime menu de acoes
    print("Menu:")
    print("Seguir novas pessoas - 1")
    print("Postar com base em trends - 2")
    print("RT com base em trends - 3")
    print("Favoritar com base em timeline - 4")
    print("RT com base em timeline - 5")
    print("Sair - 0")

    # recebe a opcao
    opcao = int(raw_input("Opção: "))

    ## Verifica as opcoes e faz as acoes
    if opcao == 1: # seguir novas pessoas
        term = raw_input("Digite os termos de pesquisa: ")
        count = raw_input("Quantos resultados? ")

        follow.follow_by_search(term=term, count=count)
    elif opcao == 2: # postar
        post.post_by_trends()
    elif opcao == 3: # RT
        post.rt_by_trends()
    elif opcao == 4:
        post.fav_by_timeline()
    elif opcao == 5:
        post.rt_by_timeline()
    elif opcao == 0: # sair
        print("Bye!")
        break
