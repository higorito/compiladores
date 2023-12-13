from analisadorLexico import AnalisadorLexico
from auxx import arvore
from semantico import analisador_semantico

if __name__ == "__main__":
    AL = AnalisadorLexico("teste.txt")
    AL.main()
    tokens = AL.tokens
    arvoreSintatica = arvore(tokens)
    print(arvoreSintatica)
    AS = analisador_semantico(arvoreSintatica)
    print(AS)