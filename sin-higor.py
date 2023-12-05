from lexico import AnalisadorLexico


class AnalisadorSintatico:
    def __init__(self, tabela_simbolos):
        self.tabela_simbolos = tabela_simbolos
        self.indice_atual = 0
        self.token_atual = None

    def proximo_token(self):
        if self.indice_atual < len(self.tabela_simbolos):
            self.token_atual = self.tabela_simbolos[self.indice_atual]
            self.indice_atual += 1
        else:
            self.token_atual = None

    def casar(self, tipo_esperado):
        if self.token_atual and self.token_atual['tipo'] == tipo_esperado:
            self.proximo_token()
        else:
            print(f"Erro sintático: Token inesperado. Tipo esperado: {tipo_esperado}, Tipo encontrado: {self.token_atual['tipo']}")

    def analisar(self):
        self.proximo_token()  # Inicializa o token_atual
        self.programa()

    def programa(self):
        self.casar('PALAVRA_RESERVADA')
        self.casar('PALAVRA_RESERVADA')  
        self.casar('SIM_ESPECIAL')
        self.lista_de_declaracao()
        self.escopo()

    def lista_de_declaracao(self):
        self.declaracao()

        # Verifica se há mais declarações separadas por '|'
        while self.token_atual and self.token_atual['lexema'] == '|':
            self.casar('SIM_ESPECIAL')  # Casar o símbolo '|'
            self.declaracao()

    def declaracao(self):
        if self.token_atual and self.token_atual['tipo'] == 'PALAVRA_RESERVADA':
            if self.token_atual['lexema'] in ['text', 'num_flu', 'num_int', 'bool' ]:
                self.tipo_var()
                self.variavel()
                self.casar('ATRIBUICAO', '=>')  # Casar o símbolo '=>'
                self.conteudo()
                self.casar('SIM_ESPECIAL', ';')  # Casar o símbolo ';'
            else:
                print(f"Erro sintático: Tipo de variável esperado, Tipo encontrado: {self.token_atual['lexema'] if self.token_atual else 'EOF'}")
        else:
            print(f"Erro sintático: Tipo de variável esperado, Tipo encontrado: {self.token_atual['tipo'] if self.token_atual else 'EOF'}")

    def tipo_var(self):
        if self.token_atual and self.token_atual['tipo'] == 'PALAVRA_RESERVADA':
            lexema = self.token_atual['lexema']
            if lexema in ['text', 'num_flu', 'num_int', 'bool']:
                self.proximo_token()
            else:
                print(f"Erro sintático: Tipo de variável esperado, Tipo encontrado: {lexema if lexema else 'EOF'}")
        else:
            print(f"Erro sintático: Tipo de variável esperado, Tipo encontrado: {self.token_atual['tipo'] if self.token_atual else 'EOF'}")

    def variavel(self):
        self.casar('IDENTIFICADOR')

    def conteudo(self):
        if self.token_atual and self.token_atual['tipo'] in ['IDENTIFICADOR', 'NUM_FLU', 'NUM_INT', 'TEXT']:
            self.casar(self.token_atual['tipo'])
        else:
            print(f"Erro sintático: Conteúdo esperado, Tipo encontrado: {self.token_atual['tipo'] if self.token_atual else 'EOF'}")

    def casar(self, tipo_esperado, lexema_esperado=None):
        if self.token_atual and self.token_atual['tipo'] == tipo_esperado and (lexema_esperado is None or self.token_atual['lexema'] == lexema_esperado):
            self.proximo_token()
        else:
            print(f"Erro sintático: Token inesperado. Tipo esperado: {tipo_esperado}, Lexema esperado: {lexema_esperado if lexema_esperado else 'qualquer'}, "
                  f"Tipo encontrado: {self.token_atual['tipo'] if self.token_atual else 'EOF'}, Lexema encontrado: {self.token_atual['lexema'] if self.token_atual else 'EOF'}")

    def analisar(self):
        self.proximo_token()  #inicializa o token_atual
        self.programa()

    def laco(self):
        if self.token_atual and self.token_atual['lexema'] == 'to':
            self.casar('PALAVRA_RESERVADA', 'to')
            self.casar('SIM_ESPECIAL', '[')
            self.atribuicao()
            self.conteudo()
            self.simbolo_relacional()
            self.conteudo()
            self.casar('SIM_ESPECIAL', ';')
            self.variavel()
            self.casar('SIM_ESPECIAL', '<<')
            self.exp_aritmetica()
            self.casar('SIM_ESPECIAL', ']')
            self.casar('SIM_ESPECIAL', '<')
            self.escopo()
            self.casar('SIM_ESPECIAL', '>')
        elif self.token_atual and self.token_atual['lexema'] == 'when':
            self.casar('PALAVRA_RESERVADA', 'when')
            self.casar('SIM_ESPECIAL', '[')
            self.exp()
            self.casar('SIM_ESPECIAL', ']')
            self.casar('SIM_ESPECIAL', '<')
            self.escopo()
            self.casar('SIM_ESPECIAL', '>')
        elif self.token_atual and self.token_atual['lexema'] == 'take':
            self.casar('PALAVRA_RESERVADA', 'take')
        else:
            print(f"Erro sintático: Laco esperado, Tipo encontrado: {self.token_atual['lexema'] if self.token_atual else 'EOF'}")

    def atribuicao(self):
        self.tipo_var()
        self.variavel()
        self.casar('ATRIBUICAO', '=>')
        self.conteudo()
        self.casar('SIM_ESPECIAL', ';')

    def simbolo_relacional(self):
        if self.token_atual and self.token_atual['lexema'] in ['<<', '>>', '>=', '<=', '==', '!=', 'ok', 'notok']:
            self.casar('SIMBOLO_RELACIONAL')
        else:
            print(f"Erro sintático: Símbolo relacional esperado, Tipo encontrado: {self.token_atual['lexema'] if self.token_atual else 'EOF'}")

    def exp_aritmetica(self):
        self.exp()
        self.termo()

    def exp(self):
        self.logico()
        self.termo_logico()

    def termo(self):
        if self.token_atual and self.token_atual['lexema'] in ['*', '/', '//']:
            self.casar('SIM_ESPECIAL')  # Casar operador aritmético
            self.fator()
            self.termo()
        else:
            print(f"Erro sintático: Operador aritmético esperado, Tipo encontrado: {self.token_atual['lexema'] if self.token_atual else 'EOF'}")

    def termo_logico(self):
        if self.token_atual and self.token_atual['lexema'] == '||':
            self.casar('SIM_ESPECIAL', '||')
            self.expressao_logica()
            self.termo_logico()
        else:
            print(f"Erro sintático: Operador lógico esperado, Tipo encontrado: {self.token_atual['lexema'] if self.token_atual else 'EOF'}")

    def fator(self):
        if self.token_atual and self.token_atual['lexema'] == '[':
            self.casar('SIM_ESPECIAL', '[')
            self.exp_aritmetica()
            self.casar('SIM_ESPECIAL', ']')
        elif self.token_atual and self.token_atual['tipo'] in ['IDENTIFICADOR', 'NUM_FLU', 'NUM_INT']:
            self.casar(self.token_atual['tipo'])
        else:
            print(f"Erro sintático: Fator esperado, Tipo encontrado: {self.token_atual['lexema'] if self.token_atual else 'EOF'}")

    def logico(self):
        self.expressao_logica()
        self.termo_logico()

    def expressao_logica(self):
        self.expressao_logica3()
        self.expressao_logica2()

    def expressao_logica2(self):
        if self.token_atual and self.token_atual['lexema'] == '&&':
            self.casar('SIM_ESPECIAL', '&&')
            self.expressao_logica3()
            self.expressao_logica2()

    def expressao_logica3(self):
        if self.token_atual and self.token_atual['lexema'] == '!':
            self.casar('SIM_ESPECIAL', '!')
            self.relacional()
        else:
            self.relacional()


    def escopo(self):
        #Implemente a regra de produção correspondente
        pass

    # ... (continue com outras regras de produção)

if __name__ == "__main__":
  
    analisador_lexico = AnalisadorLexico("cod.txt")
    tabela_simbolos = analisador_lexico.get_tabela_simbolos()

  
    analisador_sintatico = AnalisadorSintatico(tabela_simbolos)
    analisador_sintatico.analisar()
