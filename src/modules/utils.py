"""
Arquivo com utilitários para o debugger
"""

class Utils:
    def __init__(self, classify, log):
        self.classify = classify
        self.log = log

        self.PATH = '../bd/'

    """
    Função que gera o arquivo de trends words ordenando o banco de dados pelo número de ocorrências
    """
    def generate_trends(self):
        # percorre o dicionário criando uma lista para ordenar
        lista = []
        for palavra in self.classify.dict:
            try:
                lista.append((palavra, self.classify.dict[palavra]))
            except Exception:
                continue

        lista.sort(key=lambda tup: tup[1], reverse=True)

        # salva a lista em um arquivo de trends
        with open(self.PATH + 'trends_words.txt', 'w') as arq:
            arq.write('\n'.join(['%s:%d' % (tup[0], tup[1]) for tup in lista]))

    """
    Função para atualizar o banco de dados retirando as palavras que estão presentes no palavras_ignorar.txt
    """
    def trim_words(self):
        # lista com as palavras a serem removidas
        remover = []

        # percorre o dicionário
        for palavra in self.classify.dict:
            # verifica se a palavra está no ignorar
            if palavra in self.classify.ignore:
                remover.append(palavra)

        self.log.append("Removendo %d palavras do dicionário." % len(remover))
        self.log.flush()

        # remove as palavras listadas anteriormente
        for palavra in remover:
            del self.classify.dict[palavra]
        
        # salva o banco de dados novamente
        self.classify.save_bd()

        self.log.append("Removido com sucesso")
        self.log.flush()
