
def calcula_linha(posicao, qtd_colunas):
    return posicao // qtd_colunas


def calcula_coluna(linha, posicao, qtd_colunas):
    return posicao if linha is 0 else posicao % (qtd_colunas * linha)
