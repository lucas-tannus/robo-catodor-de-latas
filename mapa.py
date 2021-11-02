from random import randint
from contantes import *
from utils import calcula_coluna, calcula_linha
from math import sqrt
from pathlib import Path


class Estado(object):

    def __init__(self, tipo=CAMINHO):
        self.tipo = tipo

    def get_tipo(self):
        return TIPOS[self.tipo]

    def get_recompensa(self):
        return RECOMPENSAS.get(self.tipo)


class Mapa(object):

    def __init__(self, dimensao):
        self.dimensao = dimensao
        self.mapa = self.carrega() if Path(f'mapas/mapa{self.dimensao}.txt').exists() else self.cria()

    def cria(self):
        mapa = []
        for _ in range(self.dimensao ** 2):
            mapa.append(Estado())

        num_latas = 0
        while num_latas != (PORCENTAGEM_LATAS * (self.dimensao ** 2)):
            index = randint(0, self.dimensao ** 2)
            if not mapa[index].tipo == LATA_ACO:
                mapa[index] = Estado(LATA_ACO)
                num_latas += 1

        mapa_texto = [estado.tipo for estado in mapa]
        with open(f'mapas/mapa{self.dimensao}.txt', 'a') as file:
            file.write(','.join(mapa_texto))
        return mapa

    def carrega(self):
        with open(f'mapas/mapa{self.dimensao}.txt', 'r') as file:
            estados = file.read()

        mapa = []
        for estado in estados.split(','):
            mapa.append(Estado(estado))
        return mapa

    def mostrar(self):
        for index, estado in enumerate(self.mapa):
            if (index + 1) % self.dimensao == 0:
                print(f'{estado.get_tipo()}')
            else:
                print(f'{estado.get_tipo()}', end=' ')

    @staticmethod
    def pode_ir_para_direita(posicao):
        if posicao is 0:
            return True
        qtd_colunas = int(sqrt(DIMENSAO**2))
        linha = calcula_linha(posicao, qtd_colunas)
        coluna = calcula_coluna(linha, posicao, qtd_colunas)
        return not (coluna is qtd_colunas - 1) if linha is 0 else not ((linha + 1) * (coluna + 1) % posicao is 1)

    @staticmethod
    def pode_ir_para_esquerda(posicao):
        return not (posicao % int(sqrt(DIMENSAO**2)) is 0)

    @staticmethod
    def eh_estado_permitido(posicao):
        return 0 <= posicao < DIMENSAO**2

    def get_recompensa(self, posicao):
        return self.mapa[posicao].get_recompensa()

    def get_tipo_estado(self, posicao):
        return self.mapa[posicao].get_tipo()
