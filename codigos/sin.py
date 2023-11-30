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
# to( atribuicao conteudo simbolo_relacional conteudo ; variavel simbolo_relacional expAritmetica ) < escopo > | when( exp ) < escopo > | take;

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
        if self.posicao < len(self.tokens):
            tipo_token, lexema, _ = self.tokens[self.posicao]

            if tipo_token == tipo_esperado:
                print(f'Match bem-sucedido: {tipo_esperado} ({lexema})')
                return True, lexema
            else:
                print(f'Erro de match: esperado {tipo_esperado}, mas obtido {tipo_token} ({lexema})')
        else:
            print('Erro de match: final dos tokens alcançado')
        return False, None

    def main(self):
        node = Node('main')
        inicio_posicao = self.posicao  # Salva a posição inicial

        if (
            self.match('PALAVRA_RESERVADA')
            and self.match('main')
            and self.match('PALAVRA_RESERVADA')
            and self.match('vacuum')
            and self.match('SIM_ESPECIAL')
            and self.lista_declaracao()
            and self.escopo()
            and self.match('SIM_ESPECIAL')
        ):
            return node
        else:
            print('Erro na regra principal, reiniciando análise...')
            self.posicao = inicio_posicao  # Reinicia a posição
            return None

    def lista_declaracao(self):
        node = Node('ListaDeDeclaracao')
        child = self.declaracao()
        while self.match('|'):
            if not child:
                return None
            node.add_child(child)
            child = self.declaracao()
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
        return self.match('PALAVRA_RESERVADA')

    def variavel(self):
        return self.match('IDENTIFICADOR')

    def escopo(self):
        node = Node('escopo')
        if self.match('PALAVRA_RESERVADA'):
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
            return Node('Entrada')
        return None

    def saida(self):
        if self.match('textout') and self.match('[') and (self.texto() or self.exp_aritmetica()) and self.match(']'):
            return Node('Saida')
        return None

    def exp_aritmetica(self):
        return self.exp() or self.termo()

    def desvio(self):
        if self.match('case') and self.match('(') and self.exp() and self.match(')') and self.match('<') and self.escopo() and self.match('>') and self.desvio2():
            return Node('Desvio')
        return None

    def atribuicao(self):
        if self.variavel() and self.conteudo() and self.match(';'):
            return Node('Atribuicao')
        return None

    def conteudo(self):
        return self.texto() or self.exp()

    def laco(self):
        if self.match('to') and self.match('(') and self.atribuicao() and self.conteudo() and self.simbolo_relacional() and self.conteudo() and self.match(';') and self.variavel() and self.match('<<') and self.exp_aritmetica() and self.match(')') and self.match('<') and self.escopo() and self.match('>'):
            return Node('LacoTo')
        elif self.match('when') and self.match('(') and self.exp() and self.match(')') and self.match('<') and self.escopo() and self.match('>'):
            return Node('LacoWhen')
        elif self.match('take'):
            return Node('Take')
        return None

    def exp(self):
        return self.logico() or self.match('ok') or self.match('notok')

    def logico(self):
        return self.expressao_logica() and self.termo_logico()

    def termo(self):
        return self.fator() and self.termo2()

    def termo2(self):
        if self.match('*') and self.fator() and self.termo2():
            return Node('Multiplicacao')
        elif self.match('/') and self.fator() and self.termo2():
            return Node('Divisao')
        elif self.match('//') and self.fator() and self.termo2():
            return Node('DivisaoInteira')
        return None

    def fator(self):
        if self.match('(') and self.exp_aritmetica() and self.match(')'):
            return Node('ExpressaoAritmetica')
        elif self.variavel() or self.numero() or self.funcao():
            return Node('Fator')
        return None

    def funcao(self):
        if self.match('IDENTIFICADOR') and self.match('(') and self.argumento() and self.match(')'):
            return Node('Funcao')
        return None

    def argumento(self):
        return self.exp_aritmetica() and self.argumento2()

    def argumento2(self):
        if self.exp_aritmetica() and self.argumento2():
            return Node('Argumento')
        return None

    def texto(self):
        return self.match('String')

    def termo_logico(self):
        if self.match('||') and self.expressao_logica() and self.termo_logico():
            return Node('OULogico')
        return None

    def expressao_logica(self):
        return self.expressao_logica3() and self.expressao_logica2()

    def expressao_logica2(self):
        if self.match('&&') and self.expressao_logica3() and self.expressao_logica2():
            return Node('ELogico')
        return None

    def expressao_logica3(self):
        if self.match('!') and self.relacional():
            return Node('NaoLogico')
        elif self.relacional():
            return Node('ExpressaoRelacional')
        return None

    def simbolo_relacional(self):
        return (
            self.match('<<') or self.match('>>') or
            self.match('<<<') or self.match('>>>') or
            self.match('==') or self.match('!=') or
            self.match('ok') or self.match('notok')
        )

    def desvio2(self):
        if self.case_not() and self.match('<') and self.escopo() and self.match('>'):
            return Node('CaseNot')
        elif self.case_not() and self.desvio3():
            return Node('CaseNotDesvio3')
        return None

    def desvio3(self):
        if self.match('case') and self.match('(') and self.exp() and self.match(')') and self.match('<') and self.escopo() and self.match('>') and self.desvio2():
            return Node('CaseDesvio2')
        return None

    def relacional(self):
        return self.logico() or self.termo_relacional()

    def termo_relacional(self):
        return self.conteudo() and self.termo_relacional2()

    def termo_relacional2(self):
        if self.simbolo_relacional() and self.conteudo():
            return Node('TermoRelacional')
        return None

    def case_not(self):
        return self.match('caseNot')

    def numero(self):
        return self.match('Numero')

    def imprimir_arvore(self, node, nivel=0):
        if node:
            lexema = self.tokens[node.posicao - 1]['lexema']
            tipo = self.tokens[node.posicao - 1]['tipo']
            print('  ' * nivel + f'{node.label} ({tipo}: {lexema})')

            for child in node.children:
                self.imprimir_arvore(child, nivel + 1)

# Tokens de exemplo
tokens_exemplo = [
    {'PALAVRA_RESERVADA', 'main', 'Linha 1'},
    {'PALAVRA_RESERVADA', 'vacuum', 'Linha 1'},
    {'SIM_ESPECIAL', '<', 'Linha 1'},
]

analisador_sintatico = AnalisadorSintatico(tokens_exemplo)
arvore_sintatica = analisador_sintatico.parse()

if arvore_sintatica:
    print("Análise sintática bem-sucedida! Árvore sintática gerada:")
    analisador_sintatico.imprimir_arvore(arvore_sintatica)
else:
    print("Erro na análise sintática.")

if __name__ == "__main__":
    analisador_lexico = AnalisadorLexico("cod.txt")
    tokens_controle_fluxo = analisador_lexico.get_tabela_simbolos()

    if tokens_controle_fluxo:
        print("Análise léxica bem-sucedida! Tokens gerados:")
        analisador_lexico.imprimir_tokens()
    else:
        print("Erro na análise léxica.")

    # Análise sintática
    analisador_sintatico = AnalisadorSintatico(tokens_controle_fluxo)
    arvore_sintatica_controle_fluxo = analisador_sintatico.parse()

    if arvore_sintatica_controle_fluxo:
        print("\nAnálise sintática bem-sucedida! Árvore sintática gerada:")
        analisador_sintatico.imprimir_arvore(arvore_sintatica_controle_fluxo)
    else:
        print("\nErro na análise sintática.")
