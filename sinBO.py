class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def consumir_tokens(self, quantidade=1):
        tokens_consumidos = self.tokens[self.posicao:self.posicao + quantidade]
        self.posicao += quantidade
        return tokens_consumidos

    def erro_sintatico(self, mensagem):
        raise SyntaxError(f"Erro sintático: {mensagem} na linha {self.tokens[self.posicao]['linha']}")
    

    def inicio(self):
        print(f"DEBUG: Verificando token main na linha {self.tokens[self.posicao]['linha']}")
        if self.tokens[self.posicao]['tipo'] == 'PALAVRA_RESERVADA' and self.tokens[self.posicao]['valor'] == 'main':
            self.consumir_tokens()  
            print("DEBUG: Token main encontrado com sucesso.")
            if self.tokens[self.posicao]['tipo'] == 'SIM_ESPECIAL' and self.tokens[self.posicao]['valor'] == '@':
                print("DEBUG: Token '@' encontrado com sucesso.")
                self.lista_de_declaracao()
                print(f"DEBUG: Verificando token escopo na linha {self.tokens[self.posicao]['linha']}")
                if self.tokens[self.posicao]['tipo'] == 'PALAVRA_RESERVADA' and self.tokens[self.posicao]['valor'] == 'escopo' and \
                   self.consumir_tokens(2)[1]['tipo'] == 'SIM_ESPECIAL' and self.consumir_tokens(2)[1]['valor'] == '@':
                    
                    
                    if self.posicao == len(self.tokens) or (self.posicao + 1 == len(self.tokens) and self.tokens[-1]['tipo'] == 'SIM_ESPECIAL' and self.tokens[-1]['valor'] == '@'):
                        print("Análise sintática bem-sucedida.")
                        
                       
                    else:
                        self.erro_sintatico("Tokens adicionais após o fechamento do escopo.")
                else:
                    self.erro_sintatico("Fechamento de escopo '@' esperado.")
            else:
                self.erro_sintatico("Fechamento de '@' esperado após a lista de declaração.")
        else:
            self.erro_sintatico("Token 'main' esperado no início do código.")

    def lista_de_declaracao(self):
        print(f"DEBUG: Entrando na lista de declaração na linha {self.tokens[self.posicao]['linha']}")
        while self.posicao < len(self.tokens) and self.tokens[self.posicao]['tipo'] == 'PALAVRA_RESERVADA' and self.tokens[self.posicao]['valor'] == 'tipoVar':
            print("DEBUG: Chamando declaracao dentro da lista_de_declaracao")
            self.declaracao()
            
            
            self.posicao += 1
        
        

    def declaracao(self):
        print(f"DEBUG: Entrando na declaracao na linha {self.tokens[self.posicao]['linha']}")
        if self.tokens[self.posicao]['tipo'] == 'PALAVRA_RESERVADA' and self.tokens[self.posicao]['valor'] == 'tipoVar':
            print("DEBUG: Token tipoVar encontrado com sucesso.")
            self.consumir_tokens()
            if self.tokens[self.posicao]['tipo'] == 'IDENTIFICADOR':
                print(f"DEBUG: Token IDENTIFICADOR encontrado com sucesso: {self.tokens[self.posicao]['valor']}")
                self.consumir_tokens()
                if self.tokens[self.posicao]['tipo'] == 'SIM_ESPECIAL' and self.tokens[self.posicao]['valor'] == ';':
                    print("DEBUG: Token ; encontrado com sucesso.")
                    self.consumir_tokens()
                    print("DEBUG: Declaração concluída com sucesso.")
                else:
                    self.erro_sintatico("Esperado ; após declaração.")
            else:
                self.erro_sintatico("Esperado IDENTIFICADOR após tipoVar.")
        else:
            self.erro_sintatico("Esperado tipoVar para iniciar a declaração.")


def testar_analisador_sintatico():
    codigo_ficticio = [
        {'tipo': 'PALAVRA_RESERVADA', 'valor': 'main', 'linha': 1},
        {'tipo': 'SIM_ESPECIAL', 'valor': '@', 'linha': 1},
        {'tipo': 'PALAVRA_RESERVADA', 'valor': 'tipoVar', 'linha': 2},
        {'tipo': 'IDENTIFICADOR', 'valor': 'batata', 'linha': 2},
        {'tipo': 'SIM_ESPECIAL', 'valor': ';', 'linha': 2},
        {'tipo': 'PALAVRA_RESERVADA', 'valor': 'escopo', 'linha': 3},
        {'tipo': 'SIM_ESPECIAL', 'valor': '@', 'linha': 3}
    ]
    
    analisador = AnalisadorSintatico(codigo_ficticio)

    try:
        analisador.inicio()
    except SyntaxError as e:
        print(e)

if __name__ == "__main__":
    testar_analisador_sintatico()
