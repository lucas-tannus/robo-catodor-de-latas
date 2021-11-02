from mapa import Mapa
from algortimoGeneticoSimples import SimpleGeneticAlgorithm


if __name__ == '__main__':
    mapa = Mapa(10)
    mapa.mostrar()

    SimpleGeneticAlgorithm(mapa).run()
