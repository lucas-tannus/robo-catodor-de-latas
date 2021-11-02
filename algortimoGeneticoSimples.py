from random import random, randint
from agente import Agente
from contantes import *


class SimpleGeneticAlgorithm:

    def __init__(self, mapa):
        self.mapa = mapa
        self.populacao = self._gerar_populacao(TAMANHO_POPULACAO)

    def run(self):
        while True:
            aptidoes = {}
            index_selecionados = []

            for index, agente in enumerate(self.populacao):
                aptidoes[index] = self.calcular_aptidao(agente)

            while len(index_selecionados) == 0:
                index_selecionados = self.selecao_pela_roleta(aptidoes)

            nova_populacao = []
            for index in index_selecionados:
                nova_populacao.append(self.populacao[index])

            self.populacao = self.realizar_cruzamento(nova_populacao)

            for agente in self.populacao:
                self.calcular_aptidao(agente)

            if self.aprendeu():
                break

    def aprendeu(self):
        self.populacao.sort(key=lambda x: x.aptidao)

        print(f'Melhor da populacao {self.populacao[0].aptidao}')
        return self.populacao[0].aptidao > PORCENTAGEM_LATAS * (self.mapa.dimensao ** 2) * 10 * 0.8

    def _gerar_populacao(self, size):
        return [Agente(self.mapa) for _ in range(size)]

    def calcular_aptidao(self, agente):
        contador = aptidao = latas_capturadas = 0

        while contador < (0.9 * self.mapa.dimensao**2):
            acao = agente.cromossomo[agente.posicao]

            if not agente.andar(acao):
                aptidao -= 30
            else:
                aptidao += self.mapa.get_recompensa(agente.posicao)

            if self.mapa.get_tipo_estado(agente.posicao) == '1':
                latas_capturadas += 1

            if latas_capturadas == PORCENTAGEM_LATAS * (self.mapa.dimensao ** 2):
                break

            contador += 1
        agente.aptidao = aptidao

        return aptidao

    def selecao_pela_roleta(self, aptidoes):
        soma_aptidoes = sum(aptidoes.values())
        individuos_selecionados = []

        for index, aptidao in aptidoes.items():
            porcentagem = aptidao / soma_aptidoes

            if porcentagem > random():
                individuos_selecionados.append(index)

        return individuos_selecionados

    def realizar_cruzamento(self, nova_populacao):
        soma_aptidoes = sum([agente.aptidao for agente in nova_populacao])
        agente_1 = agente_2 = None
        novos_individuos = []

        while (len(nova_populacao) + len(novos_individuos)) < TAMANHO_POPULACAO:
            while agente_1 is None or agente_2 is None:
                for index, agente in enumerate(nova_populacao):
                    porcentagem = agente.aptidao / soma_aptidoes

                    if porcentagem > random():
                        if agente_1 is None:
                            agente_1 = index
                        elif agente_1 is not None and agente_2 is None:
                            agente_2 = index

                    if agente_1 is not None and agente_2 is not None:
                        novos_individuos.extend(self.cruzar(agente_1, agente_2))

            agente_1 = None
            agente_2 = None

        nova_populacao.extend(novos_individuos)
        return nova_populacao

    def cruzar(self, agente_1, agente_2):
        cromossomo_1 = self.populacao[agente_1].cromossomo
        cromossomo_2 = self.populacao[agente_2].cromossomo

        ponto_de_cross = randint(0, DIMENSAO**2)
        filho_1 = cromossomo_1[:ponto_de_cross] + cromossomo_2[ponto_de_cross:]
        filho_2 = cromossomo_2[:ponto_de_cross] + cromossomo_1[ponto_de_cross:]

        return [Agente(self.mapa, filho_1), Agente(self.mapa, filho_2)]
