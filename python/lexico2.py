<<<<<<< Updated upstream
class AnalisadorLexico:
    def __init__(self, path: str):
        self.__tabela_simbolos = []
        self.__cab_leitura = 0
        self.__linha = 1
        self.__lexema = ''
        self.__arq_font = path
        self.__estado = 0

        self.__tokens_aritmeticos = ['+', '-', '*', '/', '//', '**']
        self.__tokens_relacionais = ['==', '!=', '>=', '<=', '>>', '<<']
        self.__tokens_logicos = ['&&', '||', '!']
        self.__caracteres_especiais = ['<', '>', ';', '[', ']']

        self.__palavras_reservadas = ['main', 'vacuum', 'num_int', 'num_flu', 'text', 'case', 'to', 'when', 'textin', 'textout', 'puts', 'take', 'fn', 'vacuum', 'bool']



        self.__isComentario = '--'
        self.__isAtribuicao = '->'
        self.__isString = '"'
        self.__fim_linha = '\n'
        self.__fim_arquivo = '\0'

        arquivo = open(self.__arq_font, 'r')
        self._conteudo = arquivo.read()
        arquivo.close()


    
    def get_tabela_simbolos(self):
        while self.__cab_leitura < len(self._conteudo):
            char = self._conteudo[self.__cab_leitura]

            if self.__isComentario and self._conteudo[self.__cab_leitura:self.__cab_leitura + 2] == '--':
                while self.__cab_leitura < len(self._conteudo) and self._conteudo[self.__cab_leitura] != '\n':
                    self.__cab_leitura += 1
                if self.__cab_leitura < len(self._conteudo):
                    self.__cab_leitura += 1
                    self.__linha += 1
            elif self.__isAtribuicao and self._conteudo[self.__cab_leitura:self.__cab_leitura + 3] == '--->':
                self.adicionar_token('Operador', '--->')
                self.__cab_leitura += 3
            elif self.__isString and char == '"':
                self.__estado = 4
                self.__lexema = char
                self.__cab_leitura += 1
                while self.__cab_leitura < len(self._conteudo) and self._conteudo[self.__cab_leitura] != '"':
                    self.__lexema += self._conteudo[self.__cab_leitura]
                    self.__cab_leitura += 1
                self.__lexema += '"'
                self.__cab_leitura += 1
                self.adicionar_token('String', self.__lexema)
            elif char == self.__fim_linha:
                self.__linha += 1
                self.__cab_leitura += 1
            elif char.isspace():
                self.__cab_leitura += 1
            elif char.isalpha() or char == '_':
                self.__estado = 1
                self.__lexema = char
                self.__cab_leitura += 1
                while self.__cab_leitura < len(self._conteudo) and (self._conteudo[self.__cab_leitura].isalnum() or self._conteudo[self.__cab_leitura] == '_'):
                    self.__lexema += self._conteudo[self.__cab_leitura]
                    self.__cab_leitura += 1
                if self.__lexema in self.__palavras_reservadas:
                    self.adicionar_token('Palavra Reservada', self.__lexema)
                else:
                    self.adicionar_token('Identificador', self.__lexema)
            elif char.isdigit():
                self.__estado = 2
                self.__lexema = char
                self.__cab_leitura += 1
                while self.__cab_leitura < len(self._conteudo) and (self._conteudo[self.__cab_leitura].isdigit() or self._conteudo[self.__cab_leitura] == '.'):
                    self.__lexema += self._conteudo[self.__cab_leitura]
                    self.__cab_leitura += 1
                if '.' in self.__lexema:
                    self.adicionar_token('Número Flutuante', self.__lexema)
                else:
                    self.adicionar_token('Número Inteiro', self.__lexema)
            else:
                self.__estado = 3
                self.__lexema = char
                self.__cab_leitura += 1

                if self.__lexema in self.__tokens_aritmeticos:
                    self.adicionar_token('Operador', self.__lexema)
                elif self.__lexema in self.__tokens_relacionais:
                    self.adicionar_token('Relacional', self.__lexema)
                elif self.__lexema in self.__tokens_logicos:
                    self.adicionar_token('Lógico', self.__lexema)
                elif self.__lexema in self.__caracteres_especiais:
                    self.adicionar_token('Especial', self.__lexema)
                self.__estado = 0
        return self.__tabela_simbolos

    def adicionar_token(self, tipo, lexema):
        token = {'tipo': tipo, 'lexema': lexema, 'linha': self.__linha}
        self.__tabela_simbolos.append(token)


    def main(self):
        self.tabela_simbolos = self.get_tabela_simbolos()
        self.imprimir_tokens()




    def imprimir_tokens(self):
        for token in self.__tabela_simbolos:
            print(f'Tipo: {token["tipo"]}, Lexema: {token["lexema"]}, Linha: {token["linha"]}')




if __name__ == "__main__":
    analisador = AnalisadorLexico("fibonacci.txt")
    analisador.main()  # Chama o método main para iniciar o processo de análise léxica

=======
class AnalisadorLexico:
    def __init__(self, path: str):
        self.__tabela_simbolos = []
        self.__cab_leitura = 0
        self.__linha = 1
        self.__lexema = ''
        self.__arq_font = path
        self.__estado = 0

        self.__tokens_aritmeticos = ['+', '-', '*', '/', '//', '**']
        self.__tokens_relacionais = ['==', '!=', '>=', '<=', '>>', '<<']
        self.__tokens_logicos = ['&&', '||', '!']
        self.__caracteres_especiais = ['<', '>', ';', '[', ']']

        # Adicione "main" à lista de palavras reservadas
        self.__palavras_reservadas = ['main', 'vaccum', 'num_int', 'num_flu', 'text', 'case', 'to', 'when', 'textin', 'textout', 'puts', 'take', 'fn', 'vacuum', 'bool']


        self.__isComentario = '--'
        self.__isAtribuicao = '->'
        self.__isString = '"'
        self.__fim_linha = '\n'
        self.__fim_arquivo = '\0'

        arquivo = open(self.__arq_font, 'r')
        self._conteudo = arquivo.read()
        arquivo.close()


    
    def get_tabela_simbolos(self):
        while self.__cab_leitura < len(self._conteudo):
            char = self._conteudo[self.__cab_leitura]

            if self.__isComentario and self._conteudo[self.__cab_leitura:self.__cab_leitura + 2] == '--':
                while self.__cab_leitura < len(self._conteudo) and self._conteudo[self.__cab_leitura] != '\n':
                    self.__cab_leitura += 1
                if self.__cab_leitura < len(self._conteudo):
                    self.__cab_leitura += 1
                    self.__linha += 1
            elif self.__isAtribuicao and self._conteudo[self.__cab_leitura:self.__cab_leitura + 3] == '--->':
                self.adicionar_token('Operador', '--->')
                self.__cab_leitura += 3
            elif self.__isString and char == '"':
                self.__estado = 4
                self.__lexema = char
                self.__cab_leitura += 1
                while self.__cab_leitura < len(self._conteudo) and self._conteudo[self.__cab_leitura] != '"':
                    self.__lexema += self._conteudo[self.__cab_leitura]
                    self.__cab_leitura += 1
                self.__lexema += '"'
                self.__cab_leitura += 1
                self.adicionar_token('String', self.__lexema)
            elif char == self.__fim_linha:
                self.__linha += 1
                self.__cab_leitura += 1
            elif char.isspace():
                self.__cab_leitura += 1
            elif char.isalpha() or char == '_':
                self.__estado = 1
                self.__lexema = char
                self.__cab_leitura += 1
                while self.__cab_leitura < len(self._conteudo) and (self._conteudo[self.__cab_leitura].isalnum() or self._conteudo[self.__cab_leitura] == '_'):
                    self.__lexema += self._conteudo[self.__cab_leitura]
                    self.__cab_leitura += 1
                if self.__lexema in self.__palavras_reservadas:
                    self.adicionar_token('Palavra Reservada', self.__lexema)
                else:
                    self.adicionar_token('Identificador', self.__lexema)
            elif char.isdigit():
                self.__estado = 2
                self.__lexema = char
                self.__cab_leitura += 1
                while self.__cab_leitura < len(self._conteudo) and (self._conteudo[self.__cab_leitura].isdigit() or self._conteudo[self.__cab_leitura] == '.'):
                    self.__lexema += self._conteudo[self.__cab_leitura]
                    self.__cab_leitura += 1
                if '.' in self.__lexema:
                    self.adicionar_token('Número Flutuante', self.__lexema)
                else:
                    self.adicionar_token('Número Inteiro', self.__lexema)
            else:
                self.__estado = 3
                self.__lexema = char
                self.__cab_leitura += 1

                if self.__lexema in self.__tokens_aritmeticos:
                    self.adicionar_token('Operador', self.__lexema)
                elif self.__lexema in self.__tokens_relacionais:
                    self.adicionar_token('Relacional', self.__lexema)
                elif self.__lexema in self.__tokens_logicos:
                    self.adicionar_token('Lógico', self.__lexema)
                elif self.__lexema in self.__caracteres_especiais:
                    self.adicionar_token('Especial', self.__lexema)
                self.__estado = 0
        return self.__tabela_simbolos

    def adicionar_token(self, tipo, lexema):
        token = {'tipo': tipo, 'lexema': lexema, 'linha': self.__linha}
        self.__tabela_simbolos.append(token)


    def main(self):
        self.tabela_simbolos = self.get_tabela_simbolos()
        self.imprimir_tokens()




    def imprimir_tokens(self):
        for token in self.__tabela_simbolos:
            print(f'Tipo: {token["tipo"]}, Lexema: {token["lexema"]}, Linha: {token["linha"]}')




if __name__ == "__main__":
    analisador = AnalisadorLexico("teste.txt")
    analisador.main()  # Chama o método main para iniciar o processo de análise léxica

>>>>>>> Stashed changes
