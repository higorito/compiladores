import os


class AnalisadorLexico:

    def __init__(self, cam:str):
        self.__cab_leitura = 0
        self.__linha = 1 
        self.__percorrer = []
        self.__lexema = ''
        self.__tabela_simbolos = []
        self.__arq_font = cam
        self.__estado = 0
        self.__fim_linha = '\n'
        self.__fim_arquivo = '\0'
        self.__especiais = ['<', '>', ';', '[', ']']
        

        self.__op_logicos = ['&&', '||', '!']
        self.__op_relacionais = ['==', '!=', '>=', '<=', '>>', '<<']
        self.__op_aritmeticos = ['+', '-', '*', '/', '//', '**']

        self.__palavras_reservadas = ['main','num_int', 'num_flu', 'text', 'case', 'ordo', 'to', 'when', 'tetin', 'texout', 'puts', 'take', 'fn', 'vacuum', 'bool']


        # if not os.path.isfile(arq_font):
        #     print('Arquivo não encontrado!')
        #     exit(1)
        # else:
        #     with open(arq_font) as file:
        #         self.__arq_font = file.read()

        arquivo = open(cam, 'r')
        self._conteudo = arquivo.read()
        
        arquivo.close()
    

    def __adicionar_token(self, tipo, lexema):
        
        token = {'tipo': tipo, 'lexema': lexema, 'linha': self.__linha}
        self.__tabela_simbolos.append(token)


    def isSimbolo(self, char: chr):
        return char in self.__especiais or char in self.__op_logicos or char in self.__op_relacionais or char in self.__op_aritmeticos
    
    def isOperadorLogico(self, lexema: str):
        return lexema in self.__op_logicos
    
    def isPalavraReservada(self, lexema: str):
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
    

    #-----#----- 
    def __avancar_cabeca(self):
        self.__cab_leitura += 1

    def __pos_cabeca(self):
        return self.__cab_leitura
    
    def __att_linha(self):
        self.__linha += 1

    def __get_caracter(self):
        if self.__cab_leitura < len(self.__percorrer):
            self.__letra = self.__percorrer[self.__cab_leitura]
            self.__avancar_cabeca()
            if self.__letra != self.__fim_linha or not self.__letra.isspace(): #isspace() verifica se é espaço
                self.__lexema += self.__letra
            return self.__letra 
        else:
            return self.__fim_linha
        
    def get_tab_tokens(self):
        for linha in self.__arq_font:
            self.__percorrer = list(linha)
            self.__estado = 0
            self.__att_linha()
            self.__cab_leitura = 0
            self.__linha += 1  # Incrementa a linha aqui
        
        return self.__tabela_simbolos
    
    def __estadoQ0(self):
        self.__estado = 0
        self.__lexema = ''
        self.__get_caracter()
        if self.__letra:
            if self.__isNumero(self.__letra):  #numeros
                self.__estado = 1
            elif self.__isIdentificador(self.__letra):  #identificadores
                self.__estado = 2
            elif self.__letra == '"':       #string
                self.__estado = 3
            elif self.__letra in self.__especiais: #caracter especial
                self.__estado = 4
            elif self.__letra in self.__op_aritmeticos: #operador aritmetico
                self.__estado = 5
            elif self.__letra in self.__op_relacionais: #operador relacional
                self.__estado = 6
            elif self.__letra in self.__op_logicos: #operador logico
                self.__estado = 7
            elif self.__letra == " -- ": #comentario
                self.__estado = 8
            elif self.__letra == self.__fim_arquivo:  #fim de arquivo
                self.__estado = 9
            elif self.__letra == self.__fim_linha:      #fim de linha
                self.__estado = 10
            elif self.__letra.isspace():    #espaco
                self.__estado = 11
            elif self.__letra == "=>":
                self.__estado = 12
            else:
                self.__estado = 14

    def __estadoQ1(self):
        self.__estado = 1
        self.__lexema = ''
        self.__get_caracter()

        while self.__letra:
            if self.__letra == ',':
                # Encontrou uma vírgula no número
                self.__lexema += self.__letra
                self.__estado = 13  # Vá para o estado de número flutuante
            elif self.__isNumero(self.__letra):
                self.__lexema += self.__letra
                # Avance para o próximo caractere
                self.__get_caracter()
            else:
                # Terminou a sequência de números
                self.__estado = 0  # Retornar ao estado inicial
                self.__adicionar_token('NUM', self.__lexema)
                break

    def __estadoQ2(self):
        self.__estado = 2
        self.__lexema = ''
        self.__get_caracter()

        while self.__letra:
            if self.__isIdentificador(self.__letra):
                self.__lexema += self.__letra
                self.__get_caracter()
            else:
                # Terminou a sequência de identificadores
                self.__estado = 0  # Retornar ao estado inicial
                if self.__isPalavraReservada(self.__lexema):
                 
                    self.__adicionar_token('PALAVRA_RESERVADA', self.__lexema, self.__linha)
                else:
                    
                    self.__adicionar_token('ID', self.__lexema, self.__linha)
                break

    def __estadoQ3(self):
        self.__estado = 3
        self.__lexema = ''
        self.__get_caracter()

        while self.__letra:
            if self.__letra != '"':
                self.__lexema += self.__letra
                self.__get_caracter()
            else:
                # Terminou a string
                self.__estado = 0  # Retornar ao estado inicial
                # Aqui você pode adicionar o token de string à tabela de símbolos
                self.__adicionar_token('STRING', self.__lexema, self.__linha)
                # Avançar para o próximo caractere após a aspa final
                self.__get_caracter()
                break

    def __estadoQ4(self):
        self.__estado = 4
        self.__lexema = ''
        self.__get_caracter()


        self.__adicionar_token('ESPECIAL', self.__letra, self.__linha)
        self.__estado = 0

    def __estadoQ5(self):
        self.__estado = 5
        self.__lexema = ''
        self.__get_caracter()


        self.__adicionar_token('OP_ARITMETICO', self.__letra, self.__linha)
        self.__estado = 0

    def __estadoQ6(self):
        self.__estado = 6
        self.__lexema = ''
        self.__get_caracter()

        self.__adicionar_token('OP_RELACIONAL', self.__letra, self.__linha)
        self.__estado = 0

    def __estadoQ7(self):
        self.__estado = 7
        self.__lexema = ''
        self.__get_caracter()

        # Aqui você pode adicionar o token de operador lógico à tabela de símbolos
        self.__adicionar_token('OP_LOGICO', self.__letra, self.__linha)
        self.__estado = 0

    def __estadoQ8(self):
        self.__estado = 8
        self.__lexema = ''
        self.__get_caracter()

        while self.__letra:
            if self.__isComentario(self.__lexema):
                self.__lexema += self.__letra
                self.__get_caracter()
            else:
                # Terminou o comentario
                self.__estado = 0
                
                self.__adicionar_token('COMENTARIO', self.__lexema, self.__linha)      
                break

    def __estadoQ9(self):
        self.__estado = 9
        self.__lexema = ''
        self.__get_caracter()

       
        self.__adicionar_token('FIM_ARQUIVO', self.__letra, self.__linha)
        self.__estado = 0


    def __estadoQ10(self):
        self.__estado = 10
        self.__lexema = ''
        self.__get_caracter()

        
        self.__adicionar_token('FIM_LINHA', self.__letra, self.__linha)
        self.__estado = 0

    def __estadoQ11(self):
        self.__estado = 11
        self.__lexema = ''
        self.__get_caracter()

       
        self.__adicionar_token('ESPACO', self.__letra, self.__linha)
        self.__estado = 0

    def __estadoQ12(self):
        self.__estado = 12
        self.__lexema = ''
        self.__get_caracter()

       
        self.__adicionar_token('atribuicao', self.__letra, self.__linha)
        self.__estado = 0

    def __estadoQ13(self):
        self.__estado = 13
        self.__lexema = ''
        self.__get_caracter()

       
        self.__adicionar_token('num_flu', self.__letra, self.__linha)
        self.__estado = 0

    def __estadoQ14(self):
        self.__estado = 13
        self.__lexema = ''
        self.__get_caracter()

       
        self. __adicionar_token('ERRO', self.__letra, self.__linha)

    def __estado(self):
        if self.__estado == 0:
            self.__estadoQ0()
        elif self.__estado == 1:  #aqui eu vou ter q da uma mudada nos estados pq eu joguei 1 pra baixo
            self.__estadoQ1()
        elif self.__estado == 2:
            self.__estadoQ2()
        elif self.__estado == 3:
            self.__estadoQ3()
        elif self.__estado == 4:
            self.__estadoQ4()
        elif self.__estado == 5:
            self.__estadoQ5()
        elif self.__estado == 6:
            self.__estadoQ6()
        elif self.__estado == 7:
            self.__estadoQ7()
        elif self.__estado == 8:
            self.__estadoQ8()
        elif self.__estado == 9:
            self.__estadoQ9()
        elif self.__estado == 10:
            self.__estadoQ10()
        elif self.__estado == 11:
            self.__estadoQ11()
        elif self.__estado == 12:
            self.__estadoQ12()
        elif self.__estado == 13:
            self.__estadoQ13()
        elif self.__estado == 14:
            self.__estadoQ14()
        else:
            print('Erro! Estado não reconhecido!')
            exit(1)   

    def main(self):
        # if not os.path.isfile(self.__arq_font):
        #     print('Arquivo não encontrado!')
        #     exit(1)
        # else:
        #     self.__arq_font = open(self.__arq_font).read()

        self.get_tab_tokens()
        self.imprimir_tokens()

    def imprimir_tokens(self):
        for token in self.__tabela_simbolos:
            print(f'Tipo: {token["tipo"]}, Lexema: {token["lexema"]}, Linha: {token["linha"]}')


if __name__ == "__main__":
    
    analisador = AnalisadorLexico("teste.txt")
    analisador.main()

    analisador.imprimir_tokens()