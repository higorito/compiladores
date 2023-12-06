class AnaliseSemantica:
    def __init__(self):
        self.variaveis = {}
        self.funcoes = {}
        self.resultado = None

    def analisar(self, no):
        self.analisar_no(no)

    def analisar_no(self, no):
        if no.tipo == 'DECLARACAO_VAR':
            self.declarar_variavel(no)
        elif no.tipo == 'FUNCAO':
            self.declarar_funcao(no)
        elif no.tipo == 'CHAMADA_FUNCAO':
            self.chamar_funcao(no)
        elif no.tipo == 'ATRIBUICAO':
            self.atribuir_valor(no)
        elif no.tipo == 'SAIDA':
            self.saida(no)

    def declarar_variavel(self, no):
        tipo = no.filhos[0].valor
        nome = no.filhos[1].valor
        valor = self.avaliar_expressao(no.filhos[2])

        # regras semânticas para a declaração de variáveis
        self.variaveis[nome] = {'tipo': tipo, 'valor': valor}

    def declarar_funcao(self, no):
        nome_funcao = no.filhos[0].valor
        parametros = no.filhos[1].filhos
        corpo_funcao = no.filhos[2].filhos

        # regras semânticas para a declaração de funções
        self.funcoes[nome_funcao] = {'parametros': parametros, 'corpo': corpo_funcao}

    def chamar_funcao(self, no):
        nome_funcao = no.filhos[0].valor
        argumentos = no.filhos[1].filhos

        #regras semânticas para a chamada de funções
        if nome_funcao in self.funcoes:
            #Avaliar a função e lidar com o retorno conforme necessário
            resultado_funcao = self.avaliar_funcao(nome_funcao, argumentos)
            self.resultado = resultado_funcao

    def atribuir_valor(self, no):
        nome_variavel = no.filhos[0].valor
        valor = self.avaliar_expressao(no.filhos[1])

        #regras semânticas para a atribuição de valores
        self.variaveis[nome_variavel]['valor'] = valor

    def saida(self, no):
        #regras semânticas para a saída
        print(f"Saida: {self.resultado}")

    def avaliar_expressao(self, no):
        #avaliação de expressões
    
        pass

    def avaliar_funcao(self, nome_funcao, argumentos):
        #avaliação de funções e retornar o resultado
        
        pass


class No:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.filhos = []

    def adicionar_filho(self, filho):
        self.filhos.append(filho)


def construir_arvore_sintatica():
    arvore_sintatica = No("main")
    arvore_sintatica.adicionar_filho(No("DECLARACAO_VAR", "a -> 5"))
    arvore_sintatica.adicionar_filho(No("DECLARACAO_VAR", "b -> 10"))

    atribuicao = No("ATRIBUICAO", "a -> a + b")
    atribuicao.adicionar_filho(No("VARIAVEL", "a"))
    expressao_aritmetica = No("EXPRESSAO_ARITMETICA", "+")
    expressao_aritmetica.adicionar_filho(No("VARIAVEL", "a"))
    expressao_aritmetica.adicionar_filho(No("VARIAVEL", "b"))
    atribuicao.adicionar_filho(expressao_aritmetica)
    arvore_sintatica.adicionar_filho(atribuicao)

    saida = No("SAIDA", "puts<a>")
    saida.adicionar_filho(No("VARIAVEL", "a"))
    arvore_sintatica.adicionar_filho(saida)

    return arvore_sintatica


def main():
    arvore_sintatica_exemplo = construir_arvore_sintatica()

    analisador_semantico = AnaliseSemantica()
    analisador_semantico.analisar(arvore_sintatica_exemplo)

    imprimir_arvore(arvore_sintatica_exemplo)


def imprimir_arvore(no, prefixo=""):
    print(f"{prefixo}-- {no.tipo} ({no.valor})")
    for filho in no.filhos:
        imprimir_arvore(filho, prefixo + "|   ")


if __name__ == "__main__":
    main()
