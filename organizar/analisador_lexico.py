class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.posicao = 0  
        self.linha = 1  

        self.tabela_tokens = {}

        self.palavras_reservadas = ["fn","main", "vacuum", "case", "ordo", "to", "when", "textin", "textout", "puts", "take", "num_int", "num_flu"]

        self.operadores_aritmeticos = ["+", "-", "/", "*", "//", "**"]

        self.operadores_logicos = ["&&", "||", "!"]

        self.operadores_relacionais = ["=>",">>", "<<", ">=", "=<", "==", "=!"]

        self.simbolos_especiais = ["<", ">", "[", "]", ";"]

    def adicionar_token(self, token_tipo, lexema): #aqui vai colocar na tabela de tokens formato tipo_lexema
        chave = f"{token_tipo}_{lexema}"
        self.tabela_tokens[chave] = lexema


    def proximo_token(self):
        while self.posicao < len(self.codigo_fonte):
            caractere = self.codigo_fonte[self.posicao]

            if caractere.isspace():
                self.atualizar_posicao()
                continue

            
            if caractere.isalpha():
                lexema = self.obter_identificador()

                #-------------------------------------------------#
                if lexema in self.palavras_reservadas:
                    self.adicionar_token("PR", lexema)  #pr é palavra reservada
                    return f"PR_{lexema}"
                #-------------------------------------------------#
                if lexema == "ok" or lexema == "notok":
                    self.adicionar_token("BOOLEANO", lexema)
                    return f"BOOLEANO_{lexema}"

                #-------------------------------------------------#
                self.adicionar_token("IDENTIFICADOR", lexema)
                return f"IDENTIFICADOR, {lexema}"

            
            if caractere.isdigit():
                lexema = self.obter_numero()
                self.adicionar_token("NUM", str(lexema))  
                return f"NUM, {lexema}"
            
            if caractere == '.' and self.posicao + 1 < len(self.codigo_fonte) and self.codigo_fonte[self.posicao + 1].isdigit():
                lexema = self.obter_numero_decimal()
                self.adicionar_token("NUM_FLU", str(lexema))  
                return f"NUM_FLU, {lexema}"

           #-------------------------------------------------#
            for op in self.operadores_aritmeticos:
                if self.codigo_fonte.startswith(op, self.posicao):
                    self.posicao += len(op)
                    self.adicionar_token("OP_aritmetico", op)
                    return f"OP_aritmetico_{op}"
            #-------------------------------------------------#
            for op in self.operadores_logicos:
                if self.codigo_fonte.startswith(op, self.posicao):
                    self.posicao += len(op)
                    self.adicionar_token("OP_logico", op)
                    return f"OP_logico_{op}"

           #-------------------------------------------------#
            for op in self.operadores_relacionais:
                if self.codigo_fonte.startswith(op, self.posicao):
                    self.posicao += len(op)
                    if op == "=>":
                        self.adicionar_token("ATRIBUICAO", op)
                        return f"ATRIBUICAO_{op}"
                    else:
                        self.adicionar_token("OP_relacional", op)
                        return f"OP_relacional_{op}"
                    
            #-------------------------------------------------#
            for simbolo in self.simbolos_especiais:
                if self.codigo_fonte.startswith(simbolo, self.posicao):
                    self.posicao += len(simbolo)
                    if simbolo == ";":
                        self.adicionar_token("PONTO_VIRGULA", simbolo)
                        return f"PONTO_VIRGULA_{simbolo}"
                    if simbolo == "[":
                        self.adicionar_token("ABRE_COLCHETE", simbolo)
                        return f"ABRE_COLCHETE_{simbolo}"
                    if simbolo == "]":
                        self.adicionar_token("FECHA_COLCHETE", simbolo)
                        return f"FECHA_COLCHETE_{simbolo}"
                    if simbolo == "<":
                        self.adicionar_token("ABRE_ESCOPO", simbolo)
                        return f"ABRE_ESCOPO_{simbolo}"
                    if simbolo == ">":
                        self.adicionar_token("FECHA_ESCOPO", simbolo)
                        return f"FECHA_ESCOPO_{simbolo}"
                    

            # Se nenhum token foi encontrado, avançar para o próximo caractere
            self.atualizar_posicao()

        return None

    def obter_identificador(self):
        inicio = self.posicao
        while self.posicao < len(self.codigo_fonte) and (self.codigo_fonte[self.posicao].isalpha() or self.codigo_fonte[self.posicao].isdigit() or self.codigo_fonte[self.posicao] == '_'):
            self.posicao += 1
        return self.codigo_fonte[inicio:self.posicao]

    def obter_numero(self):
        inicio = self.posicao
        while self.posicao < len(self.codigo_fonte) and self.codigo_fonte[self.posicao].isdigit():
            self.posicao += 1
        return int(self.codigo_fonte[inicio:self.posicao])
    
    def obter_numero_decimal(self):
        inicio = self.posicao
        self.posicao += 1  #avacando para o primeiro dígito após o ponto
        while self.posicao < len(self.codigo_fonte) and self.codigo_fonte[self.posicao].isdigit():
            self.posicao += 1
        return float(self.codigo_fonte[inicio:self.posicao])

    def atualizar_posicao(self):
        if self.codigo_fonte[self.posicao] == '\n':
            self.linha += 1
        self.posicao += 1



def main():
    with open("programa.if", "r") as arquivo:
        codigo_fonte = arquivo.read()

    analisador_lexico = AnalisadorLexico(codigo_fonte)

    while True:
        token = analisador_lexico.proximo_token()
        if token is None:
            break
        print(token)

if __name__ == "__main__":
    main()