class No:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.filhos = []

    def adicionar_filho(self, filho):
        self.filhos.append(filho)

    def __str__(self, nivel=0):
        resultado = "  " * nivel + f"{self.tipo}: {self.valor}\n"
        for filho in self.filhos:
            resultado += filho.__str__(nivel + 1)
        return resultado

class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice = 0

    def analisar(self):
        return self.inicio()

    def consome_tipo_esperado(self, tipo_esperado):
        if self.indice < len(self.tokens) and self.tokens[self.indice]["tipo"] == tipo_esperado:
            token_atual = self.tokens[self.indice]
            self.indice += 1
            return token_atual
        else:
            raise Exception(f"Erro sintático: Esperado {tipo_esperado}, mas encontrado {self.tokens[self.indice]['tipo']} na linha {self.tokens[self.indice]['linha']}")



    def inicio(self):
        no_inicio = No("Inicio")
        if self.tokens[self.indice]["tipo"] in ["main", "vacuum", "num_int", "num_flu", "text"]:
            no_inicio.adicionar_filho(self.lista_de_declaracao())
        else:
            raise Exception(f"Erro sintático: Esperado main, vacuum, num_int, num_flu ou text, mas encontrado {self.tokens[self.indice]['tipo']} na linha {self.tokens[self.indice]['linha']}")
        return no_inicio

    def lista_de_declaracao(self):
        no_lista_de_declaracao = No("ListaDeDeclaracao")
        if self.tokens[self.indice]["tipo"] in ["main", "vacuum", "num_int", "num_flu", "text"]:
            no_lista_de_declaracao.adicionar_filho(self.declaracao())
            no_lista_de_declaracao.adicionar_filho(self.lista_de_declaracao())
        elif self.tokens[self.indice]["tipo"] == "fim_arquivo":
            return no_lista_de_declaracao  # Lista vazia
        else:
            raise Exception(f"Erro sintático: Esperado main, vacuum, num_int, num_flu, text ou fim_arquivo, mas encontrado {self.tokens[self.indice]['tipo']} na linha {self.tokens[self.indice]['linha']}")
        return no_lista_de_declaracao

    def declaracao(self):
        no_declaracao = No("Declaracao")
        tipo_var = self.tipo_var()
        variavel = self.variavel()
        self.consome(";")
        no_declaracao.adicionar_filho(tipo_var)
        no_declaracao.adicionar_filho(variavel)
        return no_declaracao

    def tipo_var(self):
        tipos_esperados = ["SIM_ESPECIAL","IDENTIFICADOR","main","num_int", "num_flu", "text"]
        token_tipo = next((t for t in tipos_esperados if self.tokens[self.indice]["tipo"] == t), None)

        if token_tipo:
            return No("TipoVar", self.consome_tipo_esperado(token_tipo)["lexema"])
        else:
            raise Exception(f"Erro sintático: Esperado {tipos_esperados}, mas encontrado {self.tokens[self.indice]['tipo']} na linha {self.tokens[self.indice]['linha']}")


    def variavel(self):
        token_id = self.consome_tipo_esperado("IDENTIFICADOR")
        return No("Variavel", token_id["lexema"])
    
    def construir_arvore(self):
        try:
            arvore_sintatica = self.analisar()
            print("Árvore Sintática:")
            print(arvore_sintatica)
        except Exception as e:
            print(e)

# Exemplo de uso:
tokens_exemplo = [
    {"tipo": "main", "lexema": "main", "linha": 1},
    {"tipo": "SIM_ESPECIAL", "lexema": "{", "linha": 1},
    {"tipo": "num_int", "lexema": "num_int", "linha": 2},
    {"tipo": "IDENTIFICADOR", "lexema": "x", "linha": 2},
    {"tipo": ";", "lexema": ";", "linha": 2},
    {"tipo": "}", "lexema": "}", "linha": 3},
    {"tipo": "fim_arquivo", "lexema": "\0", "linha": 3},
]

analisador = AnalisadorSintatico(tokens_exemplo)
analisador.construir_arvore()
