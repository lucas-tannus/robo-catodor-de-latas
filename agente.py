from random import randint
from contantes import *


class Agente(object):

    def __init__(self, mapa, cromossomo=None):
        self.posicao = POSICAO_INICIAL
        self.mapa = mapa
        self.cromossomo = cromossomo if cromossomo else self.gerar()
        self.aptidao = None

    def get_aptidao(self):
        return self.aptidao

    def andar(self, acao):
        posicao = self.posicao

        if acao == 0:
            posicao -= self.mapa.dimensao
            proibido = not self.mapa.eh_estado_permitido(posicao)
        elif acao == 1:
            posicao += self.mapa.dimensao
            proibido = not self.mapa.eh_estado_permitido(posicao)
        elif acao == 2:
            posicao -= 1
            proibido = not self.mapa.pode_ir_para_esquerda(posicao)
        else:
            posicao += 1
            proibido = not self.mapa.pode_ir_para_direita(posicao)

        if proibido:
            self.cromossomo[self.posicao] = randint(0, len(TABELA_ACOES))
            return False
        self.posicao = posicao

        return True

    def gerar(self):
        return [randint(0, len(TABELA_ACOES)) for _ in range(self.mapa.dimensao**2)]
