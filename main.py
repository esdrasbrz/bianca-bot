"""
Arquivo principal do BOT, totalmente autonomo que decide sozinho as opcoes

@author Esdras R. Carmo
"""

import twitter
import time
from random import randint
from follow import Follow
from post import Post
from log import Logger

## converte de horas para seguntos
def hour_to_sec(hours):
    return hours*3600

## Constantes do APP
CONSUMER_KEY = "iG3uFTZS7iNqGVlroey3cV5os"
CONSUMER_SECRET = "bUZmQxZnaZLfPKeUIRC7EsfpK6S06RUwFHtGqWaaWnduXsC55C"
ACCESS_TOKEN = "736567186169430016-AoxkDtl5irWfSp6XryCDDdKmziOiRsI"
ACCESS_TOKEN_SECRET = "v1X0bORIMR9yYDdpTNUgJMyJuEIHLJA3fnQZy77TKgWjK"

## Constantes para os randoms
MIN_FOLLOW = 3
MAX_FOLLOW = 50
ACOES_POR_ITERACAO = 2
MIN_SLEEP = 30
MAX_SLEEP = hour_to_sec(1)

## instancia o logger
log = Logger()

## Abre a conexao
log.append("Conectando-se")
api = twitter.Api(consumer_key        = CONSUMER_KEY,    \
                  consumer_secret     = CONSUMER_SECRET, \
                  access_token_key    = ACCESS_TOKEN,    \
                  access_token_secret = ACCESS_TOKEN_SECRET)
log.append("Conectado com sucesso!")
log.append("--------")
log.append("")

log.flush()

# instancia as classes
post = Post(api, log)
follow = Follow(api, log)

## mapa com as ações possíveis
acoes = {1: lambda: follow.follow_by_trend(count=str(randint(MIN_FOLLOW, MAX_FOLLOW))),
        2: lambda: post.post_by_trends(),
        3: lambda: post.rt_by_trends(),
        4: lambda: post.fav_by_timeline(),
        5: lambda: post.rt_by_timeline()}

## MAIN LOOP
while True:
    # escolhe algumas opções
    opcoes = [randint(min(acoes.keys()), max(acoes.keys())) for i in range(ACOES_POR_ITERACAO)]

    try:
        for opcao in opcoes:
            acoes[opcao]()
    except Exception as e:
        log.append("EXCEPTION: %s" % e)

    delay = randint(MIN_SLEEP, MAX_SLEEP)
    log.append('')
    log.append('delay: %d s.' % delay)
    log.flush()

    time.sleep(delay)
