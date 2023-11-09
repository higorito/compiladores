from lexico2 import AnalisadorLexico

class AnalisadorSintatico:
    def __init__(self, path):
        self.analisador_lexico = AnalisadorLexico(path)
        self.tokens = self.analisador_lexico.get_tabela_simbolos()
        self.indice_token_atual = 0

    def match(self, tipo_esperado):
        if self.indice_token_atual < len(self.tokens):
            tipo_token_atual = self.tokens[self.indice_token_atual]['tipo']
            if tipo_token_atual == tipo_esperado:
                self.indice_token_atual += 1
            else:
                raise SyntaxError(f"Token inesperado {tipo_token_atual} na linha {self.tokens[self.indice_token_atual]['linha']}")

#### MÉTODO QUE ANALISA DE FORMA MANUAL O ARQUIVO TESTE.TXT ####
#### MÉTODO QUE ANALISA DE FORMA MANUAL O ARQUIVO TESTE.TXT ####
#### MÉTODO QUE ANALISA DE FORMA MANUAL O ARQUIVO TESTE.TXT ####

#def analisar_programa(self):
        #ISSO AQUI É UM MÉTODO QUE LÊ TODO O ARQUIVO "TESTE.TXT" 
        #FOI UM TRAMPO FUNCIONAR ESSA PARTE, ATÉ ENTENDER QUE ERA ASSIM.

        #O MÉTODO COMEÇA NA PRIMEIRA LINHA DO "TESTE.TXT" E VAI LENDO ATÉ O FINAL IDENTIFICANDO O QUE CADA TOKEN É.
        #try:
          #  self.match('Palavra Reservada')     #fn
          #  self.match('Palavra Reservada')     #main
          #  self.match('Palavra Reservada')     #vaccum
          #  self.match('Especial')              #<
          #  self.match('Palavra Reservada')     #num_int
          #  self.match('Identificador')         #num1
          #  self.match('Operador')              #-
          #  self.match('Especial')              #>
          #  self.match('Número Inteiro')        #4
          #  self.match('Especial')              #;
          #  self.match('Palavra Reservada')     #num_int
          #  self.match('Identificador')         #num2
          #  self.match('Operador')              #-
          #  self.match('Especial')              #>
          #  self.match('Número Inteiro')        #9
          #  self.match('Especial')              #;
          #  self.match('Palavra Reservada')     #num_flu
          #  self.match('Identificador')         #num3
          #  self.match('Operador')              #-
          #  self.match('Especial')              #>
          #  self.match('Número Flutuante')      #1.7
          #  self.match('Especial')              #;
          #  self.match('Palavra Reservada')     #text
          #  self.match('Identificador')         #palavra
          #  self.match('Operador')              #-
          #  self.match('Especial')              #>
          #  self.match('String')                #"stringAqui"
          #  self.match('Especial')              #;
          #  self.match('Palavra Reservada')     #bool
          #  self.match('Identificador')         #numMaior
          #  self.match('Operador')              #-
          #  self.match('Especial')              #>
          #  self.match('Identificador')         #ok
          #  self.match('Especial')              #;
          #  self.match('Palavra Reservada')     #num_int
          #  self.match('Identificador')         #soma
          #  self.match('Operador')              #-
          #  self.match('Especial')              #>
          #  self.match('Identificador')         #num1
          #  self.match('Operador')              #+
          #  self.match('Identificador')         #num2
          #  self.match('Especial')              #;
          #  self.match('Palavra Reservada')     #case
          #  self.match('Especial')              #[
          #  self.match('Identificador')         #num1
          #  self.match('Especial')              #>=
          #  self.match('Identificador')         #num2
          #  self.match('Especial')              #]
          #  self.match('Especial')              #<
          #  self.match('Palavra Reservada')     #puts
          #  self.match('Especial')              #<
          #  self.match('String')                #"palavra"
          #  self.match('Especial')              #>
          #  self.match('Especial')              #;
          #  self.match('Especial')              #>
          #  self.match('Identificador')         #ordo
          #  self.match('Especial')              #<
          #  self.match('Identificador')         #numMaior
          #  self.match('Operador')              #-
          #  self.match('Especial')              #>
          #  self.match('Lógico')                #!
          #  self.match('Identificador')         #numMaior
          #  self.match('Especial')              #->
          #  self.match('Palavra Reservada')     #take
          #  self.match('Número Inteiro')        #0
          #  self.match('Especial')              #;
          #  self.match('Especial')              #>

          #  self.analisar_escopo()
            
          #  if self.indice_token_atual < len(self.tokens):
          #      raise SyntaxError(f"Token inesperado {self.tokens[self.indice_token_atual]['tipo']} na linha {self.tokens[self.indice_token_atual]#['linha']}")
        #except SyntaxError as e:
        #    print(e)
    def analisar_programa(self):
        try:
            while self.indice_token_atual < len(self.tokens):
                token = self.tokens[self.indice_token_atual]['tipo']
                self.match(token)
        except SyntaxError as e:
            print(e)

    def analisar_escopo(self):
        while self.indice_token_atual < len(self.tokens):
            token = self.tokens[self.indice_token_atual]['tipo']
            if token in ('num_int', 'num_flu', 'text', 'bool'):
                self.analisar_declaracao()
            elif token == 'Palavra Reservada' and self.tokens[self.indice_token_atual]['lexema'] == 'vacuum':
                self.match('Palavra Reservada')  # 'vacuum'
            elif token == 'Palavra Reservada' and self.tokens[self.indice_token_atual]['lexema'] == 'case':
                self.analisar_desvio()
            else:
                raise SyntaxError(f"Token inesperado {token} na linha {self.tokens[self.indice_token_atual]['linha']}")

    def analisar_declaracao(self):
        tipo_variavel = self.tokens[self.indice_token_atual]['tipo']
        self.match(tipo_variavel)
        self.match('Identificador')
        self.match('Caractere Especial')  # ';'

    def analisar_desvio(self):
        self.match('Palavra Reservada')  # 'case'
        self.match('Caractere Especial')  # '['
        self.analisar_exp_relacional()
        self.match('Caractere Especial')  # ']'
        self.match('Caractere Especial')  # '<'
        self.analisar_escopo()
        self.match('Caractere Especial')  # '>'
        self.analisar_desvio2()

    def analisar_exp_relacional(self):
        # Implementar a análise da expressão relacional
        pass

    def analisar_desvio2(self):
        while self.indice_token_atual < len(self.tokens):
            token = self.tokens[self.indice_token_atual]['tipo']
            if token == 'Palavra Reservada' and self.tokens[self.indice_token_atual]['lexema'] == 'case':
                self.analisar_desvio()
            else:
                return  # ε

def main():
    path = "teste.txt"
    analisador_sintatico = AnalisadorSintatico(path)
    analisador_sintatico.tokens = analisador_sintatico.analisador_lexico.get_tabela_simbolos()  # Carregar os tokens
    analisador_sintatico.analisar_programa()
    print("Análise concluída com sucesso.")

if __name__ == "__main__":
    main()
