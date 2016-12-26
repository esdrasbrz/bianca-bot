"""
Arquivo principal do BOT, que possui controle das opcoes

@author Esdras R. Carmo
"""

import twitter
from modules import *

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
log = Logger('debug')
post = Post(api, log)
follow = Follow(api, log)
classify = Classify(api, log)

## mapa com as ações possíveis
acoes = {1: lambda count: follow.follow_by_trend(count=count),
        2: lambda: post.post_by_trends_with_analysis(classify),
        3: lambda: post.rt_by_trends(),
        4: lambda: post.fav_by_timeline(),
        5: lambda: post.rt_by_timeline()}


while True:
    ## Imprime menu de acoes
    print("Menu:")
    print("Seguir novas pessoas - 1")
    print("Postar com base em trends com análise - 2")
    print("RT com base em trends - 3")
    print("Favoritar com base em timeline - 4")
    print("RT com base em timeline - 5")
    print("Sair - 0")

    # recebe a opcao
    opcao = int(input("Opção: "))

    ## Verifica as opcoes e faz as acoes
    if opcao == 1: # seguir novas pessoas
        count = input("Quantos resultados? ")

        acoes[opcao](count)
    elif opcao != 0:
        acoes[opcao]()
    else: # sair
        print("Bye!")
        break

    log.flush()
