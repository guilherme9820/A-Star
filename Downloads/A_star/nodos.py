##   Esta classe detém os valores de cada nodo do mapa
class Nodo(object):

    ##  Construtor da classe
    def __init__(self):
        ##  @var nodo_pai
        #   @brief Guarda a referência para o nodo pai
        self.nodo_pai = None
        ##  @var bloqueado
        #   @brief Identifica se um nodo está bloqueado ou não
        self.bloqueado = False
        ##  @var objetivo
        #   @brief Identifica se um nodo é o nodo objetivo
        self.objetivo = False
        ##  @var inicio
        #   @brief Identifica se um nodo é o nodo de inicio
        self.inicio = False
        ##  @var g
        #   @brief Corresponde ao valor da função de custo (g(x))
        self.g = 0
        ##  @var h
        #   @brief Corresponde ao valor da função heurística (h(x))
        self.h = 0
        ##  @var f
        ##  @brief Corresponde ao valor da função de custo total (f(x) = g(x) + h(x))
        self.f = 0