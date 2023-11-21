#### GRAMÁTICA ###

# Início
# main  ListaDeDeclaração  < escopo >

# Lista De Declaração
# ListaDeDeclaração | declaração | vacuum

# Declaração
# tipoVar variavel ;

# TipoVar
# text | numero 

# Número
# num_int | num_flu

# Variável 
# ID

# Escopo 
# escopo | comando | ε

# Comando 
# entrada | saida | desvio | atribuicao | laco

# Entrada
# textin [ variavel ]

# Saída
# textout [ texto | expAritmetica ]

# Exp Aritmética 
# exp | termo

# Desvio 
# case( exp ) < escopo > desvio2

# Atribuição
# variavel conteudo ;

# Conteúdo
# texto | exp

# Laço
# to( atribuicao conteudo simbolo_relacional conteudo ; variavel << expAritmetica ) < escopo > | when( exp ) < escopo > | take;

# Exp
# logico | ok | notok

# Lógico
# expressãoLogica termo logico

# Termo
# fator termo2

# Termo2
# *fator termo2 | / fator termo2 | // fator termo2 | ε

# Fator
# ( expAritmetica ) | variavel | numero | função

# Função
# ID ( argumento )

# Argumento
# expAritmetica argumento2 | ε

# Argumento2
# expAritmetica argumento2 | ε

# Texto
# text

# Termo lógico
# || expressaoLogica termoLogico | ε

# Expressão Lógica
# expressaoLogica3 expressaoLogica2

# Expressão Lógica2
# && expressaoLogica3 expressaoLogica2 | ε

# Expressão Lógica3
# ! relacional | relacional

# Simbolo_relacional
# << | >> | <<< | >>> | == | != | ok | notok

# Desvio2
# caseNot < escopo > | caseNot desvio3

# Desvio3
# case ( exp ) < escopo > desvio2 | ε

# Relacional
# logico | termoRelacional

# TermoRelacional
# conteudo termoRelacional2

# TermoRelacional2
# simbolo_relacional conteudo | ε



from python.lexico import AnalisadorLexico

class No:
    def __init__(self, tipo, lexema=None):
        self.tipo = tipo
        self.lexema = lexema
        self.filhos = []

    def adicionar_filho(self, filho):
        self.filhos.append(filho)

    def imprimir_arvore(self, nivel=0):
        print("  " * nivel + f"{self.tipo}: {self.lexema}")
        for filho in self.filhos:
            filho.imprimir_arvore(nivel + 1)

class AnalisadorSintatico:
    def __init__(self, path):
        self.analisador_lexico = AnalisadorLexico(path)
        self.tokens = self.analisador_lexico.get_tabela_simbolos()
        self.indice_token_atual = 0
        self.raiz = No('Programa')

    def match(self, tipo_esperado):
        if self.indice_token_atual < len(self.tokens):
            tipo_token_atual = self.tokens[self.indice_token_atual]['tipo']
            lexema_token_atual = self.tokens[self.indice_token_atual]['lexema']
            if tipo_token_atual == tipo_esperado:
                no_token = No(tipo_token_atual, lexema_token_atual)
                self.indice_token_atual += 1
                return no_token
            else:
                raise SyntaxError(f"Token inesperado {tipo_token_atual} na linha {self.tokens[self.indice_token_atual]['linha']}")

    def analisar_programa(self):
        try:
            self.analisar_escopo(self.raiz)
            print("\nAnálise dos tokens concluída com sucesso.")
        except SyntaxError as e:
            print(e)

        except SyntaxError as e:
            print(e)

    def analisar_programa(self):
        try:
            self.analisar_escopo(self.raiz)
            print("\nAnálise dos tokens concluída com sucesso.")
        except SyntaxError as e:
            print(e)



    def analisar_escopo(self, no_pai):
        no_escopo = No('Escopo')
        try:
            while self.indice_token_atual < len(self.tokens):
                token = self.tokens[self.indice_token_atual]['tipo']
                if token in ('num_int', 'num_flu', 'text', 'bool'):
                    no_escopo.adicionar_filho(self.analisar_declaracao())
                elif token == 'vacuum':
                    no_escopo.adicionar_filho(self.match('Palavra Reservada'))  # 'vacuum'
                elif token == 'case':
                    no_escopo.adicionar_filho(self.analisar_desvio())
                elif token == 'ordo':
                    no_escopo.adicionar_filho(self.analisar_ordo())
                elif token == 'take':
                    no_escopo.adicionar_filho(self.match('Palavra Reservada'))  # 'take'
                    no_escopo.adicionar_filho(self.match('Num Inteiro'))  # '0'
                    self.match('Caractere Especial')  # ';'
                else:
                    raise SyntaxError(f"Token inesperado {token} na linha {self.tokens[self.indice_token_atual]['linha']}")

            no_pai.adicionar_filho(no_escopo)

        except SyntaxError as e:
            print(e)

    def analisar_ordo(self):
        no_ordo = No('Ordo')
        no_ordo.adicionar_filho(self.match('Palavra Reservada'))  # 'ordo'
        self.analisar_escopo(no_ordo)
        return no_ordo

    def analisar_declaracao(self):
        no_declaracao = No('Declaracao')
        tipo_variavel = self.match('Palavra Reservada')
        identificador = self.match('Identificador')
        self.match('Caractere Especial')  # ';'

        no_declaracao.adicionar_filho(tipo_variavel)
        no_declaracao.adicionar_filho(identificador)
        return no_declaracao

    def analisar_desvio(self):
        no_desvio = No('Desvio')
        no_desvio.adicionar_filho(self.match('Palavra Reservada'))  # 'case'
        no_desvio.adicionar_filho(self.match('Caractere Especial'))  # '['     
        self.analisar_exp_relacional(no_desvio)
        no_desvio.adicionar_filho(self.match('Caractere Especial'))  # ']'
        no_desvio.adicionar_filho(self.match('Caractere Especial'))  # '<'
        self.analisar_escopo(no_desvio)
        no_desvio.adicionar_filho(self.match('Caractere Especial'))  # '>'

        self.analisar_desvio2(no_desvio)

        return no_desvio

    def analisar_exp_relacional(self, no_pai):
        no_exp_relacional = No('ExpRelacional')

        # Analisar a parte esquerda da expressão relacional
        no_exp_relacional.adicionar_filho(self.analisar_termo())

        # Analisar o operador relacional (pode haver vários operadores)
        while self.tokens[self.indice_token_atual]['tipo'] == 'Operador Relacional':
            operador = self.match('Operador Relacional')
            # Adiciona o operador à árvore
            no_exp_relacional.adicionar_filho(operador)

            # Analisar a parte direita da expressão relacional
            no_exp_relacional.adicionar_filho(self.analisar_termo())

        no_pai.adicionar_filho(no_exp_relacional)

    def analisar_termo(self):
        # Implemente a lógica para analisar um termo (pode ser um fator ou uma expressão)
        # Vou fornecer uma implementação básica para termo que considera apenas um fator
        no_termo = No('Termo')
        no_termo.adicionar_filho(self.analisar_fator())
        return no_termo
    
    def analisar_fator(self):
        # Implemente a lógica para analisar um fator (pode ser um identificador, número, etc.)
        no_fator = No('Fator')

        if self.tokens[self.indice_token_atual]['tipo'] == 'Identificador':
            no_fator.adicionar_filho(self.match('Identificador'))
        elif self.tokens[self.indice_token_atual]['tipo'] == 'Num Inteiro':
            no_fator.adicionar_filho(self.match('Num Inteiro'))
        elif self.tokens[self.indice_token_atual]['tipo'] == 'Num Flutuante':
            no_fator.adicionar_filho(self.match('Num Flutuante'))
        else:
            raise SyntaxError(f"Token inesperado {self.tokens[self.indice_token_atual]['tipo']} na linha {self.tokens[self.indice_token_atual]['linha']}")

        return no_fator
    
    def analisar_desvio2(self, no_pai):
        no_desvio2 = No('Desvio2')
        while self.indice_token_atual < len(self.tokens):
            token = self.tokens[self.indice_token_atual]['tipo']
            if token == 'Palavra Reservada' and self.tokens[self.indice_token_atual]['lexema'] == 'case':
                no_desvio2.adicionar_filho(self.analisar_desvio())
            else:
                return  # ε

        no_pai.adicionar_filho(no_desvio2)

def imprimir_arvore_sintatica(no, nivel=0, lado=None):
    if no.lexema is not None:
        if nivel > 0:
            prefixo = "|   " * (nivel - 1) + "+--"
        else:
            prefixo = ""
        print(f"{prefixo} {no.tipo}: {no.lexema} ({lado})")
    else:
        print(" " * nivel + f"{no.tipo}")

    for i, filho in enumerate(no.filhos):
        novo_lado = None
        if i == len(no.filhos) - 1:
            novo_lado = "D"
        elif i == 0:
            novo_lado = "E"

        imprimir_arvore_sintatica(filho, nivel + 1, lado=novo_lado)

def main():
    path = "controlefluxo.txt"
    analisador_sintatico = AnalisadorSintatico(path)
    analisador_sintatico.analisar_programa()

    # Chamada para imprimir a árvore sintática
    print("\nÁrvore Sintática:")
    imprimir_arvore_sintatica(analisador_sintatico.raiz)

if __name__ == "__main__":
    main()