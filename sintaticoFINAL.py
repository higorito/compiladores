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
        self.tokens = []        #lista de tokens
        self.posicao = 0        #posição atual na lista de tokens

    #função principal que inicia a análise sintática
    def parse(self, tokens):
        self.tokens = tokens
        self.posicao = 0
        self.erro_encontrado = False
        self.erro_tipo = None

    #chama a função para processar todos os tokens
        arvore_sintatica = self.processar_todos_tokens()

        return arvore_sintatica

    def processar_todos_tokens(self):

        
        #inicializa o nó principal
        node = Node('')

        #processa cada token até o final da lista
        while self.posicao < len(self.tokens):
            token_atual = self.tokens[self.posicao]

            #verifica o tipo do token atual e chama a função correspondente
            if token_atual['tipo'] == 'PALAVRA_RESERVADA':
                node.add_child(self.palavra_reservada())
            elif token_atual['tipo'] == 'SIM_ESPECIAL':
                node.add_child(self.sim_especial())
            elif token_atual['tipo'] == 'OP_ARITMETICO':
                node.add_child(self.op_aritmetico())
            elif token_atual['tipo'] == 'OP_RELACIONAL':
                node.add_child(self.op_relacional())
            elif token_atual['tipo'] == 'OP_LOGICO':
                node.add_child(self.op_logico())
            elif token_atual['tipo'] == 'IDENTIFICADOR':
                node.add_child(self.identificador())
            elif token_atual['tipo'] == 'ATRIBUICAO':
                node.add_child(self.atribuicao())
            elif token_atual['tipo'] == 'LISTADEDECLARACAO':
                node.add_child(self.lista_declaracao())
            elif token_atual['tipo'] == 'TEXT':
                node.add_child(self.text())
            elif token_atual['tipo'] == 'NUM_INT':
                node.add_child(self.num_int())
            elif token_atual['tipo'] == 'NUM_FLU':
                node.add_child(self.num_flu())
            else:
                #trata outros tipos de tokens conforme necessário
                self.posicao += 1  #avança para o próximo token

        return node
        

    #função para verificar se o token atual corresponde ao tipo esperado
    def match(self, tipo_esperado):
        if self.posicao < len(self.tokens):
            token_atual = self.tokens[self.posicao]

            if token_atual['tipo'] == tipo_esperado:
                self.posicao += 1
                return token_atual['lexema']
       

    #   APLICAÇÃO DAS FUNÇÕES
    #          'OP_ARITMETICO', 'OP_RELACIONAL', 
    #         'OP_LOGICO', 'SIM_ESPECIAL',
    #         'IDENTIFICADOR', 'NUM_INT',
    #         'NUM_FLU', 'TEXT', 'PALAVRA_RESERVADA',
    #         'ATRIBUICAO',  'LISTADEDECLARACAO'
    
         

    #função principal que representa as palavras reservadas
    def palavra_reservada(self):
        node = Node('PALAVRA_RESERVADA')  # cria um nó para representar a regra <main>

        lexema = self.match('PALAVRA_RESERVADA')

        #enquanto houver correspondência, adiciona o lexema como filho
        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('PALAVRA_RESERVADA')  #avança para o próximo lexema após a correspondência

        return node
    
    #função principal que representa os simbolos especiais
    def sim_especial(self):
        node = Node('SIM_ESPECIAL')

        lexema = self.match('SIM_ESPECIAL')

        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('SIM_ESPECIAL')

        return node

    #função principal que representa os operadores aritmeticos
    def op_aritmetico(self):
        node = Node('OP_ARITMETICO')

        lexema = self.match('OP_ARITMETICO')

        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('OP_ARITMETICO')

        return node
    
    #função principal que representa os operadores relacionais
    def op_relacional(self):
        node = Node('OP_RELACIONAL')

        lexema = self.match('OP_RELACIONAL')

        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('OP_RELACIONAL')

        return node
    
    #função principal que representa os operadores logicos
    def op_logico(self):
        node = Node('OP_LOGICO')
        lexema = self.match('OP_LOGICO')

        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('OP_LOGICO')
        
        return node
    
    #função principal que representa os identificadores
    def identificador(self):
        node = Node('IDENTIFICADOR')

        lexema = self.match('IDENTIFICADOR')

        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('IDENTIFICADOR')

        return node
    
    #função principal que representa as atribuições
    def atribuicao(self):
        node = Node('ATRIBUICAO')

        lexema = self.match('ATRIBUICAO')

        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('ATRIBUICAO')

        return node
    
    #função principal que representa as listas de declarações
    def lista_declaracao(self):
        node = Node('LISTADEDECLARACAO')

        lexema = self.match('LISTADEDECLARACAO')

        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('LISTADEDECLARACAO')

        return node
    
    #função principal que representa os text
    def text (self):
        node = Node('TEXT')

        lexema = self.match('TEXT')

        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('TEXT')

        return node
    
    #função principal que representa os numeros inteiros
    def num_int(self):
        node = Node('NUM_INT')

        lexema = self.match('NUM_INT')

        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('NUM_INT')

        return node
    
    #função principal que representa os numeros flutuantes
    def num_flu(self):
        node = Node('NUM_FLU')

        lexema = self.match('NUM_FLU')

        while lexema:
            node.add_child(Node(lexema))
            lexema = self.match('NUM_FLU')

        return node
    
    #função principal que imprime a árvore sintática
    def imprimir_arvore(self, node, nivel=0, tipo_esperado=None, lado=None):
        if node:
            if not node.children:
                #é um nó folha, exibe o tipo esperado e o lexema (se houver)
                lexema = node.label if node.label else ""
                tipo = f"{tipo_esperado}: {lexema}" if tipo_esperado else lexema
                print(' ' * nivel * 4 + f'{lado} {tipo}')
            else:
                #é um nó interno, exibe o rótulo da regra gramatical
                print(' ' * nivel * 4 + f'{lado} {node.label}')

                #para cada filho, imprima à direita e ajuste o lado conforme necessário
                for i, child in enumerate(node.children):
                    if i < len(node.children) - 1:
                        self.imprimir_arvore(child, nivel + 1, tipo_esperado=node.label if tipo_esperado is None else tipo_esperado, lado='|--')
                    else:
                        self.imprimir_arvore(child, nivel + 1, tipo_esperado=node.label if tipo_esperado is None else tipo_esperado, lado='' * nivel * 4 + '|--')


############### AQUI IREI ADICIONAR OS MÉTODOS PARA IDENTIFICAR ERROS SINTÁTICOS ######################
    def erro(self, tipo):
        self.erro_encontrado = True
        self.erro_tipo = tipo

    def erro_sintatico(self, tipo_esperado):
        self.erro(tipo_esperado)
        print(f"Erro sintático: {tipo_esperado} esperado na posição {self.posicao}.")
        exit()  #saia do programa se houver erro sintático

    
    
    
if __name__ == "__main__":
    analisador_lexico = AnalisadorLexico("teste.txt")
    tokens_controle_fluxo = analisador_lexico.get_tabela_simbolos()

    # if tokens_controle_fluxo:
    #     print("Análise léxica bem-sucedida! Tokens gerados:")
    #     analisador_lexico.imprimir_tokens()
    # else:
    #     print("Erro na análise léxica.")
    #     exit()  #saia do programa se houver erro léxico

    # Análise sintática
    analisador_sintatico = AnalisadorSintatico()
    arvore_sintatica_controle_fluxo = analisador_sintatico.parse(tokens_controle_fluxo)

    if not analisador_sintatico.erro_encontrado:
        print("\nAnálise sintática bem-sucedida! Árvore sintática gerada:")
        analisador_sintatico.imprimir_arvore(arvore_sintatica_controle_fluxo)
    else:
        print(f"\n{analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")