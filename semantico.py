from sintatico2 import AnalisadorSintatico, No

class AnalisadorSemantico:
    def __init__(self, analisador_sintatico):
        self.analisador_sintatico = analisador_sintatico
        self.tabela_simbolos = {}
        self.analisar()

    def analisar(self):
        raiz = self.analisador_sintatico.analisar_programa()
        self.analisar_programa(raiz)

    def analisar_programa(self, no_programa):
        if no_programa is not None:
            for filho in no_programa.filhos:
                if filho.tipo == 'Declaracao':
                    self.analisar_declaracao(filho)
                elif filho.tipo == 'Escopo':
                    self.analisar_escopo(filho)

    def analisar_declaracao(self, no_declaracao):
        tipo_variavel = no_declaracao.filhos[0].lexema
        identificador = no_declaracao.filhos[1].lexema

        if identificador in self.tabela_simbolos:
            raise Exception(f"Erro semântico: Variável '{identificador}' já foi declarada.")

        self.tabela_simbolos[identificador] = {'tipo': tipo_variavel}

    def analisar_escopo(self, no_escopo):
        if no_escopo is not None:
            for filho in no_escopo.filhos:
                if filho.tipo == 'Atribuicao':
                    self.analisar_atribuicao(filho)
                elif filho.tipo == 'Expressao':
                    self.analisar_expressao(filho)
                elif filho.tipo == 'Laco':
                    self.analisar_laco(filho)

    def analisar_atribuicao(self, no_atribuicao):
        identificador = no_atribuicao.filhos[0].lexema
        expressao = no_atribuicao.filhos[1]

        if identificador not in self.tabela_simbolos:
            raise Exception(f"Erro semântico: Variável '{identificador}' não foi declarada.")

        tipo_variavel = self.tabela_simbolos[identificador]['tipo']
        tipo_expressao = self.analisar_expressao(expressao)

        if tipo_variavel != tipo_expressao:
            raise Exception(f"Erro semântico: Atribuição de tipo '{tipo_expressao}' a uma variável do tipo '{tipo_variavel}'.")

    def analisar_expressao(self, no_expressao):
        # Implemente a análise semântica da expressão aqui
        pass

    def analisar_laco(self, no_laco):
        # Implemente a análise semântica do laço aqui
        pass

def main():
    path = "teste.txt"
    analisador_sintatico = AnalisadorSintatico(path)
    analisador_semantico = AnalisadorSemantico(analisador_sintatico)
    print("Análise semântica concluída com sucesso.")

if __name__ == "__main__":
    main()
