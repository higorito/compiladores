class AnalisadorLexico:
    def __init__(self, path: str):
        self.tokens = []
        self.__tabela_simbolos = []
        self.__cab_leitura = 0
        self.__linha = 1
        self.__lexema = ''
        self.__arq_font = path
        self.__estado = 0

        self.__tokens_aritmeticos = ['+', '-', '*', '/', '//', '**']
        self.__tokens_relacionais = ['==', '!=', '>=', '<=', '>>', '<<']
        self.__tokens_logicos = ['&&', '||', '!']
        self.__caracteres_especiais = ['@', ';', '[', ']', ',']

        self.__palavras_reservadas = ['main', 'num_int', 'num_flu', 'text', 'case', 'to', 'when', 'textin', 'textout', 'puts', 'take', 'bool', 'ordo', 'fn']


        self.__isComentario = '--'
        self.__isAtribuicao =  '->'
        self.__isString = '"'
        self.__fim_linha = '\n'
        self.__fim_arquivo = '\0'

        arquivo = open(self.__arq_font, 'r')
        self._conteudo = arquivo.read()
        arquivo.close()


    
    def get_tabela_simbolos(self):
        tabela_simbolos = []
        while self.__cab_leitura < len(self._conteudo):
            char = self._conteudo[self.__cab_leitura]

            if self.__isComentario and self._conteudo[self.__cab_leitura:self.__cab_leitura + 2] == '--':
                while self.__cab_leitura < len(self._conteudo) and self._conteudo[self.__cab_leitura] != '\n':
                    self.__cab_leitura += 1
                if self.__cab_leitura < len(self._conteudo):
                    self.__cab_leitura += 1
                    self.__linha += 1
            elif self._conteudo[self.__cab_leitura:self.__cab_leitura + 2] in self.__tokens_relacionais:
                self.adicionar_token('OP_RELACIONAL', self._conteudo[self.__cab_leitura:self.__cab_leitura + 2])
                self.__cab_leitura += 2
            elif self._conteudo[self.__cab_leitura:self.__cab_leitura + 2] in ['->']:
                self.adicionar_token('ATRIBUICAO', self._conteudo[self.__cab_leitura:self.__cab_leitura + 2])
                self.__cab_leitura += 2
            elif self.__isString and char == '"':
                self.__estado = 4
                self.__lexema = char
                self.__cab_leitura += 1
                while self.__cab_leitura < len(self._conteudo) and self._conteudo[self.__cab_leitura] != '"':
                    self.__lexema += self._conteudo[self.__cab_leitura]
                    self.__cab_leitura += 1
                if self.__cab_leitura < len(self._conteudo) and self._conteudo[self.__cab_leitura] == '"':
                    self.__lexema += self._conteudo[self.__cab_leitura]  #adicionando a segunda aspa ao lexema
                    self.__cab_leitura += 1
                    self.verificar_aspas(self.__lexema, self.__linha)
                    self.adicionar_token('TEXT', self.__lexema)
                    
                else:
                    #senão encontrar a segunda aspa, indicar erro
                    print(f"Erro lexic  o: String '{self.__lexema}' na linha {self.__linha} com aspas faltando")
                    self.__cab_leitura += 1  #avancando para evitar loop infinito
                
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
                    self.adicionar_token('PALAVRA_RESERVADA', self.__lexema)
                else:
                    self.adicionar_token('IDENTIFICADOR', self.__lexema)
                    self.erro_lexico_acento(self.__lexema, self.__linha)
            elif char.isdigit():
                self.__estado = 2
                self.__lexema = char
                self.__cab_leitura += 1
                while self.__cab_leitura < len(self._conteudo) and (self._conteudo[self.__cab_leitura].isdigit() or self._conteudo[self.__cab_leitura] == '.'):
                    self.__lexema += self._conteudo[self.__cab_leitura]
                    self.__cab_leitura += 1
                if '.' in self.__lexema:
                    self.adicionar_token('NUM_FLU', self.__lexema)
                else:
                    self.adicionar_token('NUM_INT', self.__lexema)
            else:
                self.__estado = 3
                self.__lexema = char
                self.__cab_leitura += 1

                if self.__lexema in self.__tokens_aritmeticos:
                    self.adicionar_token('OP_ARITMETICO', self.__lexema)
                # elif self.__lexema in self.__tokens_relacionais:
                #     self.adicionar_token('OP_RELACIONAL', self.__lexema)
                elif self.__lexema in self.__tokens_logicos:
                    self.adicionar_token('OP_LOGICO', self.__lexema)
                elif self.__lexema in self.__caracteres_especiais:
                    self.adicionar_token('SIM_ESPECIAL', self.__lexema)
                self.__estado = 0
        return self.__tabela_simbolos

    def adicionar_token(self, tipo, lexema):
        token = {'tipo': tipo, 'lexema': lexema, 'linha': self.__linha}
        self.__tabela_simbolos.append(token)


    def preencher_tokens(self):
        for token in self.__tabela_simbolos:
            elemento = []
            elemento.append(token["tipo"])
            elemento.append(token["lexema"])
            elemento.append(token["linha"])
            self.tokens.append(elemento)
        
    def imprimir_tokens(self):
        for token in self.__tabela_simbolos:
            print(f'{token["tipo"]}, {token["lexema"]}, Linha: {token["linha"]}')

    
    def verificar_tokens_validos(self):
        tokens_validos = set([ #pode adicionar outros tokens ou modificar
            'OP_ARITMETICO', 'OP_RELACIONAL', 
            'OP_LOGICO', 'SIM_ESPECIAL',
            'IDENTIFICADOR', 'NUM_INT',
            'NUM_FLU', 'TEXT', 'PALAVRA_RESERVADA',
            'ATRIBUICAO',  'LISTADEDECLARACAO'
        ])  

        for token in self.__tabela_simbolos:
            if token['tipo'] not in tokens_validos:
                print(f"Erro lexico: Token inválido '{token['lexema']}' na linha {token['linha']}")

    def erro_lexico_acento(self, lexema, linha):
        if any(char.isalpha() and not char.isascii() for char in lexema):
            print(f"Erro lexico: Identificador '{lexema}' na linha {linha} contem caracteres nao ASCII (acentos)")

    def encontrar_identificadores_duplicados(self):
        identificadores_vistos = set()

        for token in self.__tabela_simbolos:
            if token['tipo'] == 'IDENTIFICADOR':
                lexema = token['lexema']
                linha = token['linha']

                if lexema in identificadores_vistos:
                    print(f"Erro lexico: Identificador '{lexema}' duplicado na linha {linha}")
                else:
                    identificadores_vistos.add(lexema)
                    
    def verificar_aspas(self, lexema, linha):
        if not (lexema.startswith('"') and lexema.endswith('"')):
            print(f"Erro lexico: String '{lexema}' na linha {linha} com aspas faltando ou no lugar errado")

    def main(self):
        self.tabela_simbolos = self.get_tabela_simbolos()
        self.verificar_tokens_validos() 
        self.imprimir_tokens()
        self.preencher_tokens()

if __name__ == "__main__":
    # analisador = AnalisadorLexico("erros/erro-lexico-acento.if")
    analisador = AnalisadorLexico("exemplo1.txt")
    analisador.main()