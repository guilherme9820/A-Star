#!/usr/bin/python3
from tkinter import *
from PIL import ImageTk, Image
import os, random, math
from a_star import *

##   Esta classe implementa a parte gráfica da busca A*
class GUI(object):

    ##  Construtor da classe
    #   @param linha Quantidade de linhas da matriz a ser gerada
    #   @param coluna Quantidade de colunas da matriz a ser gerada
    #   @param porcentagem Porcentagem de nodos a serem bloqueados
    def __init__(self, linha, coluna, porcentagem):
        ##  @var path
        #   @brief Caminho para a pasta com as imagens a serem geradas
        self.path = r"."
        self.height = 600/linha
        self.width = 600/coluna
        ##  @var star
        #   @brief Instância da classe A_star
        self.star = A_star(linha, coluna, self.height, self.width)
        ##  @var tipo
        #   @brief Atributo para identificar o tipo de escolha ao clicar em um nodo
        self.tipo = 'start'
        ##  @var porcentagem
        #   @brief Recebe o valor da porcentagem passado como parâmetro
        self.porcentagem = porcentagem
        ##  @var root
        #   @brief Instância da classe tkinter.Tk
        self.root = Tk()
        ##  @var quantidade
        #   @brief Quantidade de nodos a serem bloqueados
        self.quantidade = None
        self.gera_mapa(linha, coluna)

    ##  Método de evento
    #   @brief Quando ocorre um click sobre algum dos nodos, é gerado um evento e então
    #   este método é executado automaticamente, alterando as imagens para identificar
    #   o que será inicio e fim.
    def callback(self, event):
        info = event.widget.grid_info()
        linha = info['row']
        coluna = info['column']
        if self.tipo == 'start':
            self.tipo = 'end'
            self.star.define_inicio(linha,coluna)
            im = Image.open(os.path.join(self.path, 'start.jpg'))
            resized = im.resize((int(self.width), int(self.height)), Image.NEAREST)
            tkimage = ImageTk.PhotoImage(resized)
            myvar = Label(self.root, image=tkimage)
            myvar.image = tkimage
            myvar.grid(row=linha, column=coluna)
            self.root.update()
            d = MyDialog(self.root, self.tipo)
            self.root.wait_window(d.top)
        elif self.tipo == 'end':
            self.tipo = 'block'
            self.star.define_objetivo(linha,coluna)
            im = Image.open(os.path.join(self.path, 'end.jpg'))
            resized = im.resize((int(self.width), int(self.height)), Image.NEAREST)
            tkimage = ImageTk.PhotoImage(resized)
            myvar = Label(self.root, image=tkimage)
            myvar.image = tkimage
            myvar.grid(row=linha, column=coluna)



    ##  Método da classe
    #   @param linha Quantidade de linhas da matriz a ser gerada
    #   @param coluna Quantidade de colunas da matriz a ser gerada
    #   @brief Obtém o tamanho total do mapa, calcula com base na porcentagem
    #   passada pelo usuário a quantidade de nodos a serem bloqueados e gera o mapa escolhendo randomicamente
    #   os nodos a serem bloqueados.    
    def gera_mapa(self, linha, coluna):
        max_linhas = len(self.star.mapa.grade)
        max_colunas = len(self.star.mapa.grade[0])
        self.quantidade = math.floor((max_linhas*max_colunas-2)*self.porcentagem/100)
        self.root.title("Busca A*")
        grade = self.star.mapa.grade
        while self.quantidade > 0:
            nodo = random.choice(grade)[random.randrange(len(grade[0]))]
            linhab, colunab = self.star.mapa.obter_posicao(nodo)
            self.star.bloqueia_nodo(linhab,colunab)
            im = Image.open(os.path.join(self.path, 'block.jpg'))
            resized = im.resize((int(self.width), int(self.height)), Image.NEAREST)
            tkimage = ImageTk.PhotoImage(resized)
            myvar = Label(self.root, image=tkimage)
            myvar.image = tkimage
            myvar.grid(row=linhab, column=colunab)
            self.quantidade -= 1
        for r in range(linha):
            for c in range(coluna):
                if not grade[r][c].bloqueado:
                    im = Image.open(os.path.join(self.path, 'normal.jpg'))
                    resized = im.resize((int(self.width), int(self.height)), Image.NEAREST)
                    tkimage = ImageTk.PhotoImage(resized)
                    myvar = Label(self.root, image=tkimage)
                    myvar.image = tkimage
                    myvar.bind("<Button-1>", self.callback)
                    myvar.grid(row=r, column=c)

        botao = Button(self.root, text="Iniciar busca!", command=lambda:self.star.busca_solucao(self.root)).grid(row=max_linhas, columnspan=max_linhas, sticky=W)

        self.root.update()
        d = MyDialog(self.root, self.tipo)
        self.root.wait_window(d.top)

        self.root.mainloop()

##  Esta classe implementa as janelas de pop-up
class MyDialog:

    ##  Construtor da classe
    #   @brief Mostra as pop-ups para avisa o usuário como proceder
    def __init__(self, parent, tipo):
        top = self.top = Toplevel(parent)
        if tipo == 'start':
            Label(top, text="Escolha o nodo de inicio!").pack()
            b = Button(top, text="OK", command=self.ok)
            b.pack(pady=5)
        else:
            Label(top, text="Escolha o nodo objetivo!").pack()
            b = Button(top, text="OK", command=self.ok)
            b.pack(pady=5)
    ##  Método da classe
    #   @brief Apenas destroi o pop-up
    def ok(self):
        self.top.destroy()

if __name__ == "__main__":

    linha = int(input("insira a quantidade de linhas: "))
    coluna = int(input("insira a quantidade de colunas: "))
    porcentagem = int(input("insira o percentual de obstaculos: "))

    a = GUI(linha, coluna, porcentagem)
