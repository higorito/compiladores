from lexico import AnalisadorLexico

class AnalisadorSintatico:
    def __init__(self, tabela_simbolos):
        self.tokens = tabela_simbolos
        self.posicao_atual = 0

    def casar(self, tipo_esperado):
        if self.posicao_atual < len(self.tokens):
            token_atual = self.tokens[self.posicao_atual]
            if tipo_esperado == 'IDENTIFICADOR':
                if token_atual['tipo'] in ['IDENTIFICADOR', 'PALAVRA_RESERVADA']:
                    self.posicao_atual += 1
                else:
                    print(f"Erro sintático: Esperado '{tipo_esperado}', encontrado '{token_atual['tipo']}' na linha {token_atual['linha']}")
                    self.posicao_atual = len(self.tokens)
            else:
                if token_atual['tipo'] == tipo_esperado:
                    self.posicao_atual += 1
                else:
                    print(f"Erro sintático: Esperado '{tipo_esperado}', encontrado '{token_atual['tipo']}' na linha {token_atual['linha']}")
                    self.posicao_atual = len(self.tokens)
        else:
            print(f"Erro sintático: Fim inesperado do código")

    def main(self):
        self.casar('main')
        self.lista_declaracao()
        self.casar('<')
        self.escopo()

    def lista_declaracao(self):
        while self.posicao_atual < len(self.tokens) and self.tokens[self.posicao_atual]['tipo'] != 'vacuum':
            self.declaracao()

    def declaracao(self):
        self.tipo_var()
        self.casar('IDENTIFICADOR')
        self.casar(';')

    def tipo_var(self):
        tipo = self.tokens[self.posicao_atual]['tipo']
        if tipo in ['text', 'num_int', 'num_flu']:
            self.casar(tipo)
        else:
            print(f"Erro sintático: Tipo inválido '{tipo}' na linha {self.tokens[self.posicao_atual]['linha']}")

    def escopo(self):
        while self.posicao_atual < len(self.tokens) and self.tokens[self.posicao_atual]['tipo'] != '>':
            token_atual = self.tokens[self.posicao_atual]
            if token_atual['tipo'] == 'escopo':
                self.casar('escopo')
            elif token_atual['tipo'] == 'comando':
                self.comando()
            else:
                self.posicao_atual += 1

    def comando(self):
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] == 'entrada':
            self.entrada()
        elif token_atual['tipo'] == 'saida':
            self.saida()
        elif token_atual['tipo'] == 'desvio':
            self.desvio()
        elif token_atual['tipo'] == 'atribuicao':
            self.atribuicao()
        elif token_atual['tipo'] == 'laco':
            self.laco()

    def entrada(self):
        self.casar('entrada')
        self.casar('textin')
        self.casar('[')
        self.variavel()
        self.casar(']')
        self.casar(';')

    def saida(self):
        self.casar('saida')
        self.casar('textout')
        self.casar('[')
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] == 'texto':
            self.texto()
        elif token_atual['tipo'] == 'expAritmetica':
            self.exp_aritmetica()
        else:
            print(f"Erro sintático: Esperado 'texto' ou 'expAritmetica', encontrado '{token_atual['tipo']}' na linha {token_atual['linha']}")
        self.casar(']')
        self.casar(';')

    def exp_aritmetica(self):
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] == 'exp':
            self.exp()
        elif token_atual['tipo'] == 'termo':
            self.termo()

    def exp(self):
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] == 'logico':
            self.logico()
        elif token_atual['tipo'] in ['ok', 'notok']:
            self.casar(token_atual['tipo'])
        else:
            print(f"Erro sintático: Esperado 'logico', 'ok' ou 'notok', encontrado '{token_atual['tipo']}' na linha {token_atual['linha']}")

    def logico(self):
        self.expressao_logica()
        self.termo_logico()

    def termo_logico(self):
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] == '||':
            self.casar('||')
            self.expressao_logica()
            self.termo_logico()

    def expressao_logica(self):
        self.expressao_logica3()
        self.expressao_logica2()

    def expressao_logica2(self):
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] == '&&':
            self.casar('&&')
            self.expressao_logica3()
            self.expressao_logica2()
        else:
            self.casar('vacuum')

    def expressao_logica3(self):
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] == '!':
            self.casar('!')
            self.relacional()
        else:
            self.relacional()

    def relacional(self):
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] == '[':
            self.casar('[')
            self.logico()
            self.casar(']')
        elif token_atual['tipo'] == 'termoRelacional':
            self.termo_relacional()

    def termo_relacional(self):
        self.conteudo()
        self.termo_relacional2()

    def termo_relacional2(self):
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] in ['<<', '>>', '<<<', '>>>', '==', '!=', 'ok', 'notok']:
            self.casar(token_atual['tipo'])
            self.conteudo()
        else:
            self.casar('vacuum')

    def desvio(self):
        self.casar('desvio')
        self.casar('(')
        self.exp()
        self.casar(')')
        self.casar('<')
        self.escopo()
        self.desvio2()

    def desvio2(self):
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] == 'caseNot':
            self.casar('caseNot')
            self.casar('<')
            self.escopo()
        elif token_atual['tipo'] == 'case':
            self.casar('case')
            self.casar('(')
            self.exp()
            self.casar(')')
            self.casar('<')
            self.escopo()
            self.desvio2()

    def atribuicao(self):
        self.variavel()
        self.casar('conteudo')
        self.casar(';')

    def laco(self):
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] == 'to':
            self.casar('to')
            self.casar('(')
            self.atribuicao()
            self.conteudo()
            self.simbolo_relacional()
            self.conteudo()
            self.casar(';')
            self.variavel()
            self.simbolo_relacional()
            self.exp_aritmetica()
            self.casar(')')
            self.casar('<')
            self.escopo()
        elif token_atual['tipo'] == 'when':
            self.casar('when')
            self.casar('(')
            self.exp()
            self.casar(')')
            self.casar('<')
            self.escopo()
        elif token_atual['tipo'] == 'take':
            self.casar('take')
            self.casar(';')

    def variavel(self):
        self.casar('ID')

    def conteudo(self):
        token_atual = self.tokens[self.posicao_atual]
        if token_atual['tipo'] == 'texto':
            self.texto()
        elif token_atual['tipo'] == 'exp':
            self.exp()

    def texto(self):
        self.casar('text')

    def simbolo_relacional(self):
        self.casar('simbolo_relacional')


if __name__ == "__main__":
    analisador_lexico = AnalisadorLexico("cod.txt")
    tabela_simbolos = analisador_lexico.get_tabela_simbolos()

    analisador_sintatico = AnalisadorSintatico(tabela_simbolos)
    analisador_sintatico.main()
