# -*- coding: utf-8 -*-
"""
Arquivo principal do BOT, que checa as postagens sobre medicina e posta automaticamente
no perfil.

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

while True:
    ## Imprime menu de acoes
    print("Menu:")
    print("Seguir novas pessoas - S")
    print("Postar com base em trends - PT")
    print("RT com base em trends - RT")
    print("Favoritar com base em timeline - F")
    print("Sair - 0")

    # recebe a opcao
    opcao = raw_input("Opção: ")

    # instancia as classes
    post = Post(api)
    follow = Follow(api)

    ## Verifica as opcoes e faz as acoes
    if opcao.lower() == 's': # seguir novas pessoas
        term = raw_input("Digite os termos de pesquisa: ")
        count = raw_input("Quantos resultados? ")

        follow.follow_by_search(term=term, count=count)
    elif opcao.lower() == 'pt': # postar
        post.post_by_trends()
    elif opcao.lower() == 'rt': # RT
        post.rt_by_trends()
    elif opcao.lower() == 'f':
        post.fav_by_timeline()
    elif opcao == '0': # sair
        print("Bye!")
        break
