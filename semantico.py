class AnalisadorSemantico:
    def __init__(self):
        self.tabela_simbolos = []
    
    def inserir_simbolo(self, id, tipo,tipoValor,valor, escopo):
        linha = []
        linha.append(id)
        linha.append(tipo)
        linha.append(tipoValor)
        linha.append(valor)
        linha.append(escopo)
        self.tabela_simbolos.append(linha)

    def verificar_tipo(self,i, tipo, id):
        if (self.tabela_simbolos[i][1] == 'num_int' and tipo != 'NUM_INT'):
            assert False, "Erro Semantico: para a variavel "+ str(id) + " era esperado um valor do tipo inteiro"
        elif (self.tabela_simbolos[i][1] == 'num_flu' and tipo != 'NUM_FLU'):
            assert False, "Erro Semantico: para a variavel "+ str(id) + " era esperado um valor do tipo float"
        elif (self.tabela_simbolos[i][1] == 'text' and tipo != 'TEXT'):
            assert False, "Erro Semantico: para a variavel "+ str(id) + " era esperado um valor do tipo string"

    def retornar_tipo(self, id, escopo = 'global'):
        i = 0
        while(i < len(self.tabela_simbolos)):
            if (self.tabela_simbolos[i][0] == id and self.tabela_simbolos[i][4] == escopo):
                return self.tabela_simbolos[i][2]
            i = i+1
        raise Exception("Erro Semantico: Identificador nao declarado "+ str(id))

    def retornar_tipo_funcao(self, id):
        i = 0
        while(i < len(self.tabela_simbolos)):
            if (self.tabela_simbolos[i][0] == id):
                return self.tabela_simbolos[i][1].upper()
            i = i+1
        raise Exception("Erro Semantico: Identificador nao declarado "+ str(id))

    def retornar_valor(self, id, escopo = 'global'):
        i = 0
        while(i < len(self.tabela_simbolos)):
            if (self.tabela_simbolos[i][0] == id and self.tabela_simbolos[i][4] == escopo):
                return self.tabela_simbolos[i][3]
            i = i+1
        raise Exception("Erro Semantico: Identificador nao declarado "+ str(id))

    def inserir_valor(self, valor, tipo, id, escopo = 'global'):
        i = 0
        #percorrendo a tabela de simbolos
        while(i < len(self.tabela_simbolos)):
            #verifica a presença do identificador na tabela de simbolos com o escopo correto
            if (self.tabela_simbolos[i][0] == id and self.tabela_simbolos[i][4] == escopo):
                if (tipo == 'IDENTIFICADOR'):
                    #pegando o tipo e o valor do identificador a ser atribuido
                    tipo = self.retornar_tipo(valor,escopo)
                    valor = self.retornar_valor(valor, escopo)
                #função não tem tipo especificado
                if (tipo != 'funcao'):
                    #verificando se o tipo do conteudo bate com o tipo da variavel
                    self.verificar_tipo(i, tipo, id)
                #inserindo o tipo e o valor no conteudo da variavel
                self.tabela_simbolos[i][2] = tipo
                self.tabela_simbolos[i][3] = valor
                return True
            i = i+1
        raise Exception("Erro Semantico: Identificador nao declarado "+ str(id))
    
    def verificar_declaracao(self,tipoVar, tipoValor,id, id2 = None):
        if (tipoVar == 'num_int' and tipoValor != 'NUM_INT'):
            assert False, "Erro Semantico: para a variavel "+ str(id) + " era esperado um valor do tipo inteiro"
        elif (tipoVar == 'num_flu' and tipoValor != 'NUM_FLU'):
            assert False, "Erro Semantico: para a variavel "+ str(id) + " era esperado um valor do tipo float"
        elif (tipoVar == 'text' and tipoValor != 'TEXT'):
            assert False, "Erro Semantico: para a variavel "+ str(id) + " era esperado um valor do tipo string"

    def verificar_redeclaracao(self, id, escopo):
        i = 0
        while(i < len(self.tabela_simbolos)):
            if (self.tabela_simbolos[i][0] == id) and (self.tabela_simbolos[i][4] == escopo) :
                assert False, "Erro Semantico: Identificador "+ str(id) + " está sendo redeclarado"
            i = i+1
    
    def analise_simbolos(self, no, escopo = None):
        tipo = ""
        id= ""
        tipoValor = None
        valor = None
        if no.tipo == 'declaracao':
            for i in no.filhos:
                if i.tipo == 'tipoVar':
                    tipo = i.filhos[0].lexema
                if i.tipo == 'IDENTIFICADOR':
                    #nome da variavel
                    id = i.lexema
                if i.tipo == 'conteudo':
                    tipoValor = i.filhos[0].tipo
                    valor = i.filhos[0].lexema 
                    if tipoValor == 'IDENTIFICADOR':
                        #verifica se o identificador a ser atribuido está na tabela de simbolos
                        #escopo padrão global
                        if escopo == None:
                            #pega o tipo do valor e o valor na tabela de simbolos
                            tipoValor = self.retornar_tipo(i.filhos[0].lexema)
                            valor = self.retornar_valor(i.filhos[0].lexema)
                        else:
                            #pega o tipo do valor e o valor na tabela de simbolos
                            tipoValor = self.retornar_tipo(i.filhos[0].lexema, escopo)
                            valor = self.retornar_valor(i.filhos[0].lexema, escopo)
                    #verifica se o tipo do valor bate com o valor    
                    self.verificar_declaracao(tipo, tipoValor, id)
                    if escopo == None:
                        #verifica se a variavel ja foi declarada
                        self.verificar_redeclaracao(id, 'global')
                        self.inserir_simbolo(id, tipo, tipoValor, valor, 'global')
                    else:
                        #verifica se a variavel ja foi declarada
                        self.verificar_redeclaracao(id, escopo)
                        self.inserir_simbolo(id, tipo, tipoValor, valor, escopo)

        elif no.tipo == 'atribuicao':
            #pegando o nome da variavel
            id = no.filhos[0].lexema
            #pegando o tipo do conteudo a ser inserido na variavel
            tipo = no.filhos[2].filhos[0].tipo
            #pegando o valor do conteudo
            valor = no.filhos[2].filhos[0].lexema
            if escopo == None:
                self.inserir_valor(valor, tipo, id, 'global')
            else:
                self.inserir_valor(valor, tipo, id, escopo)
        #verifica estrutura de parametros para inserir os parametros declarados na função
        elif no.tipo == 'argumento':
            tipo = no.filhos[0].filhos[0].lexema
            id = no.filhos[1].lexema
            self.inserir_simbolo(id, tipo, None, None, escopo)

        elif no.tipo == 'funcao':
            self.verificar_redeclaracao(no.filhos[1].lexema, 'global')
            self.inserir_simbolo(no.filhos[1].lexema, 'funcao', None, None, 'global')
        #pega o valor e o tipo do conteudo após o <retorno> na arvore
        elif no.tipo == 'retorno':
                tipo = self.retornar_tipo_funcao(no.filhos[1].filhos[0].lexema)
                valor = self.retornar_valor(no.filhos[1].filhos[0].lexema, escopo)
                self.inserir_valor(valor, tipo, escopo)
        c= 0
        #percorrer a arvore para analisar os simbolos
        for filho in no.filhos:
            if no.tipo == 'funcao':
                #passando o nome da função para o escopo
                escopo = no.filhos[1].lexema
            #encontrou o segundo <programa> na arvore apos a função, indo para o escopo global
            if filho.tipo == 'programa' and c != 0 and len(filho.filhos)> 0 and filho.filhos[0].tipo != 'retorno':
                escopo = None
                c = 0
            #encontrou o primeiro <programa> na arvore apos a função
            if filho.tipo == 'programa':
                c = 1

            self.analise_simbolos(filho, escopo)

def analisador_semantico(arvore_sintatica):
    analisador_semantico = AnalisadorSemantico()
    analisador_semantico.analise_simbolos(arvore_sintatica)
    return analisador_semantico.tabela_simbolos