import numpy, time
import math
import itertools
from mapa import *
import sys
from tkinter import *
from PIL import ImageTk, Image
import os

##   Esta classe detém a implementação do algorítmo A*
class A_star(object):

    ##  Construtor da classe
    #   @param linhas Quantidade de linhas da matriz a ser gerada
    #   @param colunas Quantidade de colunas da matriz a ser gerada
    def __init__(self, linhas, colunas, height, width):
        ##  @var nodos_fechados
        #   @brief Guarda todos os nodos que já foram inspecionados
        self.nodos_fechados = []
        ##  @var nodos_abertos
        #   @brief Guarda todos os nodos que foram abertos por outro nodo
        self.nodos_abertos = []
        ##  @var nodo_atual
        #   @brief Detém o nodo atual da busca
        self.nodo_atual = None
        ##  @var nodo_objetivo
        #   @brief Detém o nodo escolhido como objetivo
        self.nodo_objetivo = None
        ##  @var mapa
        #   @brief  Uma instancia da classe Mapa
        self.height = height
        self.width = width
        self.mapa = Mapa(linhas, colunas)

    ##  Método da classe
    #   @param nodo Recebe um objeto da classe Nodo
    #   @brief Calcula o valor da função heurística h(x), que consiste na distância entre o nodo
    #   passado como parâmetro e o nodo objetivo
    #   @return Retorna a distância calculada
    def calcula_h(self, nodo):
        linha_objetivo, coluna_objetivo = self.mapa.obter_posicao(self.nodo_objetivo)
        linha_nodo, coluna_nodo = self.mapa.obter_posicao(nodo)
        abs_x = int(math.fabs(linha_objetivo - linha_nodo + 1))
        abs_y = int(math.fabs(coluna_objetivo - coluna_nodo + 1))

        return abs_y + abs_x

    ##  Método da classe
    #   @param linha Recebe o número da linha
    #   @param coluna Recebe o número da coluna
    #   @brief Seta o objetivo na posição do mapa indicado pelos parâmetros: linha e coluna
    def define_objetivo(self, linha, coluna):
        self.mapa.grade[linha][coluna].objetivo = True
        self.nodo_objetivo = self.mapa.grade[linha][coluna]

    ##  Método da classe
    #   @param linha Recebe o número da linha
    #   @param coluna Recebe o número da coluna
    #   @brief Seta o inicio na posição do mapa indicado pelos parâmetros: linha e coluna
    def define_inicio(self, linha, coluna):
        self.mapa.grade[linha][coluna].inicio = True
        self.nodo_atual = self.mapa.grade[linha][coluna]
        self.nodos_abertos.append(self.nodo_atual)

    ##  Método da classe
    #   @param linha Recebe o número da linha
    #   @param coluna Recebe o número da coluna
    #   @brief Bloqueia um nodo indicado pelos parâmetros: linha e coluna
    def bloqueia_nodo(self, linha, coluna):
        self.mapa.grade[linha][coluna].bloqueado = True

    ##  Método da classe
    #   @param nodo Recebe um objeto da classe Nodo
    #   @brief Calcula o valor da função de custo total f(x) = h(x) + g(x) e
    #   seta o nodo_atual como o nodo_pai do nodo passado como parâmetro
    #   @return None caso o nodo ainda não exista em nenhuma das listas (nodos_fechados e nodos_abertos),
    #   True caso o nodo exista em alguma das listas e o valor do f foi efetivamente trocado, False caso
    #   ele exista em alguma das listas e o valor do f não foi trocado. 
    def calcula_f(self, nodo):
        if nodo:
            flag = None
            g_aux = 1 + self.nodo_atual.g
            if nodo.f == 0:
                nodo.g = g_aux
                nodo.h = self.calcula_h(nodo)
                nodo.f = g_aux + nodo.h
                nodo.nodo_pai = self.nodo_atual
            else:
                if g_aux < nodo.g:
                    flag = True
                    nodo.g = g_aux
                    nodo.f = g_aux + nodo.h
                    nodo.nodo_pai = self.nodo_atual
                else:
                    flag = False
        return flag

    ##  Método da classe
    #   @brief Obtém dos nodos vizinhos(direita, esquerda, cima, baixo) do nodo atual
    #   @return Retorna os vizinhos do nodo
    def obter_vizinhos(self):
        matrix_linhas = len(self.mapa.grade) - 1
        matrix_colunas = len(self.mapa.grade[0]) - 1
        linha_atual, coluna_atual = self.mapa.obter_posicao(self.nodo_atual)
        if (coluna_atual - 1) >= 0:
            if not self.mapa.grade[linha_atual][coluna_atual - 1].bloqueado:
                vizinho_esquerda = self.mapa.grade[linha_atual][coluna_atual - 1]
            else:
                vizinho_esquerda = None
        else:
            vizinho_esquerda = None
        if (coluna_atual + 1) <= matrix_colunas:
            if not self.mapa.grade[linha_atual][coluna_atual + 1].bloqueado:
                vizinho_direita = self.mapa.grade[linha_atual][coluna_atual + 1]
            else:
                vizinho_direita = None
        else:
            vizinho_direita = None
        if (linha_atual - 1) >= 0:
            if not self.mapa.grade[linha_atual - 1][coluna_atual].bloqueado:
                vizinho_cima = self.mapa.grade[linha_atual - 1][coluna_atual]
            else:
                vizinho_cima = None
        else:
            vizinho_cima = None
        if (linha_atual + 1) <= matrix_linhas:
            if not self.mapa.grade[linha_atual + 1][coluna_atual].bloqueado:
                vizinho_baixo = self.mapa.grade[linha_atual + 1][coluna_atual]
            else:
                vizinho_baixo = None
        else:
            vizinho_baixo = None

        return vizinho_esquerda, vizinho_direita, vizinho_baixo, vizinho_cima

    ##  Método da classe
    #   @param nodo Recebe um objeto da classe Nodo
    #   @brief Calcula o custo f do nodo, caso ele estreja presente na lista de nodos fechados
    #   e o valor de f foi alterado então ele é recolocado na lista de nodos abertos novamente,
    #   caso o nodo não esteja presente em nenhuma das listas (nodos_fechados e nodos_abertos), então
    #   ele é adicionado na lista de nodos_abertos
    def abre_nodo(self, nodo):
        if nodo and not nodo.inicio:
            flag = self.calcula_f(nodo)
            if flag is not None:
                if flag:
                    for fechados in self.nodos_fechados:
                        if fechados:
                            if fechados == nodo:
                                self.nodos_fechados.remove(nodo)
                                self.nodos_abertos.append(nodo)
                                break
            else:
                self.nodos_abertos.append(nodo)

    ##  Método da classe
    #   @brief Fecha o nodo atual, removendo-o da lista nodos_abertos e inserindo-o na lista
    #   nodos_fechados
    def fecha_nodo(self):
        self.nodos_abertos.remove(self.nodo_atual)
        self.nodos_fechados.append(self.nodo_atual)

    ##  Método da classe
    #   @brief Verifica dentre os nodos da lista nodos_abertos aquele com o menor custo e coloca-o
    #   como nodo atual
    #   @return Retorna True caso exista algum valor na lista, False caso contrário
    def muda_nodo(self):
        f = math.inf
        if self.nodos_abertos:
            for iterator in self.nodos_abertos:
                if iterator.f < f:
                    f = iterator.f
                    nodo = iterator
            self.nodo_atual = nodo
            return True
        else:
            return False

    ##  Método da classe
    #   @param nodo Recebe um objeto da classe tkinter.Tk
    #   @brief A partir do nodo atual, percorre através dos nodo_pai até não existir mais nenhum
    #   e substitui na interface grafica a imagem do nodo atual, para identificar o caminho percorrido.
    #   @brief Além de imprimir no terminal o custo total até o nodo objetivo
    def imprime_caminho(self, root):
        iterador_nodo = self.nodo_atual
        print("Custo total = {}".format(iterador_nodo.f))
        while iterador_nodo is not None:
            linha, coluna = self.mapa.obter_posicao(iterador_nodo)
            im = Image.open(os.path.join(r'.', 'path.jpg'))
            resized = im.resize((int(self.width), int(self.height)), Image.NEAREST)
            tkimage = ImageTk.PhotoImage(resized)
            myvar = Label(root, image=tkimage)
            myvar.image = tkimage
            myvar.grid(row=linha, column=coluna)
            iterador_nodo = iterador_nodo.nodo_pai

    ##  Método da classe
    #   @brief Imprime a lista nodos_abertos, mostrando a posição do nodo e seu custo
    def imprime_nodos(self):
        linha, coluna = self.mapa.obter_posicao(self.nodo_atual)
        print("Nodo atual: [{}][{}]".format(linha, coluna))
        print("[Nodos abertos:\n")
        for nodos in self.nodos_abertos:
            linha, coluna = self.mapa.obter_posicao(nodos)
            print("nó = [{}][{}], custo = {}".format(linha, coluna, nodos.f))
        print("]")

    ##  Método da classe
    #   @param nodo Recebe um objeto da classe tkinter.Tk
    #   @brief A partir do nodo atual, abre todos os seus nodos vizinhos e muda para o próximo nodo
    #   de acordo com a função @link muda_nodo()@endlink, até encontrar o nodo objetivo
    def busca_solucao(self, root):
        while True:
            self.fecha_nodo()
            if self.nodo_atual.objetivo:
                self.imprime_caminho(root)
                dialog = Toplevel(root)
                Label(dialog, text="Busca concluída!").pack(pady=5)
                break
            vizinho_esquerda, vizinho_direita, vizinho_baixo, vizinho_cima = self.obter_vizinhos()
            self.abre_nodo(vizinho_direita)
            self.abre_nodo(vizinho_esquerda)
            self.abre_nodo(vizinho_cima)
            self.abre_nodo(vizinho_baixo)
            self.imprime_nodos()
            if not self.muda_nodo():
                self.imprime_caminho(root)
                dialog = Toplevel(root)
                Label(dialog, text="Não foi possível concluir a busca!").pack(pady=5)
                break
