class AnaliseSemantica:
    def __init__(self):
        self.variaveis = {}
        self.funcoes = {}
        self.resultado = None

    def analisar(self, no):
        self.analisar_no(no)

    def analisar_no(self, no):
        if no.tipo == 'DECLARACAO_VAR':
            self.declarar_variavel(no)
        elif no.tipo == 'FUNCAO':
            self.declarar_funcao(no)
        elif no.tipo == 'CHAMADA_FUNCAO':
            self.chamar_funcao(no)
        elif no.tipo == 'ATRIBUICAO':
            self.atribuir_valor(no)
        elif no.tipo == 'EXPRESSAO_ARITMETICA':
            self.avaliar_expressao(no)
        elif no.tipo == 'EXPRESSAO_RELACIONAL':
            self.avaliar_expressao_relacional(no)
        elif no.tipo == 'DESVIO':
            self.analisar_desvio(no)
        elif no.tipo == 'LACO':
            self.analisar_laco(no)
        elif no.tipo == 'SAIDA':
            self.saida(no)
        elif no.tipo == 'main':
            self.verificar_escopo(no)

    def declarar_variavel(self, no):
        tipo = no.filhos[0].valor
        nome = no.filhos[1].valor

        if len(no.filhos) == 3:
            valor = self.avaliar_expressao(no.filhos[2])

            if valor is not None:
                self.variaveis[nome] = {'tipo': tipo, 'valor': valor}
        else:
            self.variaveis[nome] = {'tipo': tipo, 'valor': None}

    def declarar_funcao(self, no):
        nome_funcao = no.filhos[0].valor
        parametros = no.filhos[1].filhos
        corpo_funcao = no.filhos[2].filhos

        if nome_funcao in self.funcoes:
            print(f"Erro semântico: Função '{nome_funcao}' já declarada.")
            return

        self.funcoes[nome_funcao] = {'parametros': parametros, 'corpo': corpo_funcao}
        self.analisar_escopo(corpo_funcao)

    def verificar_escopo(self, no):
        conteudo_escopo = no.filhos
        if conteudo_escopo and len(conteudo_escopo) > 0 and conteudo_escopo[-1].tipo != 'FIM_ESCOPO':
            print("Erro semântico: Escopo não está fechado corretamente com '@ @'.")
        elif conteudo_escopo and conteudo_escopo[-1].tipo == 'FIM_ESCOPO':
            no.filhos.pop()

    def atribuir_valor(self, no):
        nome_variavel = no.filhos[0].valor
        valor = self.avaliar_expressao(no.filhos[1])

        if nome_variavel in self.variaveis:
            tipo_variavel = self.variaveis[nome_variavel]['tipo']
            if tipo_variavel == 'num_int' and not isinstance(valor, int):
                print(f"Erro semântico: Tentativa de atribuir um valor não inteiro à variável '{nome_variavel}'.")
            elif tipo_variavel == 'num_flu' and not isinstance(valor, (int, float)):
                print(f"Erro semântico: Tentativa de atribuir um valor não numérico à variável '{nome_variavel}'.")
            else:
                self.variaveis[nome_variavel]['valor'] = valor
        else:
            print(f"Erro semântico: Variável '{nome_variavel}' não foi declarada.")

    def saida(self, no):
        print(f"Saida: {self.resultado}")

    def avaliar_expressao(self, no):
        if no.tipo == 'VARIAVEL':
            nome_variavel = no.valor
            if nome_variavel in self.variaveis:
                return self.variaveis[nome_variavel]['valor']
            else:
                print(f"Erro semântico: Variável '{nome_variavel}' não foi definida.")
                return None
        elif no.tipo == 'EXPRESSAO_ARITMETICA':
            return self.avaliar_expressao_aritmetica(no)
        elif no.tipo == 'EXPRESSAO_RELACIONAL':
            return self.avaliar_expressao_relacional(no)
        else:
            print(f"Erro semântico: Tipo de expressão não suportado: {no.tipo}")
            return None

    def avaliar_expressao_aritmetica(self, no):
        operador = no.filhos[0].valor
        operando1 = self.avaliar_expressao(no.filhos[1])
        operando2 = self.avaliar_expressao(no.filhos[2])

        if operando1 is not None and operando2 is not None:
            if operador in ('+', '-', '*', '/'):
                if isinstance(operando1, int) and isinstance(operando2, int):
                    if operador in ('/', '*') and operando2 == 0:
                        print("Erro semântico: Divisão por zero.")
                        return None
                    else:
                        if operador == '+':
                            return operando1 + operando2
                        elif operador == '-':
                            return operando1 - operando2
                        elif operador == '*':
                            return operando1 * operando2
                        elif operador == '/':
                            return operando1 / operando2
                else:
                    print("Erro semântico: Operações aritméticas devem ser realizadas entre números inteiros.")
                    return None
            else:
                print(f"Erro semântico: Operador '{operador}' não suportado em expressões aritméticas.")
                return None
        else:
            return None

    def avaliar_expressao_relacional(self, no):
        if no.tipo == 'RELACIONAL':
            return no.valor
        elif no.tipo == 'EXPRESSAO_RELACIONAL':
            operador_relacional = no.filhos[0].valor
            expressao1 = self.avaliar_expressao_relacional(no.filhos[1])
            expressao2 = self.avaliar_expressao_relacional(no.filhos[2])

            if operador_relacional == '<':
                return expressao1 < expressao2
            elif operador_relacional == '>':
                return expressao1 > expressao2
            elif operador_relacional == '<=':
                return expressao1 <= expressao2
            elif operador_relacional == '>=':
                return expressao1 >= expressao2
            elif operador_relacional == '==':
                return expressao1 == expressao2
            elif operador_relacional == '!=':
                return expressao1 != expressao2
        else:
            pass

    def analisar_laco(self, no):
        tipo_laco = no.filhos[0].valor
        if tipo_laco == 'to':
            self.analisar_laco_to(no)
        elif tipo_laco == 'when':
            self.analisar_laco_when(no)

    def analisar_laco_to(self, no):
        atribuicao_inicio = no.filhos[1]
        atribuicao_fim = no.filhos[2]
        escopo = no.filhos[3].filhos[0]

        variavel_inicio = atribuicao_inicio.filhos[0].valor
        valor_inicio = self.avaliar_expressao(atribuicao_inicio.filhos[1])

        variavel_fim = atribuicao_fim.filhos[0].valor
        valor_fim = self.avaliar_expressao(atribuicao_fim.filhos[1])

        if variavel_inicio in self.variaveis and variavel_fim in self.variaveis:
            tipo_variavel_inicio = self.variaveis[variavel_inicio]['tipo']
            tipo_variavel_fim = self.variaveis[variavel_fim]['tipo']

            if tipo_variavel_inicio == 'num_int' and not isinstance(valor_inicio, int):
                print(f"Erro semântico: Valor inicial do loop 'to' não é do tipo 'num_int'.")
            elif tipo_variavel_fim == 'num_int' and not isinstance(valor_fim, int):
                print(f"Erro semântico: Valor final do loop 'to' não é do tipo 'num_int'.")
            else:
                pass
        else:
            print("Erro semântico: Variáveis do loop 'to' devem ser previamente declaradas.")

        self.analisar_escopo(escopo)

    def analisar_laco_when(self, no):
        expressao_condicao = no.filhos[1]
        escopo = no.filhos[2].filhos[0]

        valor_condicao = self.avaliar_expressao(expressao_condicao)

        if not isinstance(valor_condicao, bool):
            print(f"Erro semântico: Condição do loop 'when' não avalia para um valor booleano.")
        else:
            pass

        self.analisar_escopo(escopo)

    def analisar_escopo(self, no):
        for filho in no:
            self.analisar_no(filho)

    def analisar_desvio(self, no):
        tipo_desvio = no.filhos[0].valor

        if tipo_desvio == 'case':
            self.analisar_case(no)
        elif tipo_desvio == 'when':
            self.analisar_when(no)
        elif tipo_desvio == 'caseNot':
            self.analisar_case_not(no)

    def analisar_case(self, no):
        expressao = no.filhos[1]
        escopo = no.filhos[2].filhos[0]

        valor_condicao = self.avaliar_expressao(expressao)

        if not isinstance(valor_condicao, bool):
            print("Erro semântico: A condição do 'case' deve ser uma expressão booleana.")

        self.analisar_escopo(escopo)

    def analisar_case_not(self, no):
        escopo = no.filhos[1].filhos[0]

        self.analisar_escopo(escopo)

    def analisar_when(self, no):
        expressao = no.filhos[1]
        escopo = no.filhos[2].filhos[0]

        valor_condicao = self.avaliar_expressao(expressao)

        if not isinstance(valor_condicao, bool):
            print("Erro semântico: A condição do 'when' deve ser uma expressão booleana.")

        # Análise semântica para o escopo dentro do 'when'
        self.analisar_escopo(escopo)

    def avaliar_expressao_relacional(self, no):
        if no.tipo == 'RELACIONAL':
            return no.valor
        elif no.tipo == 'EXPRESSAO_RELACIONAL':
            operador_relacional = no.filhos[0].valor
            expressao1 = self.avaliar_expressao_relacional(no.filhos[1])
            expressao2 = self.avaliar_expressao_relacional(no.filhos[2])

            
            if operador_relacional == '<':
                return expressao1 < expressao2
            elif operador_relacional == '>':
                return expressao1 > expressao2
            elif operador_relacional == '<=':
                return expressao1 <= expressao2
            elif operador_relacional == '>=':
                return expressao1 >= expressao2
            elif operador_relacional == '==':
                return expressao1 == expressao2
            elif operador_relacional == '!=':
                return expressao1 != expressao2
        else:
            
            pass

    def analisar_laco(self, no):
        tipo_laco = no.filhos[0].valor
        if tipo_laco == 'to':
            self.analisar_laco_to(no)
        elif tipo_laco == 'when':
            self.analisar_laco_when(no)

    def analisar_laco_to(self, no):
        atribuicao_inicio = no.filhos[1]
        atribuicao_fim = no.filhos[2]
        escopo = no.filhos[3].filhos[0]

        variavel_inicio = atribuicao_inicio.filhos[0].valor
        valor_inicio = self.avaliar_expressao(atribuicao_inicio.filhos[1])

        variavel_fim = atribuicao_fim.filhos[0].valor
        valor_fim = self.avaliar_expressao(atribuicao_fim.filhos[1])

        if variavel_inicio in self.variaveis and variavel_fim in self.variaveis:
            tipo_variavel_inicio = self.variaveis[variavel_inicio]['tipo']
            tipo_variavel_fim = self.variaveis[variavel_fim]['tipo']

            if tipo_variavel_inicio == 'num_int' and not isinstance(valor_inicio, int):
                print(f"Erro semântico: Valor inicial do loop 'to' não é do tipo 'num_int'.")
            elif tipo_variavel_fim == 'num_int' and not isinstance(valor_fim, int):
                print(f"Erro semântico: Valor final do loop 'to' não é do tipo 'num_int'.")
            else:
            
                pass
        else:
            print("Erro semântico: Variáveis do loop 'to' devem ser previamente declaradas.")

        self.analisar_escopo(escopo)

    def analisar_laco_when(self, no):
        expressao_condicao = no.filhos[1]
        escopo = no.filhos[2].filhos[0]

        valor_condicao = self.avaliar_expressao(expressao_condicao)

        if not isinstance(valor_condicao, bool):
            print(f"Erro semântico: Condição do loop 'when' não avalia para um valor booleano.")
        else:
            
            pass

        
        self.analisar_escopo(escopo)

    def analisar_escopo(self, no):
        for filho in no.filhos:
            self.analisar_no(filho)

    def analisar_desvio(self, no):
        tipo_desvio = no.filhos[0].valor

        if tipo_desvio == 'case':
            self.analisar_case(no)
        elif tipo_desvio == 'when':
            self.analisar_when(no)
        elif tipo_desvio == 'caseNot':
            self.analisar_case_not(no)

    def analisar_case(self, no):
        expressao = no.filhos[1]
        escopo = no.filhos[2].filhos[0]

        valor_condicao = self.avaliar_expressao(expressao)

        if not isinstance(valor_condicao, bool):
            print("Erro semântico: A condição do 'case' deve ser uma expressão booleana.")

       
        self.analisar_escopo(escopo)

    def analisar_case_not(self, no):
        escopo = no.filhos[1].filhos[0]

        self.analisar_escopo(escopo)

    def avaliar_funcao(self, nome, argumentos):
        #avaliar a função com base nos argumentos
       
        pass

    def saida(self, no):
        expressao = no.filhos[0]
        resultado = self.avaliar_expressao(expressao)
        print(f"Saida: {resultado}")


class No:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.filhos = []

    def adicionar_filho(self, filho):
        self.filhos.append(filho)

def imprimir_arvore(no, nivel=0):
    if no.valor is not None:
        print("  " * nivel + f"-- {no.tipo} ({no.valor})")
    else:
        print("  " * nivel + f"-- {no.tipo}")

    for filho in no.filhos:
        imprimir_arvore(filho, nivel + 1)

# Exemplo de uso
raiz = No("Programa")

# Atribuição 1
atribuicao1 = No("ATRIBUICAO")
atribuicao1.adicionar_filho(No("TIPO_VAR", "num_int"))
atribuicao1.adicionar_filho(No("VARIAVEL", "a"))
atribuicao1.adicionar_filho(No("NUMERO", "20"))
raiz.adicionar_filho(atribuicao1)

# Atribuição 2
atribuicao2 = No("ATRIBUICAO")
atribuicao2.adicionar_filho(No("TIPO_VAR", "num_int"))
atribuicao2.adicionar_filho(No("VARIAVEL", "b"))
atribuicao2.adicionar_filho(No("NUMERO", "10"))
raiz.adicionar_filho(atribuicao2)

# Estrutura condicional
estrutura_case = No("DESVIO")
case = No("CASE")
expressao_case = No("EXPRESSAO_RELACIONAL")
expressao_case.adicionar_filho(No("VARIAVEL", "a"))
expressao_case.adicionar_filho(No("OPERADOR_RELACIONAL", "<="))
expressao_case.adicionar_filho(No("VARIAVEL", "b"))
case.adicionar_filho(expressao_case)

# Escopo do Case
escopo_case = No("ESOCAPO_CASE")

# Atribuição dentro do escopo
atribuicao_case = No("ATRIBUICAO")
atribuicao_case.adicionar_filho(No("VARIAVEL", "a"))
expressao_aritmetica = No("EXPRESSAO_ARITMETICA")
expressao_aritmetica.adicionar_filho(No("VARIAVEL", "a"))
expressao_aritmetica.adicionar_filho(No("OPERADOR_ARITMETICO", "+"))
expressao_aritmetica.adicionar_filho(No("NUMERO", "1"))
atribuicao_case.adicionar_filho(expressao_aritmetica)

escopo_case.adicionar_filho(atribuicao_case)
case.adicionar_filho(escopo_case)

# Adiciona o Case à estrutura condicional
estrutura_case.adicionar_filho(case)
raiz.adicionar_filho(estrutura_case)

# Imprime a árvore
imprimir_arvore(raiz)