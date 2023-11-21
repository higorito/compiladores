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

from lexico import AnalisadorLexico

class Node:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)


class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def parse(self):
        return self.main()

    def match(self, tipo_esperado):
        if self.posicao < len(self.tokens) and self.tokens[self.posicao]['tipo'] == tipo_esperado:
            self.posicao += 1
            return True
        return False

    def main(self):
        node = Node('main')
        if (
            self.match('Palavra Reservada')
            and self.match('main')
            and self.match('Palavra Reservada')
            and self.match('vacuum')
            and self.match('<')
            and self.lista_declaracao()
            and self.escopo()
            and self.match('>')
        ):
            return node
        return None

    def lista_declaracao(self):
        node = Node('ListaDeDeclaracao')
        child = self.declaracao()
        while self.match('|'):
            child = self.declaracao()
            if not child:
                return None
            node.add_child(child)
        return node

    def declaracao(self):
        tipo_var_node = self.tipo_var()
        variavel_node = self.variavel()

        if tipo_var_node and variavel_node and self.match(';'):
            node = Node('Declaracao')
            node.add_child(tipo_var_node)
            node.add_child(variavel_node)
            return node

        return None

    def tipo_var(self):
        return self.match('Palavra Reservada')

    def variavel(self):
        return self.match('Identificador')

    def escopo(self):
        node = Node('escopo')
        if self.match('Palavra Reservada'):
            child = self.lista_declaracao()
            if child:
                node.add_child(child)
                child = self.escopo()
                if child:
                    node.add_child(child)
                    return node
        elif self.lista_declaracao():
            return Node('ListaDeDeclaracao')
        return None
    
    def comando(self):
        if self.entrada() or self.saida() or self.desvio() or self.atribuicao() or self.laco():
            return True
        return False

    def entrada(self):
        if self.match('textin') and self.match('[') and self.variavel() and self.match(']'):
            return True
        return False

    def saida(self):
        if self.match('textout') and self.match('[') and (self.texto() or self.exp_aritmetica()) and self.match(']'):
            return True
        return False

    def exp_aritmetica(self):
        return self.exp() or self.termo()

    def desvio(self):
        if self.match('case') and self.match('(') and self.exp() and self.match(')') and self.match('<') and self.escopo() and self.match('>') and self.desvio2():
            return True
        return False

    def atribuicao(self):
        if self.variavel() and self.conteudo() and self.match(';'):
            return True
        return False

    def conteudo(self):
        return self.texto() or self.exp()

    def laco(self):
        if self.match('to') and self.match('(') and self.atribuicao() and self.conteudo() and self.simbolo_relacional() and self.conteudo() and self.match(';') and self.variavel() and self.match('<<') and self.exp_aritmetica() and self.match(')') and self.match('<') and self.escopo() and self.match('>'):
            return True
        elif self.match('when') and self.match('(') and self.exp() and self.match(')') and self.match('<') and self.escopo() and self.match('>'):
            return True
        elif self.match('take'):
            return True
        return False

    def exp(self):
        return self.logico() or self.match('ok') or self.match('notok')

    def logico(self):
        return self.expressao_logica() and self.termo_logico()

    def termo(self):
        return self.fator() and self.termo2()

    def termo2(self):
        if self.match('*') and self.fator() and self.termo2():
            return True
        elif self.match('/') and self.fator() and self.termo2():
            return True
        elif self.match('//') and self.fator() and self.termo2():
            return True
        return False

    def fator(self):
        if self.match('(') and self.exp_aritmetica() and self.match(')'):
            return True
        elif self.variavel() or self.numero() or self.funcao():
            return True
        return False

    def funcao(self):
        if self.match('Identificador') and self.match('(') and self.argumento() and self.match(')'):
            return True
        return False

    def argumento(self):
        return self.exp_aritmetica() and self.argumento2()

    def argumento2(self):
        if self.exp_aritmetica() and self.argumento2():
            return True
        return False

    def texto(self):
        return self.match('String')

    def termo_logico(self):
        if self.match('||') and self.expressao_logica() and self.termo_logico():
            return True
        return False

    def expressao_logica(self):
        return self.expressao_logica3() and self.expressao_logica2()

    def expressao_logica2(self):
        if self.match('&&') and self.expressao_logica3() and self.expressao_logica2():
            return True
        return False

    def expressao_logica3(self):
        if self.match('!') and self.relacional():
            return True
        elif self.relacional():
            return True
        return False

    def simbolo_relacional(self):
        return self.match('<<') or self.match('>>') or self.match('<<<') or self.match('>>>') or self.match('==') or self.match('!=') or self.match('ok') or self.match('notok')

    def desvio2(self):
        if self.case_not() and self.match('<') and self.escopo() and self.match('>'):
            return True
        elif self.case_not() and self.desvio3():
            return True
        return False

    def desvio3(self):
        if self.match('case') and self.match('(') and self.exp() and self.match(')') and self.match('<') and self.escopo() and self.match('>') and self.desvio2():
            return True
        return True

    def relacional(self):
        return self.logico() or self.termo_relacional()

    def termo_relacional(self):
        return self.conteudo() and self.termo_relacional2()

    def termo_relacional2(self):
        if self.simbolo_relacional() and self.conteudo():
            return True
        return False

    def case_not(self):
        return self.match('caseNot')
    
    def imprimir_arvore(self, node, nivel=0):
        if node:
            print('  ' * nivel + f'{node.label}')
            for child in node.children:
                self.imprimir_arvore(child, nivel + 1)

tokens_exemplo = [
    {'tipo': 'Palavra Reservada', 'lexema': 'main'},
    {'tipo': 'Palavra Reservada', 'lexema': 'num_int'},
    {'tipo': 'Identificador', 'lexema': 'x'},
    {'tipo': ';', 'lexema': ';'},
    {'tipo': 'vacuum', 'lexema': 'vacuum'},
    {'tipo': '<', 'lexema': '<'},
    {'tipo': 'Identificador', 'lexema': 'x'},
    {'tipo': '>', 'lexema': '>'},
]

analisador_sintatico = AnalisadorSintatico(tokens_exemplo)
arvore_sintatica = analisador_sintatico.parse()

if arvore_sintatica:
    print("Análise sintática bem-sucedida! Árvore sintática gerada:")
    analisador_sintatico.imprimir_arvore(arvore_sintatica)
else:
    print("Erro na análise sintática.")

if __name__ == "__main__":
    analisador_lexico = AnalisadorLexico("fibonacci.txt")
    tokens_controle_fluxo = analisador_lexico.get_tabela_simbolos()

    if tokens_controle_fluxo:
        print("Análise léxica bem-sucedida! Tokens gerados:")
        analisador_lexico.imprimir_tokens()
    else:
        print("Erro na análise léxica.")

    # Agora, vamos usar os tokens gerados na análise sintática
    analisador_sintatico = AnalisadorSintatico(tokens_controle_fluxo)
    arvore_sintatica_controle_fluxo = analisador_sintatico.parse()

    if arvore_sintatica_controle_fluxo:
        print("\nAnálise sintática bem-sucedida! Árvore sintática gerada:")
        analisador_sintatico.imprimir_arvore(arvore_sintatica_controle_fluxo)
    else:
        print("\nErro na análise sintática.")


