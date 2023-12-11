#<inicio> ::= main @ <programa> @
#<programa> ::= <declaracao>| <comando> | ε
#<declaracao> ::= <tipoVar> IDENTIFICADOR; <programa> | <declaracao2>
#<declaracao2> ::= <tipoVar> <atribuicao>
#<tipoVar> ::= num_int | num_flu | text
#<atribuicao> ::= IDENTIFICADOR -> <conteudo> ; <programa>
#<conteudo> ::= <valor> | texto | <expAritmetica> | <retornoFuncao>
#<valor> ::= IDENTIFICADOR | numero inteiro | numero float
#<comando> ::= <entrada>|<saida>|<desvio>|<atribuicao>|<laco>|<funcao>|<retorno>
#<entrada> ::= textin [ IDENTIFICADOR ]; <programa>
#<saida> :: = puts '[' <conteudo> ']'; <programa>
#<expAritmetica> ::= <valor> <operadorA> <expAritmetica2> ;| ε 
#<expAritmetica2> ::= <valor> | <valor> <operadorA> <expAritmetica2> | <valor> <operadorA> ( <expAritmetica2> )
#<operadorA> ::= + | - | / | * | //
#<funcao> ::= fn IDENTIFICADOR [ <argumento> ] @ <programa> @ <programa>
#<retorno> ::= take <conteudo> ;
#<simboloRelacional> ::= << | >> | >= | <= | == | != | ok | notok
#<termoRelacional> ::= <conteudo> <simboloRelacional> <termoRelacional2>
#<termoRelacional2> ::= <conteudo> | <conteudo> <termoLogico> <termoRelacional>
#<termoLogico> ::= && | '||'
#<desvio> ::= case[<termoRelacional>]@ <programa> @ <programa> | case[<termoRelacional>]@ <programa> @ <desvio2> <programa>
#<desvio2> ::= ordo @ <programa> @
#<laco> ::= <for> | <while>
#<for> ::= to [ num_int IDENTIFICADOR -> numero inteiro, IDENTIFICADOR <simboloRelacional> numero, <incrementa>]@ <programa> @ <programa>
#<incrementa> ::= <IDENTIFICADOR> <operadorA> <valor> 
#<while> ::= when [ <termoRelacional> ] @ <programa> @ <programa>
#<argumento> ::= <tipoVar> IDENTIFICADOR <argumento2>
#<argumento2> ::= , <argumento> | ε
#<retornoFuncao> ::= IDENTIFICADOR [ <argumento3> ]
#<argumento3> ::= <conteudo> | <conteudo> , <argumento3>


def inicio(tokens):
    elemento = No("inicio")
    if tokens[0][1] == "main":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if tokens[0][1] == "@":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            elemento.adicionar_filho(programa(tokens))
            if tokens[0][1] == "@":
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                tokens.pop(0)
                return elemento
            else:
                assert False, "Faltando @ na linha " + str(tokens[0][2])
        else:
            assert False, "Faltando @ na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando main na linha " + str(tokens[0][2])

def programa(tokens):
    elemento = No("programa")
    if tokens[0][1] == "num_int" or tokens[0][1] == "num_flu" or tokens[0][1] == "text":
        elemento.adicionar_filho(declaracao(tokens))
        return elemento
    elif tokens[0][1] == "textin":
        elemento.adicionar_filho(entrada(tokens))
        return elemento
    elif tokens[0][1] == "puts":
        elemento.adicionar_filho(saida(tokens))
        return elemento
    elif tokens[0][1] == "case":
        elemento.adicionar_filho(desvio(tokens))
        return elemento
    elif tokens[0][1] == "fn":
        elemento.adicionar_filho(funcao(tokens))
        return elemento
    elif tokens[0][0] == "IDENTIFICADOR":
        elemento.adicionar_filho(atribuicao(tokens))
        return elemento
    elif tokens[0][1] == "when":
        elemento.adicionar_filho(laco(tokens))
        return elemento
    elif tokens[0][1] == "to":
        elemento.adicionar_filho(laco(tokens))
        return elemento
    elif tokens[0][1] == "take":
        elemento.adicionar_filho(retorno(tokens))
        return elemento
    else:
        return elemento
    
def declaracao(tokens):
    elemento = No("declaracao")
    if tokens[0][1] == "num_int" or tokens[0][1] == "num_flu" or tokens[0][1] == "text":
        elemento.adicionar_filho(tipoVar(tokens))
        if tokens[0][0] == "IDENTIFICADOR":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            if tokens[0][0] == "ATRIBUICAO":
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                tokens.pop(0)
                elemento.adicionar_filho(conteudo(tokens))
            if tokens[0][1] == ";":
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                tokens.pop(0)
                elemento.adicionar_filho(programa(tokens))
                return elemento
            else:
                assert False, "Faltando ; na linha " + str(tokens[0][2])
        else:
            assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando tipo da variavel na linha " + str(tokens[0][2])

def tipoVar(tokens):
    elemento = No("tipoVar")
    if tokens[0][1] == "num_int":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        return elemento
    elif tokens[0][1] == "num_flu":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        return elemento
    elif tokens[0][1] == "text":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        return elemento
    else:
        assert False, "Faltando tipo da variavel na linha " + str(tokens[0][2])

def atribuicao(tokens):
    elemento = No("atribuicao")
    if tokens[0][0] == "IDENTIFICADOR":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if tokens[0][1] == "->":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            elemento.adicionar_filho(conteudo(tokens))
            if tokens[0][1] == ";":
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                tokens.pop(0)
                elemento.adicionar_filho(programa(tokens))
                return elemento
            else:
                assert False, "Faltando ; na linha " + str(tokens[0][2])
        else:
            assert False, "Faltando -> na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])

def conteudo(tokens):
    elemento = No("conteudo")
    if tokens[0][0] == "IDENTIFICADOR":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if (tokens[0][1] == "+" or tokens[0][1] == "-" or tokens[0][1] == "/" or tokens[0][1] == "*" or tokens[0][1] == "//"):
            elemento.adicionar_filho(operadorA(tokens))
            elemento.adicionar_filho(expAritmetica(tokens))
            return elemento
        elemento.adicionar_filho(retornoFuncao(tokens))
        return elemento
    elif tokens[0][0] == "NUM_INT":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if (tokens[0][1] == "+" or tokens[0][1] == "-" or tokens[0][1] == "/" or tokens[0][1] == "*" or tokens[0][1] == "//"):
            elemento.adicionar_filho(operadorA(tokens))
            elemento.adicionar_filho(expAritmetica(tokens))
            return elemento
        return elemento
    elif tokens[0][0] == "NUM_FLU":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if (tokens[0][1] == "+" or tokens[0][1] == "-" or tokens[0][1] == "/" or tokens[0][1] == "*" or tokens[0][1] == "//"):
            elemento.adicionar_filho(operadorA(tokens))
            elemento.adicionar_filho(expAritmetica(tokens))
            return elemento
        return elemento
    elif tokens[0][0] == "TEXT":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        return elemento
    elif tokens[0][1] == "(":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        elemento.adicionar_filho(expAritmetica(tokens))
        if tokens[0][1] == ")":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            return elemento
        else:
            assert False, "Faltando ) na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando conteudo na linha " + str(tokens[0][2])

def retornoFuncao(tokens):
    elemento = No("retornoFuncao")
    if tokens[0][1] == "[":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        elemento.adicionar_filho(argumento3(tokens))
        if tokens[0][1] == "]":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            return elemento
        else:
            assert False, "Faltando ) na linha " + str(tokens[0][2])
    else:
        return elemento
def expAritmetica(tokens):
    elemento = No("expAritmetica")
    if tokens[0][0] == "IDENTIFICADOR" or tokens[0][0] == "NUM_INT" or tokens[0][0] == "NUM_FLU":
        elemento.adicionar_filho(valor(tokens))
        if tokens[0][1] == "+" or tokens[0][1] == "-" or tokens[0][1] == "/" or tokens[0][1] == "*" or tokens[0][1] == "//":
            elemento.adicionar_filho(operadorA(tokens))
            elemento.adicionar_filho(expAritmetica2(tokens))
            return elemento
        else:
            return elemento
    else:
        assert False, "Faltando valor na linha " + str(tokens[0][2])

def expAritmetica2(tokens):
    elemento = No("expAritmetica2")
    if tokens[0][1] == "IDENTIFICADOR" or tokens[0][0] == "NUM_INT" or tokens[0][0] == "NUM_FLU":
        elemento.adicionar_filho(valor(tokens))
        if tokens[0][1] == "+" or tokens[0][1] == "-" or tokens[0][1] == "/" or tokens[0][1] == "*" or tokens[0][1] == "//":
            elemento.adicionar_filho(operadorA(tokens))
            elemento.adicionar_filho(expAritmetica2(tokens))
            return elemento
        else:
            return elemento
    elif tokens[0][1] == "(":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        elemento.adicionar_filho(expAritmetica2(tokens))
        if tokens[0][1] == ")":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            return elemento
        else:
            assert False, "Faltando ) na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando valor na linha " + str(tokens[0][2])

def operadorA(tokens):
    elemento = No("operadorA")
    if tokens[0][1] == "+" or tokens[0][1] == "-" or tokens[0][1] == "/" or tokens[0][1] == "*" or tokens[0][1] == "//":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        return elemento
    else:
        assert False, "Faltando operador aritmetico na linha " + str(tokens[0][2])

def valor(tokens):
    elemento = No("valor")
    if tokens[0][0] == "IDENTIFICADOR":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        return elemento
    elif tokens[0][0] == "NUM_INT":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        return elemento
    elif tokens[0][0] == "NUM_FLU":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        return elemento
    else:
        assert False, "Faltando valor na linha " + str(tokens[0][2])

def entrada(tokens):
    elemento = No("entrada")
    if tokens[0][1] == "textin":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if tokens[0][1] == "[":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            if tokens[0][0] == "IDENTIFICADOR":
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                tokens.pop(0)
                if tokens[0][1] == "]":
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    tokens.pop(0)
                    if tokens[0][1] == ";":
                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                        tokens.pop(0)
                        elemento.adicionar_filho(programa(tokens))
                        return elemento
                    else:
                        assert False, "Faltando ; na linha " + str(tokens[0][2])
                else:
                    assert False, "Faltando ] na linha " + str(tokens[0][2])
            else:
                assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
        else:
            assert False, "Faltando [ na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando textin na linha " + str(tokens[0][2])

def saida(tokens):
    elemento = No("saida")
    if tokens[0][1] == "puts":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if tokens[0][1] == "[":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            elemento.adicionar_filho(conteudo(tokens))
            if tokens[0][1] == "]":
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                tokens.pop(0)
                if tokens[0][1] == ";":
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    tokens.pop(0)
                    elemento.adicionar_filho(programa(tokens))
                    return elemento
                else:
                    assert False, "Faltando ; na linha " + str(tokens[0][2])
            else:
                assert False, "Faltando ] na linha " + str(tokens[0][2])
        else:
            assert False, "Faltando [ na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando puts na linha " + str(tokens[0][2])

def desvio(tokens):
    elemento = No("desvio")
    if tokens[0][1] == "case":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if tokens[0][1] == "[":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            elemento.adicionar_filho(termoRelacional(tokens))
            if tokens[0][1] == "]":
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                tokens.pop(0)
                if tokens[0][1] == "@":
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    tokens.pop(0)
                    elemento.adicionar_filho(programa(tokens))
                    if tokens[0][1] == "@":
                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                        tokens.pop(0)
                        elemento.adicionar_filho(programa(tokens))
                        if tokens[0][1] == "ordo":
                            elemento.adicionar_filho(desvio2(tokens))
                        return elemento
                    else:
                        assert False, "Faltando @ na linha " + str(tokens[0][2])
                else:
                    assert False, "Faltando @ na linha " + str(tokens[0][2])
            else:
                assert False, "Faltando [ na linha " + str(tokens[0][2])
        else:
            assert False, "Faltando ] na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando case na linha " + str(tokens[0][2])

def desvio2(tokens):
    elemento = No("desvio2")
    if tokens[0][1] == "ordo":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if tokens[0][1] == "@":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            elemento.adicionar_filho(programa(tokens))
            if tokens[0][1] == "@":
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                tokens.pop(0)
                return elemento
            else:
                assert False, "Faltando @ na linha " + str(tokens[0][2])
        else:
            assert False, "Faltando @ na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando ordo na linha " + str(tokens[0][2])

def termoRelacional(tokens):
    elemento = No("termoRelacional")
    if tokens[0][0] == "IDENTIFICADOR" or tokens[0][0] == "NUM_INT" or tokens[0][0] == "NUM_FLU" or tokens[0][1] == "TEXT":
        elemento.adicionar_filho(conteudo(tokens))
        elemento.adicionar_filho(simboloRelacional(tokens))
        elemento.adicionar_filho(termoRelacional2(tokens))
        return elemento
    else:
        assert False, "Faltando conteudo na linha " + str(tokens[0][2])

def simboloRelacional(tokens):
    elemento = No("simboloRelacional")
    if tokens[0][1] == "<<" or tokens[0][1] == ">>" or tokens[0][1] == ">=" or tokens[0][1] == "<=" or tokens[0][1] == "==" or tokens[0][1] == "!=" or tokens[0][1] == "ok" or tokens[0][1] == "notok":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        return elemento
    else:
        assert False, "Faltando simbolo relacional na linha " + str(tokens[0][2])

def termoRelacional2(tokens):
    elemento = No("termoRelacional2")
    if tokens[0][0] == "IDENTIFICADOR" or tokens[0][0] == "NUM_INT" or tokens[0][0] == "NUM_FLU" or tokens[0][1] == "TEXT":
        elemento.adicionar_filho(conteudo(tokens))
        if tokens[0][1] == "&&" or tokens[0][1] == "||":
            elemento.adicionar_filho(termoLogico(tokens))
            elemento.adicionar_filho(termoRelacional(tokens))
        return elemento
    else:
        assert False, "Faltando conteudo na linha " + str(tokens[0][2])

def termoLogico(tokens):
    elemento = No("termoLogico")
    if tokens[0][1] == "&&" or tokens[0][1] == "||":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        return elemento
    else:
        return elemento

def funcao(tokens):
    elemento = No("funcao")
    if tokens[0][1] == "fn":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if tokens[0][0] == "IDENTIFICADOR":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            if tokens[0][1] == "[":
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                tokens.pop(0)
                elemento.adicionar_filho(argumento(tokens))
                if tokens[0][1] == "]":
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    tokens.pop(0)
                    if tokens[0][1] == "@":
                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                        tokens.pop(0)
                        elemento.adicionar_filho(programa(tokens))
                        if tokens[0][1] == "@":
                            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                            tokens.pop(0)
                            elemento.adicionar_filho(programa(tokens))
                            return elemento
                        else:
                            assert False, "Faltando @ na linha " + str(tokens[0][2])
                    else:
                        assert False, "Faltando @ na linha " + str(tokens[0][2])
                else:
                    assert False, "Faltando ] na linha " + str(tokens[0][2])
            else:
                assert False, "Faltando [ na linha " + str(tokens[0][2])
        else:
            assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando fn na linha " + str(tokens[0][2])

def argumento(tokens):
    elemento = No("argumento")
    if tokens[0][1] == "num_int" or tokens[0][1] == "num_flu" or tokens[0][1] == "text":
        elemento.adicionar_filho(tipoVar(tokens))
        if tokens[0][0] == "IDENTIFICADOR":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            elemento.adicionar_filho(argumento2(tokens))
            return elemento
        else:
            assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
    else:
        return elemento
    
def argumento2(tokens):
    elemento = No("argumento2")
    if tokens[0][1] == ",":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        elemento.adicionar_filho(argumento(tokens))
        return elemento
    else:
        return elemento
    
def retorno(tokens):
    elemento = No("retorno")
    if tokens[0][1] == "take":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        elemento.adicionar_filho(conteudo(tokens))
        if tokens[0][1] == ";":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            return elemento
        else:
            assert False, "Faltando ; na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando take na linha " + str(tokens[0][2])

def laco(tokens):
    elemento = No("laco")
    if tokens[0][1] == "when":
        elemento.adicionar_filho(while_(tokens))
        return elemento
    elif (tokens[0][1] == "to"):
        elemento.adicionar_filho(for_(tokens))
        return elemento
    else:
        assert False, "Faltando laco na linha " + str(tokens[0][2])

def while_(tokens):
    elemento = No("while")
    if tokens[0][1] == "when":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if tokens[0][1] == "[":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            elemento.adicionar_filho(termoRelacional(tokens))
            if tokens[0][1] == "]":
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                tokens.pop(0)
                if tokens[0][1] == "@":
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    tokens.pop(0)
                    elemento.adicionar_filho(programa(tokens))
                    if tokens[0][1] == "@":
                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                        tokens.pop(0)
                        elemento.adicionar_filho(programa(tokens))
                        return elemento
                    else:
                        assert False, "Faltando @ na linha " + str(tokens[0][2])
                else:
                    assert False, "Faltando @ na linha " + str(tokens[0][2])
            else:
                assert False, "Faltando ] na linha " + str(tokens[0][2])
        else:
            assert False, "Faltando [ na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando when na linha " + str(tokens[0][2])


def for_(tokens):
    elemento = No("for")
    if tokens[0][1] == "to":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        if tokens[0][1] == "[":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            if tokens[0][1] == "num_int":
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                tokens.pop(0)
                if tokens[0][0] == "IDENTIFICADOR":
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    tokens.pop(0)
                    if tokens[0][1] == "->":
                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                        tokens.pop(0)
                        if tokens[0][0] == "NUM_INT":
                            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                            tokens.pop(0)
                            if tokens[0][1] == ",":
                                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                tokens.pop(0)
                                if tokens[0][0] == "IDENTIFICADOR":
                                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                    tokens.pop(0)
                                    if tokens[0][1] == "<<" or tokens[0][1] == ">>" or tokens[0][1] == ">=" or tokens[0][1] == "<=" or tokens[0][1] == "==" or tokens[0][1] == "!=" or tokens[0][1] == "ok" or tokens[0][1] == "notok":
                                        elemento.adicionar_filho(simboloRelacional(tokens))
                                        if tokens[0][0] == "NUM_INT":
                                            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                            tokens.pop(0)
                                            if tokens[0][1] == ",":
                                                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                                tokens.pop(0)
                                                elemento.adicionar_filho(incrementa(tokens))
                                                if tokens[0][1] == "]":
                                                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                                    tokens.pop(0)
                                                    if tokens[0][1] == "@":
                                                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                                        tokens.pop(0)
                                                        elemento.adicionar_filho(programa(tokens))
                                                        if tokens[0][1] == "@":
                                                            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                                            tokens.pop(0)
                                                            elemento.adicionar_filho(programa(tokens))
                                                            return elemento
                                                        else:
                                                            assert False, "Faltando @ na linha " + str(tokens[0][2])
                                                    else:
                                                        assert False, "Faltando @ na linha " + str(tokens[0][2])
                                                else:
                                                    assert False, "Faltando ] na linha " + str(tokens[0][2])
                                            else:
                                                assert False, "Faltando ',' na linha " + str(tokens[0][2])
                                        else:
                                            assert False, "Faltando numero inteiro na linha " + str(tokens[0][2])
                                    else:
                                        assert False, "Faltando simbolo relacional na linha " + str(tokens[0][2])
                                else:
                                    assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
                            else:
                                assert False, "Faltando ',' na linha " + str(tokens[0][2])
                        else:
                            assert False, "Faltando numero inteiro na linha " + str(tokens[0][2])
                    else:
                        assert False, "Faltando '->' na linha " + str(tokens[0][2])
                else:
                    assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
            else:
                assert False, "Faltando num_int na linha " + str(tokens[0][2])
        else:
            assert False, "Faltando '[' na linha " + str(tokens[0][2])
    else:
        assert False, "Faltando 'to' na linha " + str(tokens[0][2])

def argumento3(tokens):
    elemento = No("argumento3")
    if tokens[0][0] == "IDENTIFICADOR" or tokens[0][0] == "NUM_INT" or tokens[0][0] == "NUM_FLU" or tokens[0][1] == "TEXT":
        elemento.adicionar_filho(conteudo(tokens))
        if tokens[0][1] == ",":
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            tokens.pop(0)
            elemento.adicionar_filho(argumento3(tokens))
            return elemento
        return elemento
    else:
        assert False, "Faltando conteudo na linha " + str(tokens[0][2])

def incrementa(tokens):
    elemento = No("incrementa")
    if tokens[0][0] == "IDENTIFICADOR":
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        tokens.pop(0)
        elemento.adicionar_filho(operadorA(tokens))
        elemento.adicionar_filho(valor(tokens))
        return elemento
    else:
        assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])

#classe para representar um nó na árvore sintática
class No:
    def __init__(self, tipo, lexema = None):
        self.tipo = tipo
        self.lexema = lexema
        self.filhos = []
    
    def __repr__(self, profundidade=0):
        indentacao = "\t |--" * profundidade
        representacao = f"{indentacao}{repr(self.tipo)}\n"

        for filho in self.filhos:
            representacao += filho.__repr__(profundidade + 1)

        return representacao

    def adicionar_filho(self, elemento):
        self.filhos.append(elemento)

def arvore(tokens): 
    raiz = No("Arvore Sintatica")
    raiz.adicionar_filho(inicio(tokens))
    return raiz