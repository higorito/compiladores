from lexico2 import AnalisadorLexico

class No:
    def __init__(self, tipo, lexema=None):
        self.tipo = tipo
        self.lexema = lexema
        self.filhos = []

class AnalisadorSintatico:
    def __init__(self, path):
        self.analisador_lexico = AnalisadorLexico(path)
        self.tokens = self.analisador_lexico.get_tabela_simbolos()
        self.indice_token_atual = 0

    def match(self, tipo_esperado):
        if self.indice_token_atual < len(self.tokens):
            tipo_token_atual = self.tokens[self.indice_token_atual]['tipo']
            lexema_token_atual = self.tokens[self.indice_token_atual]['lexema']
            if tipo_token_atual == tipo_esperado:
                self.indice_token_atual += 1
                return No(tipo_token_atual, lexema_token_atual)
            else:
                raise SyntaxError(f"Token inesperado {tipo_token_atual} na linha {self.tokens[self.indice_token_atual]['linha']}")

    def analisar_programa(self):
        no_programa = No('Programa')
        try:
            no_programa.filhos.append(self.match('Palavra Reservada'))  # 'fn'
            no_programa.filhos.append(self.match('Palavra Reservada'))  # 'main'
            no_programa.filhos.append(self.match('Palavra Reservada'))  # 'vaccum'
            no_programa.filhos.append(self.match('Especial'))  # '<'
            no_programa.filhos.append(self.match('Palavra Reservada'))  # 'num_int'
            no_programa.filhos.append(self.match('Identificador'))  # 'num1'
            no_programa.filhos.append(self.match('Operador'))  # '-'
            no_programa.filhos.append(self.match('Especial'))  # '>'
            no_programa.filhos.append(self.match('Número Inteiro'))  # '4'
            no_programa.filhos.append(self.match('Especial'))  # ';'
            
            # ADICIONAR MAIS FILHOS AQUI

            self.analisar_escopo(no_programa)

            if self.indice_token_atual < len(self.tokens):
                raise SyntaxError(f"Token inesperado {self.tokens[self.indice_token_atual]['tipo']} na linha {self.tokens[self.indice_token_atual]['linha']}")
        except SyntaxError as e:
            print(e)

    def analisar_escopo(self, no_pai):
        no_escopo = No('Escopo')
        while self.indice_token_atual < len(self.tokens):
            token = self.tokens[self.indice_token_atual]['tipo']
            if token in ('num_int', 'num_flu', 'text', 'bool'):
                no_escopo.filhos.append(self.analisar_declaracao())
            elif token == 'Palavra Reservada' and self.tokens[self.indice_token_atual]['lexema'] == 'vacuum':
                no_escopo.filhos.append(self.match('Palavra Reservada'))  # 'vacuum'
            elif token == 'Palavra Reservada' and self.tokens[self.indice_token_atual]['lexema'] == 'case':
                no_escopo.filhos.append(self.analisar_desvio())
            else:
                raise SyntaxError(f"Token inesperado {token} na linha {self.tokens[self.indice_token_atual]['linha']}")
        
        no_pai.filhos.append(no_escopo)

    def analisar_declaracao(self):
        no_declaracao = No('Declaracao')
        tipo_variavel = self.match('Palavra Reservada')
        identificador = self.match('Identificador')
        self.match('Caractere Especial')  # ';'

        no_declaracao.filhos.append(tipo_variavel)
        no_declaracao.filhos.append(identificador)
        return no_declaracao

    def analisar_desvio(self):
        no_desvio = No('Desvio')
        no_desvio.filhos.append(self.match('Palavra Reservada'))  # 'case'
        no_desvio.filhos.append(self.match('Caractere Especial'))  # '['
        # ADICIONAR MAIS FILHOS AQUI
        self.analisar_exp_relacional(no_desvio)
        no_desvio.filhos.append(self.match('Caractere Especial'))  # ']'
        no_desvio.filhos.append(self.match('Caractere Especial'))  # '<'
        self.analisar_escopo(no_desvio)
        no_desvio.filhos.append(self.match('Caractere Especial'))  # '>'

        self.analisar_desvio2(no_desvio)

        return no_desvio
 
    def analisar_exp_relacional(self, no_pai): # implementar a análise da expressão relacional
        
        pass

    def analisar_desvio2(self, no_pai):
        no_desvio2 = No('Desvio2')
        while self.indice_token_atual < len(self.tokens):
            token = self.tokens[self.indice_token_atual]['tipo']
            if token == 'Palavra Reservada' and self.tokens[self.indice_token_atual]['lexema'] == 'case':
                no_desvio2.filhos.append(self.analisar_desvio())
            else:
                return  # ε
        
        no_pai.filhos.append(no_desvio2)

def main():
    path = "teste.txt"
    analisador_sintatico = AnalisadorSintatico(path)
    analisador_sintatico.analisar_programa()
    print("Análise concluída com sucesso.")

if __name__ == "__main__":
    main()
