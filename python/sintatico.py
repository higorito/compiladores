from lexico2 import AnalisadorLexico

class AnalisadorSintatico:
    def __init__(self, analisador_lexico):
        self.analisador_lexico = analisador_lexico
        self.index_token = 0
        self.erro = False

    def proximo_token(self):
        tabela_simbolos = self.analisador_lexico.get_tabela_simbolos()
        if self.index_token < len(tabela_simbolos):
            self.token_atual = tabela_simbolos[self.index_token]
            self.index_token += 1
        else:
            self.token_atual = None

    def casar(self, tipo_esperado):
        if self.token_atual and self.token_atual['tipo'] == tipo_esperado:
            self.proximo_token()
        else:
            self.erro = True
            print(f"Erro de sintaxe na linha {self.token_atual['linha']} - Esperado {tipo_esperado}, encontrado {self.token_atual['tipo']}")

    def main(self):
        self.proximo_token()
        self.programa()

        if self.token_atual is not None:
            self.erro = True
            print(f"Erro de sintaxe na linha {self.token_atual['linha']} - Símbolo não esperado {self.token_atual['lexema']}")

        if not self.erro:
            print("Análise sintática concluída com sucesso.")


    def programa(self):
        if self.token_atual and self.token_atual['tipo'] == 'Palavra Reservada' and self.token_atual['lexema'] == 'main':
            self.casar('Palavra Reservada')
            self.casar('Operador')
            self.lista_declaracao()
            self.casar('Operador')
            self.escopo()
        else:
            self.erro = True
            if self.token_atual:
                print(f"Erro de sintaxe na linha {self.token_atual['linha']} - Esperado 'main', encontrado {self.token_atual['lexema']}")
            else:
                print("Erro de sintaxe - Fim de arquivo inesperado")


    def lista_declaracao(self):
        if self.token_atual['tipo'] == 'Palavra Reservada' and self.token_atual['lexema'] in ['num_int', 'num_flu', 'text']:
            self.declaracao()
            self.lista_declaracao()
        elif self.token_atual['tipo'] == 'Palavra Reservada' and self.token_atual['lexema'] == 'vacuum':
            self.casar('Palavra Reservada')
        else:
            pass  # ε (vazio)

    def declaracao(self):
        tipo_var = self.token_atual['lexema']
        self.casar('Palavra Reservada')
        self.variavel()
        self.casar('Operador')
        if tipo_var == 'text':
            self.texto()
        elif tipo_var in ['num_int', 'num_flu']:
            self.exp_aritmetica()

    def variavel(self):
        self.casar('Identificador')

    def escopo(self):
        if self.token_atual['tipo'] == 'Operador' and self.token_atual['lexema'] == '{':
            self.casar('Operador')
            self.escopo()
            self.casar('Operador')
        else:
            self.comando()
            self.escopo()

    def comando(self):
        if self.token_atual['tipo'] == 'Palavra Reservada':
            if self.token_atual['lexema'] == 'tetin':
                self.entrada()
            elif self.token_atual['lexema'] == 'texout':
                self.saida()
            elif self.token_atual['lexema'] == 'case':
                self.desvio()
            elif self.token_atual['lexema'] == 'ord':
                self.atribuicao()
            elif self.token_atual['lexema'] == 'when':
                self.laco()
            elif self.token_atual['lexema'] == 'take':
                self.casar('Palavra Reservada')
            else:
                self.erro = True
                print(f"Erro de sintaxe na linha {self.token_atual['linha']} - Comando inválido: {self.token_atual['lexema']}")
        else:
            self.erro = True
            print(f"Erro de sintaxe na linha {self.token_atual['linha']} - Comando inválido: {self.token_atual['lexema']}")

    def entrada(self):
        self.casar('Palavra Reservada')
        self.casar('Caractere Especial')
        self.variavel()
        self.casar('Caractere Especial')

    def saida(self):
        self.casar('Palavra Reservada')
        self.casar('Caractere Especial')
        if self.token_atual['tipo'] == 'String':
            self.texto()
        else:
            self.exp_aritmetica()
        self.casar('Caractere Especial')

    def exp_aritmetica(self):
        self.termo()
        self.exp_aritmetica2()

    def exp_aritmetica2(self):
        if self.token_atual['tipo'] == 'Operador Aritmético':
            self.casar('Operador Aritmético')
            self.termo()
            self.exp_aritmetica2()
        else:
            pass  # ε (vazio)

    def termo(self):
        self.fator()
        self.termo2()

    def termo2(self):
        if self.token_atual['tipo'] == 'Operador Aritmético':
            self.casar('Operador Aritmético')
            self.fator()
            self.termo2()
        else:
            pass  # ε (vazio)

    def fator(self):
        if self.token_atual['tipo'] == 'Caractere Especial' and self.token_atual['lexema'] == '(':
            self.casar('Caractere Especial')
            self.exp_aritmetica()
            self.casar('Caractere Especial')
        elif self.token_atual['tipo'] == 'Identificador':
            self.variavel()
        elif self.token_atual['tipo'] in ['Número Inteiro', 'Número Flutuante']:
            self.numero()
        elif self.token_atual['tipo'] == 'ID':
            self.funcao()
        else:
            self.erro = True
            print(f"Erro de sintaxe na linha {self.token_atual['linha']} - Fator inválido: {self.token_atual['lexema']}")

    def funcao(self):
        self.casar('ID')
        self.casar('Caractere Especial')
        self.argumento()
        self.casar('Caractere Especial')

    def argumento(self):
        if self.token_atual['tipo'] != 'Caractere Especial' or self.token_atual['lexema'] != ')':
            self.exp_aritmetica()
            self.argumento2()

    def argumento2(self):
        if self.token_atual['tipo'] == 'Caractere Especial' and self.token_atual['lexema'] == ',':
            self.casar('Caractere Especial')
            self.exp_aritmetica()
            self.argumento2()
        else:
            pass  # ε (vazio)

    def texto(self):
        self.casar('String')

    def termo_logico(self):
        if self.token_atual['tipo'] == 'Operador Lógico' and self.token_atual['lexema'] == '||':
            self.casar('Operador Lógico')
            self.expressao_logica()
            self.termo_logico()
        else:
            pass  # ε (vazio)

    def expressao_logica(self):
        self.expressao_logica3()
        self.expressao_logica2()

    def expressao_logica2(self):
        if self.token_atual['tipo'] == 'Operador Lógico' and self.token_atual['lexema'] == '&&':
            self.casar('Operador Lógico')
            self.expressao_logica3()
            self.expressao_logica2()
        else:
            pass  # ε (vazio)

    def expressao_logica3(self):
        if self.token_atual['tipo'] == 'Operador Lógico' and self.token_atual['lexema'] == '!':
            self.casar('Operador Lógico')
            self.relacional()
        else:
            self.relacional()

    def sim_relacional(self):
        if self.token_atual['tipo'] == 'Operador Relacional':
            self.casar('Operador Relacional')
        else:
            self.erro = True
            print(f"Erro de sintaxe na linha {self.token_atual['linha']} - Operador Relacional esperado")

    def numero(self):
        if self.token_atual['tipo'] == 'Número Inteiro':
            self.casar('Número Inteiro')
        elif self.token_atual['tipo'] == 'Número Flutuante':
            self.casar('Número Flutuante')
        else:
            self.erro = True
            print(f"Erro de sintaxe na linha {self.token_atual['linha']} - Número esperado")

    def desvio(self):
        self.casar('Palavra Reservada')
        self.casar('Caractere Especial')
        self.exp_aritmetica()
        self.casar('Caractere Especial')
        self.casar('Caractere Especial')
        self.escopo()
        self.desvio2()

    def desvio2(self):
        if self.token_atual['tipo'] == 'Palavra Reservada' and self.token_atual['lexema'] == 'else':
            self.casar('Palavra Reservada')
            self.casar('Caractere Especial')
            self.escopo()

    def atribuicao(self):
        self.variavel()
        self.casar('Atribuição')
        self.conteudo()
        self.casar('Caractere Especial')

    def conteudo(self):
        if self.token_atual['tipo'] == 'String':
            self.texto()
        else:
            self.exp_aritmetica()

    def laco(self):
        if self.token_atual['tipo'] == 'Palavra Reservada' and self.token_atual['lexema'] == 'to':
            self.casar('Palavra Reservada')
            self.atribuicao()
            self.conteudo()
            self.sim_relacional()
            self.conteudo()
            self.casar('Caractere Especial')
            self.casar('Caractere Especial')
            self.variavel()
            self.casar('Operador')
            self.casar('Operador')
            self.exp_aritmetica()
            self.casar('Caractere Especial')
            self.escopo()
        elif self.token_atual['tipo'] == 'Palavra Reservada' and self.token_atual['lexema'] == 'when':
            self.casar('Palavra Reservada')
            self.casar('Caractere Especial')
            self.exp_aritmetica()
            self.casar('Caractere Especial')
            self.escopo()
        elif self.token_atual['tipo'] == 'Palavra Reservada' and self.token_atual['lexema'] == 'take':
            self.casar('Palavra Reservada')
        else:
            self.erro = True
            print(f"Erro de sintaxe na linha {self.token_atual['linha']} - Laco inválido: {self.token_atual['lexema']}")
            
if __name__ == "__main__":
    analisador_lexico = AnalisadorLexico("teste.txt")
    analisador_sintatico = AnalisadorSintatico(analisador_lexico)
    analisador_sintatico.main()
