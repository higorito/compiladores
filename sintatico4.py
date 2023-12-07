# GRAMÁTICA PARA ANALISADOR SINTÁTICO

# Início
# main | ListaDeDeclaracao

# Lista de Declaração
# ListaDeDeclaracao | Declaracao | ε

# Declaração
# TipoVar Variavel ;

# TipoVar
# text | numero 

# Variável 
# ID

# Comentários
# -- .* \n

# Strings
# ".*"

# Números
# num_int | num_flu

# Palavras Reservadas
# main | vacuum | num_int | num_flu | text

# Operadores Aritméticos
# + | - | * | / | // | **

# Operadores Relacionais
# == | != | >= | <= | >> | <<

# Operadores Lógicos
# && | || | !

# Símbolos Especiais
# < | > | ; | [ | ]

# Atribuição
# ID => | ->

# Ignorar espaços em branco
# \s

from lexico import AnalisadorLexico

#classe para representar um nó na árvore sintática
class Node:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)

#classe para realizar a análise sintática
class AnalisadorSintatico:
    def __init__(self):
        self.tokens = []       #lista de tokens
        self.posicao = 0        #posição atual na lista de tokens

    #função principal que inicia a análise sintática
    def parse(self, tokens):
        self.tokens = tokens
        self.erro_encontrado = False
        self.erro_tipo = None
        return self.main()

    #função para verificar se o token atual corresponde ao tipo esperado
    def match(self, tipo_esperado):
        if self.posicao < len(self.tokens):
            token_atual = self.tokens[self.posicao]

            if token_atual['tipo'] == tipo_esperado:
                self.posicao += 1
                return token_atual['lexema']
        #     else:
        #         # Adicionando mensagem de erro
        #         self.erro_encontrado = True
        #         self.erro_tipo = f"Erro sintático: esperado {tipo_esperado}, encontrado {token_atual['tipo']} ({token_atual['lexema']})"
        #         return None
        # return None

    #imprimindo a cabeça da árvore
    def main1(self):
        node1 = Node('INICIO DA ÁRVORE')
        return node1




    #função principal que representa a regra gramatical <main>
    def main(self):
        root = self.main1()  # Obtém o nó da função main1 como a raiz da árvore
        node = Node('PALAVRA_RESERVADA')  # cria um nó para representar a regra <main>

        lexema = self.match('PALAVRA_RESERVADA')

        # enquanto houver correspondência, adiciona o lexema como filho
        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('PALAVRA_RESERVADA')  # Avança para o próximo lexema após a correspondência

        # tenta corresponder às declarações (ListaDeDeclaracao)
        declaracoes = self.lista_declaracao()
        if declaracoes:
            node.add_child(declaracoes)

        # tenta corresponder ao escopo
        escopo = self.escopo()
        if escopo:
            node.add_child(escopo)

        # tenta corresponder à função sim_especial
        especial = self.sim_especial()
        if especial:
            node.add_child(especial)
    
        return node
         
        
    def sim_especial(self):
        node = Node('                   SIM_ESPECIAL:')  # Cria um nó para representar o símbolo especial
        lexema = self.match('SIM_ESPECIAL')

        while lexema:
            # Adiciona o lexema como filho do nó 'SIM_ESPECIAL'
            node.add_child(Node(lexema))
            lexema = self.match('SIM_ESPECIAL')

        # Adiciona as declarações e o escopo como filhos do nó 'SIM_ESPECIAL'
        declaracoes = self.lista_declaracao()
        if declaracoes:
            node.add_child(declaracoes)

        escopo = self.escopo()
        if escopo:
            node.add_child(escopo)

        return node

    #função para corresponder à regra gramatical <ListaDeDeclaracao>
    def lista_declaracao(self):
        node = Node('')
        child = self.declaracao()

        #enquanto houver correspondência com '|', continua adicionando declarações
        while self.match('|'):
            if not child:
                return None
            node.add_child(child)
            child = self.declaracao()
        return node

    #função para corresponder à regra gramatical <Declaracao>
    def declaracao(self):
        tipo_var_node = self.tipo_var()
        variavel_node = self.variavel()

        #se todas as partes da declaração corresponderem, cria um nó para representar a declaração
        if tipo_var_node and variavel_node and self.match(';'):
            node = Node('Declaracao')
            node.add_child(tipo_var_node)
            node.add_child(variavel_node)
            return node

        return None

    #função para corresponder à regra gramatical <TipoVar>
    def tipo_var(self):
        if self.posicao < len(self.tokens):
            token_atual = self.tokens[self.posicao]

            # lista de tipos permitidos
            tipos_permitidos = ['PALAVRA_RESERVADA', 'SIM_ESPECIAL']

            # mensagem de debug para exibir o tipo esperado e o token atual
            print(f"debug: tipo_esperado = {tipos_permitidos}, token_atual = {token_atual['lexema']}")

            # verifica se o tipo do token atual está na lista de tipos permitidos
            if token_atual['tipo'] in tipos_permitidos:
                self.posicao += 1
                return True

        return False

    #função para corresponder à regra gramatical <Variavel>
    def variavel(self):
        return self.match('IDENTIFICADOR')

    #função para corresponder à regra gramatical <Escopo>
    def escopo(self):
        node = Node('Escopo')

        # tenta corresponder à regra <escopo>
        if self.match('PALAVRA_RESERVADA') or self.match('SIM_ESPECIAL'):
            child = self.lista_declaracao()

            # se houver correspondência com a lista de declarações, tenta corresponder ao escopo novamente
            if child:
                node.add_child(child)
                child = self.escopo()
                if child:
                    node.add_child(child)
                    return node
        # se não houver correspondência com <escopo>, verifica se há correspondência com <ListaDeDeclaracao>
        elif self.lista_declaracao():
            return Node('')

        return None

    #função para corresponder à regra gramatical <Comando>
    def comando(self):
        if self.entrada() or self.saida() or self.desvio() or self.atribuicao() or self.laco():
            return True
        return False

    #função para corresponder à regra gramatical <Entrada>
    def entrada(self):
        if self.match('textin') and self.match('[') and self.variavel() and self.match(']'):
            return Node('Entrada')
        return None

    #função para corresponder à regra gramatical <Saida>
    def saida(self):
        if self.match('textout') and self.match('[') and (self.texto() or self.exp_aritmetica()) and self.match(']'):
            return Node('Saida')
        return None

    #função para corresponder à regra gramatical <ExpAritmetica>
    def exp_aritmetica(self):
        return self.exp() or self.termo()

    #função para corresponder à regra gramatical <Desvio>
    def desvio(self):
        if self.match('case') and self.match('(') and self.exp() and self.match(')') and self.match('<') and self.escopo() and self.match('>') and self.desvio2():
            return Node('Desvio')
        return None

    #função para corresponder à regra gramatical <Atribuicao>
    def atribuicao(self):
        if self.variavel() and self.conteudo() and self.match(';'):
            return Node('Atribuicao')
        return None

    #função para corresponder à regra gramatical <Conteudo>
    def conteudo(self):
        return self.texto() or self.exp()

    #função para corresponder à regra gramatical <Laco>
    def laco(self):
        if self.match('to') and self.match('(') and self.atribuicao() and self.conteudo() and self.simbolo_relacional() and self.conteudo() and self.match(';') and self.variavel() and self.match('<<') and self.exp_aritmetica() and self.match(')') and self.match('<') and self.escopo() and self.match('>'):
            return Node('LacoTo')
        elif self.match('when') and self.match('(') and self.exp() and self.match(')') and self.match('<') and self.escopo() and self.match('>'):
            return Node('LacoWhen')
        elif self.match('take'):
            return Node('Take')
        return None

    #função para corresponder à regra gramatical <Exp>
    def exp(self):
        return self.logico() or self.match('ok') or self.match('notok')

    #função para corresponder à regra gramatical <Logico>
    def logico(self):
        return self.expressao_logica() and self.termo_logico()

    #função para corresponder à regra gramatical <Termo>
    def termo(self):
        return self.fator() and self.termo2()

    #função para corresponder à regra gramatical <Termo2>
    def termo2(self):
        if self.match('*') and self.fator() and self.termo2():
            return Node('Multiplicacao')
        elif self.match('/') and self.fator() and self.termo2():
            return Node('Divisao')
        elif self.match('//') and self.fator() and self.termo2():
            return Node('DivisaoInteira')
        return None

    #função para corresponder à regra gramatical <Fator>
    def fator(self):
        if self.match('(') and self.exp_aritmetica() and self.match(')'):
            return Node('ExpressaoAritmetica')
        elif self.variavel() or self.numero() or self.funcao():
            return Node('Fator')
        return None

    #função para corresponder à regra gramatical <Funcao>
    def funcao(self):
        if self.match('Identificador') and self.match('(') and self.argumento() and self.match(')'):
            return Node('Funcao')
        return None

    #função para corresponder à regra gramatical <Argumento>
    def argumento(self):
        return self.exp_aritmetica() and self.argumento2()

    #função para corresponder à regra gramatical <Argumento2>
    def argumento2(self):
        if self.exp_aritmetica() and self.argumento2():
            return Node('Argumento')
        return None

    #função para corresponder à regra gramatical <Texto>
    def texto(self):
        return self.match('String')

    #função para corresponder à regra gramatical <TermoLogico>
    def termo_logico(self):
        if self.match('||') and self.expressao_logica() and self.termo_logico():
            return Node('OULogico')
        return None

    #função para corresponder à regra gramatical <ExpressaoLogica>
    def expressao_logica(self):
        return self.expressao_logica3() and self.expressao_logica2()

    #função para corresponder à regra gramatical <ExpressaoLogica2>
    def expressao_logica2(self):
        if self.match('&&') and self.expressao_logica3() and self.expressao_logica2():
            return Node('ELogico')
        return None

    #função para corresponder à regra gramatical <ExpressaoLogica3>
    def expressao_logica3(self):
        if self.match('!') and self.relacional():
            return Node('NaoLogico')
        elif self.relacional():
            return Node('ExpressaoRelacional')
        return None

    #função para corresponder à regra gramatical <SimboloRelacional>
    def simbolo_relacional(self):
        return (
            self.match('<<') or self.match('>>') or
            self.match('<<<') or self.match('>>>') or
            self.match('==') or self.match('!=') or
            self.match('ok') or self.match('notok')
        )

    #função para corresponder à regra gramatical <Desvio2>
    def desvio2(self):
        if self.case_not() and self.match('<') and self.escopo() and self.match('>'):
            return Node('CaseNot')
        elif self.case_not() and self.desvio3():
            return Node('CaseNotDesvio3')
        return None

    #função para corresponder à regra gramatical <Desvio3>
    def desvio3(self):
        if self.case_not() and self.match('<') and self.escopo() and self.match('>'):
            return Node('CaseNot')
        elif self.match('case') and self.match('(') and self.exp() and self.match(')') and self.match('<') and self.escopo() and self.match('>') and self.desvio2():
            return Node('CaseDesvio2')
        return None

    #função para corresponder à regra gramatical <Relacional>
    def relacional(self):
        return self.termo_relacional() or self.logico()

    #função para corresponder à regra gramatical <TermoRelacional>
    def termo_relacional(self):
        return self.conteudo() and self.termo_relacional2()

    #função para corresponder à regra gramatical <TermoRelacional2>
    def termo_relacional2(self):
        if self.simbolo_relacional() and self.conteudo():
            return Node('TermoRelacional')
        return None

    #função para corresponder à regra gramatical <CaseNot>
    def case_not(self):
        return self.match('caseNot')

    #função para corresponder à regra gramatical <Numero>
    def numero(self):
        return self.match('Numero')

    #função para imprimir a árvore sintática de forma recursiva
    def imprimir_arvore(self, node, nivel=0, tipo_esperado=None):
        if node:
            if not node.children:
                # é um nó folha, exibe o tipo esperado e o lexema (se houver)
                lexema = node.label if node.label else ""
                tipo = f"{tipo_esperado}: {lexema}" if tipo_esperado else lexema
                print('  ' * nivel + f'{tipo}')
            else:
                # é um nó interno, exibe o rótulo da regra gramatical
                print('  ' * nivel + f'{node.label}')

                for child in node.children:
                    # passa o tipo esperado do pai para os filhos
                    self.imprimir_arvore(child, nivel + 1, tipo_esperado=node.label if tipo_esperado is None else tipo_esperado)




if __name__ == "__main__":
    analisador_lexico = AnalisadorLexico("teste.txt")
    tokens_controle_fluxo = analisador_lexico.get_tabela_simbolos()

    if tokens_controle_fluxo:
        print("Análise léxica bem-sucedida! Tokens gerados:")
        analisador_lexico.imprimir_tokens()
    else:
        print("Erro na análise léxica.")
        exit()  #saia do programa se houver erro léxico

    # Análise sintática
    analisador_sintatico = AnalisadorSintatico()
    arvore_sintatica_controle_fluxo = analisador_sintatico.parse(tokens_controle_fluxo)

    if not analisador_sintatico.erro_encontrado:
        print("\nAnálise sintática bem-sucedida! Árvore sintática gerada:")
        analisador_sintatico.imprimir_arvore(arvore_sintatica_controle_fluxo)
    else:
        print(f"\n{analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")
