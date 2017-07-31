from nodos import *

##   Esta classe detém o mapa em si
class Mapa(object):

    ##  Construtor da classe
    #   @param linhas Quantidade de linhas da matriz a ser gerada
    #   @param colunas Quantidade de colunas da matriz a ser gerada
    def __init__(self, linhas, colunas):
        ##  @var grade
        #   @brief Gera uma matriz de Nodo a partir dos valores passados como parâmetro na função __init__
        self.grade = [[Nodo() for j in range(colunas)] for i in range(linhas)]

    ##  Método da classe
    #   @param nodo Recebe um objeto da classe Nodo
    #   @brief Obtém um objeto da classe Nodo e procura sua localização dentro da matriz 
    #   @return Retorna a linha e a coluna onde o nodo se encontra      
    def obter_posicao(self, nodo):
        matrix_dim = len(self.grade[0])
        item_index = 0
        for row in self.grade:
            for i in row:
                if i == nodo:
                    break
                item_index += 1
            if i == nodo:
                break

        return int(item_index / matrix_dim), (item_index % matrix_dim)