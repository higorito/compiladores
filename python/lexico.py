import os


class AnalisadorLexico:

    def __init__(self, arq_font):
        self.__cab_leitura = 0
        self.__linha = 1
        self.__percorrer = []
        self.__lexema = ''
        self.__tabela_simbolos = []
        self.__arq_font = arq_font
        self.__estado = 0
        self.__fim_linha = '\n'
        self.__fim_arquivo = '\0'
        self.__especiais = ['<', '>', ';', '[', ']']

        self.__op_logicos = ['&&', '||', '!']
        self.__op_relacionais = ['==', '!=', '>=', '<=', '>', '<']
        self.__op_aritmeticos = ['+', '-', '*', '/', '//', '**']

        self.__palavras_reservadas = ['main','num_int', 'num_flu', 'text', 'case', 'ordo', 'to', 'when', 'tetin', 'texout', 'puts', 'take', 'fn', 'vacuum', 'bool']


        if not os.path.isfile(arq_font):
            print('Arquivo não encontrado!')
            exit(1)
        else:
            self.__arquivo = open(arq_font).read()
    
    def __isSimbolo(self, char: chr):
        return char in self.__especiais or char in self.__op_logicos or char in self.__op_relacionais or char in self.__op_aritmeticos
    
    def __isPalavraReservada(self, lexema: str):
        return lexema in self.__palavras_reservadas
    
    def __isNumero(self, lexema: str):
        return lexema.isdigit()
    
    def __isIdentificador(self, lexema: str):
        return lexema.isalpha()
    
    def __isFimArquivo(self, char: chr):
        return char == self.__fim_arquivo
    
    def __isFimLinha(self, char: chr):
        return char == self.__fim_linha
    
    def __isEspaco(self, char: chr):
        return char.isspace()
    
    def __isComentario(self, lexema: str):
        return lexema == '--'
    

    #-----#
    def __avancar_cabeca(self):
        self.__cab_leitura += 1

    def __pos_cabeca(self):
        return self.__cab_leitura
    
    def __att_linha(self):
        self.__linha += 1

    def __get_caracter(self):
        if self.__cab_leitura() < len(self.__percorrer):
            self.__letra = self.__percorrer[self.__cab_leitura]
            self.__avancar_cabeca()
            if self.__letra != self.__fim_linha or not self.__letra.isspace(): #isspace() verifica se é espaço
                self.__lexema += self.__letra
            return self.__letra 
        else:
            return self.__fim_linha
        
    def get_tab_tokens(self):
        for self.__linha in self.__arquivo:
            self.__percorrer = list(self.__linha)
            self.__estadoQ0()
            self.__att_linha()
            self.__cab_leitura = 0
        self.__arquivo.close()
        return self.__tabela_simbolos
    
    def __estadoQ0(self):
        self.__estado = 0
        self.__lexema = ''
        self.__get_caracter()
        if self.__letra.isalpha():
            self.__estadoQ1()
        elif self.__letra.isdigit():
            self.__estadoQ2()
        