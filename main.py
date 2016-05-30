# -*- coding: utf-8 -*-
"""
Arquivo principal do BOT, totalmente autonomo que decide sozinho as opcoes

@author Esdras R. Carmo
"""

import twitter
import time
from random import randint
from follow import Follow
from post import Post

## Constantes do APP
CONSUMER_KEY = "iG3uFTZS7iNqGVlroey3cV5os"
CONSUMER_SECRET = "bUZmQxZnaZLfPKeUIRC7EsfpK6S06RUwFHtGqWaaWnduXsC55C"
ACCESS_TOKEN = "736567186169430016-AoxkDtl5irWfSp6XryCDDdKmziOiRsI"
ACCESS_TOKEN_SECRET = "v1X0bORIMR9yYDdpTNUgJMyJuEIHLJA3fnQZy77TKgWjK"

## converte de horas para seguntos
def hour_to_sec(hours):
    return hours*3600

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

# Loop de acoes
while True:
    # lista de acoes
    acoes = []

    # encontra uma opcao entre postar ou dar RT
    acoes.append(randint(1, 3))
    # favorita algo na timeline/trends
    acoes.append(randint(4, 5))

    ## Verifica as opcoes e faz as acoes
    for opcao in acoes:
        try:
            if opcao == 1: # postar
                post.post_by_trends()
            elif opcao == 2: # RT
                post.rt_by_trends()
            elif opcao == 3: # RT na timeline
                post.rt_by_timeline()
            elif opcao == 4: # favorita na timeline
                post.fav_by_timeline()
            elif opcao == 5: # favorita nos trends
                post.fav_by_trends()
        except UnicodeEncodeError as err:
            print("Error: {0}".format(err))

    # sleep por um tempo aleatorio
    sleep = randint(60, hour_to_sec(0.3))

    print("Sleep: %.2f" %sleep)
    time.sleep(sleep)
