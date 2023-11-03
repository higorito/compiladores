class AnalisadorLexico:
    def __init__(self, path:str):
        self.__cab_leitura = 0
        self.__linha = 1 
        self.__percorrer = []
        self.__lexema = ''
        self.__tabela_simbolos = []
        self.__arq_font = path
        self.__estado = 0
        

        self.__especiais = ['<', '>', ';', '[', ']']
        self.__op_logicos = ['&&', '||', '!']
        self.__op_relacionais = ['==', '!=', '>=', '<=', '>>', '<<']
        self.__op_aritmeticos = ['+', '-', '*', '/', '//', '**']

        self.__palavras_reservadas = ['main','num_int', 'num_flu', 'text', 'case', 'ordo', 'to', 'when', 'tetin', 'texout', 'puts', 'take', 'fn', 'vacuum', 'bool']

        self.__isComentario = ['--']
        self.__isAtribuicao = ['->']
        self.__isString = ['"'] 
        self.__fim_linha = '\n'
        self.__fim_arquivo = '\0'

        arquivo = open(path, 'r')
        self._conteudo = arquivo.read()
        
        arquivo.close()
    
    def __adicionar_token(self, tipo, lexema):
        
        token = {'tipo': tipo, 'lexema': lexema, 'linha': self.__linha}
        self.__tabela_simbolos.append(token)

    def get_tab_tokens(self):
        while self.__cab_leitura < len(self._conteudo):
            char = self._conteudo[self.__cab_leitura]

            if self.__isComentario and self._conteudo[self.__cab_leitura:self.__cab_leitura + 2] == '--':
                # Verifica se é um comentário
                while self.__cab_leitura < len(self._conteudo) and self._conteudo[self.__cab_leitura] != '\n':
                    self.__cab_leitura += 1
                if self.__cab_leitura < len(self._conteudo):
                    # Pula o caractere de nova linha
                    self.__cab_leitura += 1
                    self.__linha += 1
            elif self.__isAtribuicao and self._conteudo[self.__cab_leitura:self.__cab_leitura + 2] == '->':
                # É um token de atribuição
                self.__adicionar_token('Atribuição', '->')
                self.__cab_leitura += 2
            elif self.__isString and char == '"':
                # É uma string
                self.__estado = 4
                self.__lexema = char
                self.__cab_leitura += 1
                while self.__cab_leitura < len(self._conteudo) and self._conteudo[self.__cab_leitura] != '"':
                    self.__lexema += self._conteudo[self.__cab_leitura]
                    self.__cab_leitura += 1
                self.__lexema += '"'
                self.__cab_leitura += 1
                self.__adicionar_token('String', self.__lexema)
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
                    self.__adicionar_token('Palavra Reservada', self.__lexema)
                else:
                    self.__adicionar_token('Identificador', self.__lexema)
            elif char.isdigit():
                self.__estado = 2
                self.__lexema = char
                self.__cab_leitura += 1
                while self.__cab_leitura < len(self._conteudo) and (self._conteudo[self.__cab_leitura].isdigit() or self._conteudo[self.__cab_leitura] == '.'):
                    self.__lexema += self._conteudo[self.__cab_leitura]
                    self.__cab_leitura += 1
                if '.' in self.__lexema:
                    self.__adicionar_token('Número Flutuante', self.__lexema)
                else:
                    self.__adicionar_token('Número Inteiro', self.__lexema)
            else:
                self.__estado = 3
                self.__lexema = char
                self.__cab_leitura += 1

                if self.__lexema in self.__op_aritmeticos:
                    self.__adicionar_token('Operador Aritmético', self.__lexema)
                elif self.__lexema in self.__op_relacionais:
                    self.__adicionar_token('Operador Relacional', self.__lexema)
                elif self.__lexema in self.__op_logicos:
                    self.__adicionar_token('Operador Lógico', self.__lexema)
                elif self.__lexema in self.__especiais:
                    self.__adicionar_token('Caractere Especial', self.__lexema)
            self.__estado = 0

    
    def main(self):

        self.get_tab_tokens()
        self.imprimir_tokens()

    def imprimir_tokens(self):
        for token in self.__tabela_simbolos:
            print(f'Tipo: {token["tipo"]}, Lexema: {token["lexema"]}, Linha: {token["linha"]}')


if __name__ == "__main__":
    
    analisador = AnalisadorLexico("teste.txt")
    analisador.main()

    analisador.imprimir_tokens()