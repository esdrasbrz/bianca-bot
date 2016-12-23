"""
Classe com as funcoes para armazenar log do bot

@author Esdras R. Carmo
"""

from datetime import date, datetime

class Logger:
    def __init__(self):
        self.log = [] # cria uma fila vazia

    """
    Função para armazenar uma nova linha
    """
    def append(self, line):
        self.log.append('[' + datetime.now().strftime('%H:%M:%S') + ']: ' + line)

    """
    Função para dar flush no arquivo final, salvando alterações
    """
    def flush(self):
        path = 'log/'
        filename = date.today().strftime('%Y-%m-%d') + '.log'

        with open(path + filename, 'a') as arq:
            arq.write('\n'.join(self.log) + '\n')

        self.log = []
