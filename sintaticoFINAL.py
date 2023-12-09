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
        self.posicao = 0       #posição atual na lista de tokens
        self.erro_encontrado = False
        self.erro_tipo = None

    #função principal que inicia a análise sintática
    def parse(self, tokens):
        self.tokens = tokens
        self.posicao = 0
        self.erro_encontrado = False
        self.erro_tipo = None

        # #debug: Mostra os tokens antes de iniciar o processamento
        # print("Tokens antes da análise sintática:")
        # for token in self.tokens:
        #     print(token)

        #continua com o processamento dos tokens
        arvore_sintatica = self.processar_todos_tokens()

        #verifica palavras reservadas após o processamento
        self.verificar_palavras_reservadas()

        if not self.erro_encontrado:
            return arvore_sintatica
        else:
            return None

    def processar_todos_tokens(self):

        
        #inicializa o nó principal
        node = Node('')

        #processa cada token até o final da lista
        while self.posicao < len(self.tokens):
            token_atual = self.tokens[self.posicao]

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
                self.erro_sintatico(f"Token inesperado: {token_atual['tipo']}, esperado algum tipo específico.")
                self.posicao += 1  #avança para o próximo token


        return node
        

    #função para verificar se o token atual corresponde ao tipo esperado
    def match(self, tipos_esperados):
        if self.posicao < len(self.tokens):
            token_atual = self.tokens[self.posicao]

            if token_atual['tipo'] in tipos_esperados:
                self.posicao += 1
                return token_atual['lexema']
            else:
                self.erro_sintatico(f"Erro de correspondência: esperado {tipos_esperados}, encontrado {token_atual['tipo']}.")
                return None  #retorna None em caso de erro

       

    #   APLICAÇÃO DAS FUNÇÕES
    #          'OP_ARITMETICO', 'OP_RELACIONAL', 
    #         'OP_LOGICO', 'SIM_ESPECIAL',
    #         'IDENTIFICADOR', 'NUM_INT',
    #         'NUM_FLU', 'TEXT', 'PALAVRA_RESERVADA',
    #         'ATRIBUICAO',  'LISTADEDECLARACAO'
    
         

    #função principal que representa as palavras reservadas
    def palavra_reservada(self):
        tipos_esperados = ['PALAVRA_RESERVADA', 'ATRIBUICAO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_FLU', 'TEXT', 'OP_ARITMETICO', 'OP_RELACIONAL', 'OP_LOGICO', 'SIM_ESPECIAL', 'LISTADEDECLARACAO']

        lexema = self.match(tipos_esperados)

        if lexema:
            node = Node('PALAVRA_RESERVADA')  #cria um nó específico para a palavra reservada
            node.add_child(Node(lexema))
            return node
        else:
            return None
    
    #função principal que representa os simbolos especiais
    def sim_especial(self):
        node = Node('SIM_ESPECIAL')
        tipos_esperados = ['PALAVRA_RESERVADA', 'ATRIBUICAO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_FLU', 'TEXT', 'OP_ARITMETICO', 'OP_RELACIONAL', 'OP_LOGICO', 'SIM_ESPECIAL', 'LISTADEDECLARACAO']

        lexema = self.match(tipos_esperados)

        if lexema:
            node.add_child(Node(lexema))
            return node
        else:
            return None

    #função principal que representa os operadores aritmeticos
    def op_aritmetico(self):
        node = Node('OP_ARITMETICO')
        tipos_esperados = ['PALAVRA_RESERVADA', 'ATRIBUICAO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_FLU', 'TEXT', 'OP_ARITMETICO', 'OP_RELACIONAL', 'OP_LOGICO', 'SIM_ESPECIAL', 'LISTADEDECLARACAO']

        lexema = self.match(tipos_esperados)

        if lexema:
            node.add_child(Node(lexema))
            return node
        else:
            return None

    #função principal que representa os operadores relacionais
    def op_relacional(self):
        node = Node('OP_RELACIONAL')
        tipos_esperados = ['PALAVRA_RESERVADA', 'ATRIBUICAO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_FLU', 'TEXT', 'OP_ARITMETICO', 'OP_RELACIONAL', 'OP_LOGICO', 'SIM_ESPECIAL', 'LISTADEDECLARACAO']

        lexema = self.match(tipos_esperados)

        if lexema:
            node.add_child(Node(lexema))
            return node
        else:
            return None

    #função principal que representa os operadores logicos
    def op_logico(self):
        node = Node('OP_LOGICO')
        tipos_esperados = ['PALAVRA_RESERVADA', 'ATRIBUICAO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_FLU', 'TEXT', 'OP_ARITMETICO', 'OP_RELACIONAL', 'OP_LOGICO', 'SIM_ESPECIAL', 'LISTADEDECLARACAO']

        lexema = self.match(tipos_esperados)

        if lexema:
            node.add_child(Node(lexema))
            return node
        else:
            return None

    #função principal que representa os identificadores
    def identificador(self):
        node = Node('IDENTIFICADOR')
        tipos_esperados = ['PALAVRA_RESERVADA', 'ATRIBUICAO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_FLU', 'TEXT', 'OP_ARITMETICO', 'OP_RELACIONAL', 'OP_LOGICO', 'SIM_ESPECIAL', 'LISTADEDECLARACAO']

        lexema = self.match(tipos_esperados)

        if lexema:
            node.add_child(Node(lexema))
            return node
        else:
            return None

    #função principal que representa as atribuições
    def atribuicao(self):
        node = Node('ATRIBUICAO')
        tipos_esperados = ['PALAVRA_RESERVADA', 'ATRIBUICAO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_FLU', 'TEXT', 'OP_ARITMETICO', 'OP_RELACIONAL', 'OP_LOGICO', 'SIM_ESPECIAL', 'LISTADEDECLARACAO']

        lexema = self.match(tipos_esperados)

        if lexema:
            node.add_child(Node(lexema))
            return node
        else:
            return None

    #função principal que representa as listas de declarações
    def lista_declaracao(self):
        node = Node('LISTADEDECLARACAO')
        tipos_esperados = ['PALAVRA_RESERVADA', 'ATRIBUICAO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_FLU', 'TEXT', 'OP_ARITMETICO', 'OP_RELACIONAL', 'OP_LOGICO', 'SIM_ESPECIAL', 'LISTADEDECLARACAO']

        lexema = self.match(tipos_esperados)

        if lexema:
            node.add_child(Node(lexema))
            return node
        else:
            return None

    #função principal que representa os text
    def text(self):
        node = Node('TEXT')
        tipos_esperados = ['PALAVRA_RESERVADA', 'ATRIBUICAO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_FLU', 'TEXT', 'OP_ARITMETICO', 'OP_RELACIONAL', 'OP_LOGICO', 'SIM_ESPECIAL', 'LISTADEDECLARACAO']

        lexema = self.match(tipos_esperados)

        if lexema:
            node.add_child(Node(lexema))
            return node
        else:
            return None

    #função principal que representa os numeros inteiros
    def num_int(self):
        node = Node('NUM_INT')
        tipos_esperados = ['PALAVRA_RESERVADA', 'ATRIBUICAO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_FLU', 'TEXT', 'OP_ARITMETICO', 'OP_RELACIONAL', 'OP_LOGICO', 'SIM_ESPECIAL', 'LISTADEDECLARACAO']

        lexema = self.match(tipos_esperados)

        if lexema:
            node.add_child(Node(lexema))
            return node
        else:
            return None

    #função principal que representa os numeros flutuantes
    def num_flu(self):
        node = Node('NUM_FLU')
        tipos_esperados = ['PALAVRA_RESERVADA', 'ATRIBUICAO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_FLU', 'TEXT', 'OP_ARITMETICO', 'OP_RELACIONAL', 'OP_LOGICO', 'SIM_ESPECIAL', 'LISTADEDECLARACAO']

        lexema = self.match(tipos_esperados)

        if lexema:
            node.add_child(Node(lexema))
            return node
        else:
            return None
    
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


############### IMPLEMENTAÇÃO DE ERROS SINTÁTICOS ######################

    def erro(self, tipo):
        self.erro_encontrado = True
        self.erro_tipo = tipo

    #verifica erro sintático, caso tenha um tipo de token esperado e outro encontrado, ele informa.
    def erro_sintatico(self, mensagem):
        self.erro_encontrado = True
        self.erro_tipo = "Erro Sintático"
        print(f"{self.erro_tipo}: {mensagem} na posição {self.posicao}.")
        exit()  #saia do programa se houver erro sintático

    #verifica o erro de uma palavra reservada ser atribuida a um NUM_INT, por exemplo main ==1, main >= 2... etc
    def verificar_palavras_reservadas(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'PALAVRA_RESERVADA'
                and proximo_token['tipo'] == 'OP_RELACIONAL'
                and token_depois_do_proximo['tipo'] == 'NUM_INT'
            ):
                mensagem_erro = f"A palavra reservada '{token_atual['lexema']}' não pode ser relacionada com um NUM_INT"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
    
    #verifica o erro de operações entre NUM_INT e NUM_FLU, por exemplo 1 + 1.0, 2 * 2.0... etc
    def verificar_operacoes_num_intANDnum_flu(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'NUM_INT'
                and proximo_token['tipo'] == 'OP_ARITMETICO'
                and token_depois_do_proximo['tipo'] == 'NUM_FLU'
            ):
                mensagem_erro = f"Não é possível realizar operações entre um NUM_INT e um NUM_FLU"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
    
    #verifica o erro de atribuição em palavra reservada, por exemplo main -> 1, main -> 2... etc
    def verificar_atribuicao_em_palavra_reservada(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'PALAVRA_RESERVADA'
                and proximo_token['tipo'] == 'ATRIBUICAO'
                and token_depois_do_proximo['tipo'] == 'NUM_INT'
            ):
                mensagem_erro = f"Não é possível atribuir um valor a uma palavra reservada"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
    
    #verifica o erro de atribuição em identificador, por exemplo papai noel -> 20, papai noel -> 30... etc
    def verificar_atribuicao_em_identificador(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'IDENTIFICADOR'
                and proximo_token['tipo'] == 'ATRIBUICAO'
                and token_depois_do_proximo['tipo'] == 'NUM_INT'
            ):
                mensagem_erro = f"Não é possível atribuir um valor a um identificador"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
    
    #verificar o erro de não fechar [] ou @ corretamente, por exemplo main[1,2,3  ... @ teste  etc
    def verificar_fechamento_parenteses(self):
        stack = []  #uma pilha para rastrear os símbolos de abertura
        contador_at = 0

        for i, token in enumerate(self.tokens):
            if token['tipo'] == 'SIM_ESPECIAL':
                lexema = token['lexema']

                if lexema == '[':
                    stack.append(('[', i))  #empilha o símbolo de abertura '[' e sua posição
                elif lexema == ']':
                    if not stack:
                        mensagem_erro = f"Símbolo de fechamento ']' na posição {i} não tem correspondência de abertura"
                        self.erro_sintatico(mensagem_erro)
                        return True

                    simbolo_abertura, posicao_abertura = stack.pop()

                    #verifica se os tipos de símbolos correspondem
                    if simbolo_abertura != '[':
                        mensagem_erro = f"Símbolo de fechamento ']' na posição {i} não corresponde ao tipo de abertura '{simbolo_abertura}' na posição {posicao_abertura}"
                        self.erro_sintatico(mensagem_erro)
                        return True
                elif lexema == '@':
                    contador_at += 1

        #verifica se há símbolos de abertura não fechados
        for simbolo_abertura, posicao_abertura in stack:
            mensagem_erro = f"Símbolo de abertura '{simbolo_abertura}' na posição {posicao_abertura} não tem correspondência de fechamento."
            self.erro_sintatico(mensagem_erro)
            return True

        #verifica se o número de '@' é par
        if contador_at % 2 != 0:
            mensagem_erro = "O @ não possui fechamento"
            self.erro_sintatico(mensagem_erro)
            return True

        return False
    
    #verificar o erro de não finalizar o arquivo com ;, por exemplo main , testando [1,2,3] .... etc
    def verificar_fechamento_ponto_virgula(self):
        ultimo_token = self.tokens[-1] if self.tokens else None

        #verifica se o último token existe e se termina com ponto e vírgula
        if ultimo_token and ultimo_token['tipo'] != 'SIM_ESPECIAL' and ultimo_token['lexema'] != ';':
            mensagem_erro = "O arquivo não termina com ';'"
            self.erro_sintatico(mensagem_erro)
            return True

        return False
    
    #verificar o erro de não finalizar NUM_FLU e NUM_INT com ;, por exemplo 1.5, 2.5, 3.5 .... etc
    def verificar_fechamento_ponto_virgula_num_intANDnum_flu(self):
        for i in range(len(self.tokens) - 1):
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]

            if (
                token_atual['tipo'] in ['NUM_INT', 'NUM_FLU']
                and proximo_token['tipo'] != 'SIM_ESPECIAL'
                and proximo_token['lexema'] != ';'
            ):
                mensagem_erro = f"O {token_atual['tipo']} '{token_atual['lexema']}' não está finalizado com ';'"
                self.erro_sintatico(mensagem_erro)
                return True

        #verifica o último token no caso de ser um NUM_INT ou NUM_FLU
        ultimo_token = self.tokens[-1] if self.tokens else None
        if (
            ultimo_token
            and ultimo_token['tipo'] in ['NUM_INT', 'NUM_FLU']
            and not ultimo_token['lexema'].endswith(';')
        ):
            mensagem_erro = f"O {ultimo_token['tipo']} '{ultimo_token['lexema']}' não está finalizado com ';'"
            self.erro_sintatico(mensagem_erro)
            return True

        return False
        

    #verifica o erro de uma palavra reservada ter uma operação a um NUM_INT, por exemplo main +1, main * 2... etc
    def verificar_operacoes_palavrareservadaANDnum_int(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'PALAVRA_RESERVADA'
                and proximo_token['tipo'] == 'OP_ARITMETICO'
                and token_depois_do_proximo['tipo'] == 'NUM_INT'
            ):
                mensagem_erro = f"A palavra reservada '{token_atual['lexema']}' não pode ter uma operação com um NUM_INT"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
    
    #verifica o erro de uma palavra reservada ter uma operação a um NUM_INT, por exemplo main +1.3, main * 2.3 ... etc
    def verificar_operacoes_palavrareservadaANDnum_flu(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'PALAVRA_RESERVADA'
                and proximo_token['tipo'] == 'OP_ARITMETICO'
                and token_depois_do_proximo['tipo'] == 'NUM_FLU'
            ):
                mensagem_erro = f"A palavra reservada '{token_atual['lexema']}' não pode ter uma operação com um NUM_FLU"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
    
    #verifica o erro de um identificador ter uma operação a um NUM_INT, por exemplo PAPAI NOEL +1, PAPEL NOEL * 2 ... etc
    def verificar_operacoes_identificadorANDnum_int(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'IDENTIFICADOR'
                and proximo_token['tipo'] == 'OP_ARITMETICO'
                and token_depois_do_proximo['tipo'] == 'NUM_INT'
            ):
                mensagem_erro = f"O identificador '{token_atual['lexema']}' não pode ter uma operação com um NUM_INT"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
    
    #verifica o erro de um identificador ter uma operação a um NUM_FLU, por exemplo PAPEL NOEL +1.4, PAPAI NOEL * 2.3 ... etc
    def verificar_operacoes_identificadorANDnum_flu(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'IDENTIFICADOR'
                and proximo_token['tipo'] == 'OP_ARITMETICO'
                and token_depois_do_proximo['tipo'] == 'NUM_FLU'
            ):
                mensagem_erro = f"O identificador '{token_atual['lexema']}' não pode ter uma operação com um NUM_FLU"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
    
    #verifica o erro de um identificador ter uma operação a um NUM_FLU, por exemplo PAPEL NOEL + main, PAPAI NOEL * main ... etc
    def verificar_operacoes_identificadorANDpalavra_reservada(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == ['IDENTIFICADOR','PALAVRA_RESERVADA']
                and proximo_token['tipo'] == 'OP_ARITMETICO'
                and token_depois_do_proximo['tipo'] == ['IDENTIFICADOR','PALAVRA_RESERVADA']
            ):
                mensagem_erro = f"O identificador '{token_atual['lexema']}' não pode ter uma operação com uma PALAVRA_RESERVADA"
                self.erro_sintatico(mensagem_erro)
                return True
        return False

    #verifica o erro de um identificador ter uma operação a um identificador, por exemplo PAPEL NOEL + teste, PAPAI NOEL * teste ... etc
    def verificar_operacoes_identificadorANDidentificador(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'IDENTIFICADOR'
                and proximo_token['tipo'] == 'OP_ARITMETICO'
                and token_depois_do_proximo['tipo'] == 'IDENTIFICADOR'
            ):
                mensagem_erro = f"O identificador '{token_atual['lexema']}' não pode ter uma operação com um IDENTIFICADOR"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
    
    #verifica o erro de uma palavra_reservada ter uma operação a uma palavra_reservada, por exemplo main + main, main * main ... etc
    def verificar_operacoes_palavra_reservadaANDpalavra_reservada(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'PALAVRA_RESERVADA'
                and proximo_token['tipo'] == 'OP_ARITMETICO'
                and token_depois_do_proximo['tipo'] == 'PALAVRA_RESERVADA'
            ):
                mensagem_erro = f"A palavra reservada '{token_atual['lexema']}' não pode ter uma operação com uma PALAVRA_RESERVADA"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
        
    #verifica o erro de uma palavra_reservada ter uma operação relacional a um identificador, por exemplo main == teste, num_int ==teste ... etc
    def verificar_operacaoRELACIONAL_palavra_reservadaANDidentificador(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'PALAVRA_RESERVADA'
                and proximo_token['tipo'] == 'OP_RELACIONAL'
                and token_depois_do_proximo['tipo'] == 'IDENTIFICADOR'
            ):
                mensagem_erro = f"A palavra reservada '{token_atual['lexema']}' não pode ter uma operação relacional com um IDENTIFICADOR"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
    #verifica o erro de uma palavra_reservada ter uma atribuição a um identificador, por exemplo main -> a, main -> teste ... etc
    def verificar_atribuicao_palavra_reservadaANDidentificador(self):
        for i in range(len(self.tokens) - 2):  
            token_atual = self.tokens[i]
            proximo_token = self.tokens[i + 1]
            token_depois_do_proximo = self.tokens[i + 2]

            if (
                token_atual['tipo'] == 'PALAVRA_RESERVADA'
                and proximo_token['tipo'] == 'ATRIBUICAO'
                and token_depois_do_proximo['tipo'] == 'IDENTIFICADOR'
            ):
                mensagem_erro = f"A palavra reservada '{token_atual['lexema']}' não pode ter uma atribuição com um IDENTIFICADOR"
                self.erro_sintatico(mensagem_erro)
                return True
        return False
    
    

############### FECHAMENTO ERROS SINTÁTICOS ######################



if __name__ == "__main__":
    analisador_lexico = AnalisadorLexico("teste.txt")
    tokens_controle_fluxo = analisador_lexico.get_tabela_simbolos()

    if tokens_controle_fluxo:
         print("Análise léxica bem-sucedida! Tokens gerados:")
         analisador_lexico.imprimir_tokens()
    else:
         print("Erro na análise léxica.")
         exit()  #saia do programa se houver erro léxico

    #análise sintática
    analisador_sintatico = AnalisadorSintatico()
    arvore_sintatica_controle_fluxo = analisador_sintatico.parse(tokens_controle_fluxo)


   #exibição dos erros sintáticos:
    if analisador_sintatico.verificar_palavras_reservadas():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_operacoes_num_intANDnum_flu():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_atribuicao_em_palavra_reservada():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_atribuicao_em_identificador():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_fechamento_parenteses():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_fechamento_ponto_virgula():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_fechamento_ponto_virgula_num_intANDnum_flu():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_operacoes_palavrareservadaANDnum_int():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_operacoes_palavrareservadaANDnum_flu():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_operacoes_identificadorANDnum_int():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_operacoes_identificadorANDnum_flu():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_operacoes_identificadorANDpalavra_reservada():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_operacoes_palavra_reservadaANDpalavra_reservada():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_operacoes_identificadorANDidentificador():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")

    if analisador_sintatico.verificar_operacaoRELACIONAL_palavra_reservadaANDidentificador():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")
        
    if analisador_sintatico.verificar_atribuicao_palavra_reservadaANDidentificador():
        print(f"\n{analisador_sintatico.erro_tipo}: {analisador_sintatico.erro_tipo}")
        print("Erro na análise sintática.")
    else:
        if not analisador_sintatico.erro_encontrado:
            print("\nAnálise sintática bem-sucedida! Árvore sintática gerada:")
            analisador_sintatico.imprimir_arvore(arvore_sintatica_controle_fluxo)
