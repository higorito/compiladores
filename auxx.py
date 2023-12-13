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
    #cria um nó chamado "inicio"
    elemento = No("inicio")
    
    #verifica se o primeiro token é a palavra-chave "main"
    if tokens[0][1] == "main":
        #adiciona um filho ao nó "inicio" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é "@"
        if tokens[0][1] == "@":
            #adiciona um filho ao nó "inicio" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #chama a função 'programa' e adiciona o nó retornado como filho de "inicio"
            elemento.adicionar_filho(programa(tokens))
            
            #verifica se o próximo token é "@"
            if tokens[0][1] == "@":
                #adiciona um filho ao nó "inicio" com o valor e tipo do token atual
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                #remove o token processado da lista de tokens
                tokens.pop(0)
                
                #retorna o nó "inicio" completo
                return elemento
            else:
                #se não houver "@", gera um erro indicando a falta de "@" na linha do token atual
                assert False, "Faltando @ na linha " + str(tokens[0][2])
        else:
            #se não houver "@", gera um erro indicando a falta de "@" na linha do token atual
            assert False, "Faltando @ na linha " + str(tokens[0][2])
    else:
        #se não houver "main", gera um erro indicando a falta de "main" na linha do token atual
        assert False, "Faltando main na linha " + str(tokens[0][2])
def programa(tokens):
    #cria um nó chamado "programa"
    elemento = No("programa")
    
    #verifica o tipo do primeiro token para determinar a estrutura apropriada
    if tokens[0][1] == "num_int" or tokens[0][1] == "num_flu" or tokens[0][1] == "text":
        #adiciona um filho ao nó "programa" chamando a função 'declaracao'
        elemento.adicionar_filho(declaracao(tokens))
        #retorna o nó "programa" completo
        return elemento
    elif tokens[0][1] == "textin":
        #adiciona um filho ao nó "programa" chamando a função 'entrada'
        elemento.adicionar_filho(entrada(tokens))
        #retorna o nó "programa" completo
        return elemento
    elif tokens[0][1] == "puts":
        #adiciona um filho ao nó "programa" chamando a função 'saida'
        elemento.adicionar_filho(saida(tokens))
        #retorna o nó "programa" completo
        return elemento
    elif tokens[0][1] == "case":
        #adiciona um filho ao nó "programa" chamando a função 'desvio'
        elemento.adicionar_filho(desvio(tokens))
        #retorna o nó "programa" completo
        return elemento
    elif tokens[0][1] == "fn":
        #adiciona um filho ao nó "programa" chamando a função 'funcao'
        elemento.adicionar_filho(funcao(tokens))
        #retorna o nó "programa" completo
        return elemento
    elif tokens[0][0] == "IDENTIFICADOR":
        #adiciona um filho ao nó "programa" chamando a função 'atribuicao'
        elemento.adicionar_filho(atribuicao(tokens))
        #retorna o nó "programa" completo
        return elemento
    elif tokens[0][1] == "when":
        #adiciona um filho ao nó "programa" chamando a função 'laco'
        elemento.adicionar_filho(laco(tokens))
        #retorna o nó "programa" completo
        return elemento
    elif tokens[0][1] == "to":
        #adiciona um filho ao nó "programa" chamando a função 'laco'
        elemento.adicionar_filho(laco(tokens))
        #retorna o nó "programa" completo
        return elemento
    elif tokens[0][1] == "take":
        #adiciona um filho ao nó "programa" chamando a função 'retorno'
        elemento.adicionar_filho(retorno(tokens))
        #retorna o nó "programa" completo
        return elemento
    else:
        #se não houver correspondência, retorna o nó "programa" sem adicionar filhos
        return elemento

def declaracao(tokens):
    #cria um nó chamado "declaracao"
    elemento = No("declaracao")
    
    #verifica o tipo do primeiro token para determinar a estrutura apropriada
    if tokens[0][1] == "num_int" or tokens[0][1] == "num_flu" or tokens[0][1] == "text":
        #adiciona um filho ao nó "declaracao" chamando a função 'tipoVar'
        elemento.adicionar_filho(tipoVar(tokens))
        
        #verifica se o próximo token é um IDENTIFICADOR
        if tokens[0][0] == "IDENTIFICADOR":
            #adiciona um filho ao nó "declaracao" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #verifica se o próximo token é uma ATRIBUICAO
            if tokens[0][0] == "ATRIBUICAO":
                #adiciona um filho ao nó "declaracao" com o valor e tipo do token atual
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                #remove o token processado da lista de tokens
                tokens.pop(0)
                
                #adiciona um filho ao nó "declaracao" chamando a função 'conteudo'
                elemento.adicionar_filho(conteudo(tokens))
                
            #verifica se o próximo token é um ponto e vírgula
            if tokens[0][1] == ";":
                #adiciona um filho ao nó "declaracao" com o valor e tipo do token atual
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                #remove o token processado da lista de tokens
                tokens.pop(0)
                
                #adiciona um filho ao nó "declaracao" chamando a função 'programa'
                elemento.adicionar_filho(programa(tokens))
                
                #retorna o nó "declaracao" completo
                return elemento
            else:
                #se não houver ponto e vírgula, gera um erro indicando a falta de ";" na linha do token atual
                assert False, "Faltando ; na linha " + str(tokens[0][2])
        else:
            #se não houver IDENTIFICADOR, gera um erro indicando a falta de IDENTIFICADOR na linha do token atual
            assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
    else:
        #se não houver correspondência com tipos válidos, gera um erro indicando a falta de tipo da variável na linha do token atual
        assert False, "Faltando tipo da variavel na linha " + str(tokens[0][2])

def tipoVar(tokens):
    #cria um nó chamado "tipoVar"
    elemento = No("tipoVar")
    
    #verifica o tipo do primeiro token para determinar o tipo da variável
    if tokens[0][1] == "num_int":
        #adiciona um filho ao nó "tipoVar" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        #retorna o nó "tipoVar" completo
        return elemento
    elif tokens[0][1] == "num_flu":
        #adiciona um filho ao nó "tipoVar" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        #retorna o nó "tipoVar" completo
        return elemento
    elif tokens[0][1] == "text":
        #adiciona um filho ao nó "tipoVar" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        #retorna o nó "tipoVar" completo
        return elemento
    else:
        #se não houver correspondência com tipos válidos, gera um erro indicando a falta de tipo da variável na linha do token atual
        assert False, "Faltando tipo da variavel na linha " + str(tokens[0][2])

def atribuicao(tokens):
    #cria um nó chamado "atribuicao"
    elemento = No("atribuicao")
    
    #verifica se o primeiro token é um IDENTIFICADOR
    if tokens[0][0] == "IDENTIFICADOR":
        #adiciona um filho ao nó "atribuicao" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é uma seta "->"
        if tokens[0][1] == "->":
            #adiciona um filho ao nó "atribuicao" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #adiciona um filho ao nó "atribuicao" chamando a função 'conteudo'
            elemento.adicionar_filho(conteudo(tokens))
            
            #verifica se o próximo token é um ponto e vírgula
            if tokens[0][1] == ";":
                #adiciona um filho ao nó "atribuicao" com o valor e tipo do token atual
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                #remove o token processado da lista de tokens
                tokens.pop(0)
                
                #adiciona um filho ao nó "atribuicao" chamando a função 'programa'
                elemento.adicionar_filho(programa(tokens))
                
                #retorna o nó "atribuicao" completo
                return elemento
            else:
                #se não houver ponto e vírgula, gera um erro indicando a falta de ";" na linha do token atual
                assert False, "Faltando ; na linha " + str(tokens[0][2])
        else:
            #se não houver seta "->", gera um erro indicando a falta de "->" na linha do token atual
            assert False, "Faltando -> na linha " + str(tokens[0][2])
    else:
        #se não houver IDENTIFICADOR, gera um erro indicando a falta de IDENTIFICADOR na linha do token atual
        assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])

def conteudo(tokens):
    #cria um nó chamado "conteudo"
    elemento = No("conteudo")
    
    #verifica o tipo do primeiro token para determinar a estrutura apropriada
    if tokens[0][0] == "IDENTIFICADOR":
        #adiciona um filho ao nó "conteudo" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é um operador aritmético
        if (tokens[0][1] == "+" or tokens[0][1] == "-" or tokens[0][1] == "/" or tokens[0][1] == "*" or tokens[0][1] == "//"):
            #adiciona um filho ao nó "conteudo" chamando a função 'operadorA'
            elemento.adicionar_filho(operadorA(tokens))
            #adiciona um filho ao nó "conteudo" chamando a função 'expAritmetica'
            elemento.adicionar_filho(expAritmetica(tokens))
            #retorna o nó "conteudo" completo
            return elemento
        
        #adiciona um filho ao nó "conteudo" chamando a função 'retornoFuncao'
        elemento.adicionar_filho(retornoFuncao(tokens))
        #retorna o nó "conteudo" completo
        return elemento
        
    elif tokens[0][0] == "NUM_INT":
        #adiciona um filho ao nó "conteudo" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é um operador aritmético
        if (tokens[0][1] == "+" or tokens[0][1] == "-" or tokens[0][1] == "/" or tokens[0][1] == "*" or tokens[0][1] == "//"):
            #adiciona um filho ao nó "conteudo" chamando a função 'operadorA'
            elemento.adicionar_filho(operadorA(tokens))
            #adiciona um filho ao nó "conteudo" chamando a função 'expAritmetica'
            elemento.adicionar_filho(expAritmetica(tokens))
            #retorna o nó "conteudo" completo
            return elemento
        
        #retorna o nó "conteudo" completo
        return elemento
        
    elif tokens[0][0] == "NUM_FLU":
        #adiciona um filho ao nó "conteudo" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é um operador aritmético
        if (tokens[0][1] == "+" or tokens[0][1] == "-" or tokens[0][1] == "/" or tokens[0][1] == "*" or tokens[0][1] == "//"):
            #adiciona um filho ao nó "conteudo" chamando a função 'operadorA'
            elemento.adicionar_filho(operadorA(tokens))
            #adiciona um filho ao nó "conteudo" chamando a função 'expAritmetica'
            elemento.adicionar_filho(expAritmetica(tokens))
            #retorna o nó "conteudo" completo
            return elemento
        
        #retorna o nó "conteudo" completo
        return elemento
        
    elif tokens[0][0] == "TEXT":
        #adiciona um filho ao nó "conteudo" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        #retorna o nó "conteudo" completo
        return elemento
        
    elif tokens[0][1] == "(":
        #adiciona um filho ao nó "conteudo" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #adiciona um filho ao nó "conteudo" chamando a função 'expAritmetica'
        elemento.adicionar_filho(expAritmetica(tokens))
        
        #verifica se o próximo token é ")"
        if tokens[0][1] == ")":
            #adiciona um filho ao nó "conteudo" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            #retorna o nó "conteudo" completo
            return elemento
        else:
            #se não houver ")", gera um erro indicando a falta de ")" na linha do token atual
            assert False, "Faltando ) na linha " + str(tokens[0][2])
    else:
        #se não houver correspondência, gera um erro indicando a falta de conteudo na linha do token atual
        assert False, "Faltando conteudo na linha " + str(tokens[0][2])

def retornoFuncao(tokens):
    #cria um nó chamado "retornoFuncao"
    elemento = No("retornoFuncao")
    
    #verifica se o próximo token é "["
    if tokens[0][1] == "[":
        #adiciona um filho ao nó "retornoFuncao" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #adiciona um filho ao nó "retornoFuncao" chamando a função 'argumento3'
        elemento.adicionar_filho(argumento3(tokens))
        
        #verifica se o próximo token é "]"
        if tokens[0][1] == "]":
            #adiciona um filho ao nó "retornoFuncao" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            #retorna o nó "retornoFuncao" completo
            return elemento
        else:
            #se não houver "]", gera um erro indicando a falta de "]" na linha do token atual
            assert False, "Faltando ] na linha " + str(tokens[0][2])
    else:
        #se não houver "[", retorna o nó "retornoFuncao" vazio
        return elemento

def expAritmetica(tokens):
    #cria um nó chamado "expAritmetica"
    elemento = No("expAritmetica")
    
    #verifica o tipo do primeiro token para determinar a estrutura apropriada
    if tokens[0][0] == "IDENTIFICADOR" or tokens[0][0] == "NUM_INT" or tokens[0][0] == "NUM_FLU":
        #adiciona um filho ao nó "expAritmetica" chamando a função 'valor'
        elemento.adicionar_filho(valor(tokens))
        
        #verifica se o próximo token é um operador aritmético
        if tokens[0][1] == "+" or tokens[0][1] == "-" or tokens[0][1] == "/" or tokens[0][1] == "*" or tokens[0][1] == "//":
            #adiciona um filho ao nó "expAritmetica" chamando a função 'operadorA'
            elemento.adicionar_filho(operadorA(tokens))
            #adiciona um filho ao nó "expAritmetica" chamando a função 'expAritmetica2'
            elemento.adicionar_filho(expAritmetica2(tokens))
            #retorna o nó "expAritmetica" completo
            return elemento
        else:
            #se não houver operador aritmético, retorna o nó "expAritmetica" com um único filho
            return elemento
    else:
        #se não houver valor, gera um erro indicando a falta de valor na linha do token atual
        assert False, "Faltando valor na linha " + str(tokens[0][2])

def expAritmetica2(tokens):
    #cria um nó chamado "expAritmetica2"
    elemento = No("expAritmetica2")
    
    #verifica se o próximo token é "("
    if tokens[0][1] == "(":
        #adiciona um filho ao nó "expAritmetica2" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #adiciona um filho ao nó "expAritmetica2" chamando a função 'expAritmetica2'
        elemento.adicionar_filho(expAritmetica2(tokens))
        
        #verifica se o próximo token é ")"
        if tokens[0][1] == ")":
            #adiciona um filho ao nó "expAritmetica2" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            #retorna o nó "expAritmetica2" completo
            return elemento
        else:
            #se não houver ")", gera um erro indicando a falta de ")" na linha do token atual
            assert False, "Faltando ) na linha " + str(tokens[0][2])
    else:
        #se não houver "(", gera um erro indicando a falta de valor na linha do token atual
        assert False, "Faltando valor na linha " + str(tokens[0][2])

def operadorA(tokens):
    #cria um nó chamado "operadorA"
    elemento = No("operadorA")
    
    #verifica se o próximo token é um operador aritmético
    if tokens[0][1] == "+" or tokens[0][1] == "-" or tokens[0][1] == "/" or tokens[0][1] == "*" or tokens[0][1] == "//":
        #adiciona um filho ao nó "operadorA" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        #retorna o nó "operadorA" completo
        return elemento
    else:
        #se não houver operador aritmético, gera um erro indicando a falta de operador aritmético na linha do token atual
        assert False, "Faltando operador aritmetico na linha " + str(tokens[0][2])

def valor(tokens):
    #cria um nó chamado "valor"
    elemento = No("valor")
    
    #verifica o tipo do primeiro token para determinar a estrutura apropriada
    if tokens[0][0] == "IDENTIFICADOR":
        #adiciona um filho ao nó "valor" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        #retorna o nó "valor" completo
        return elemento
    elif tokens[0][0] == "NUM_INT":
        #adiciona um filho ao nó "valor" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        #retorna o nó "valor" completo
        return elemento
    elif tokens[0][0] == "NUM_FLU":
        #adiciona um filho ao nó "valor" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        #retorna o nó "valor" completo
        return elemento
    else:
        #se não houver correspondência, gera um erro indicando a falta de valor na linha do token atual
        assert False, "Faltando valor na linha " + str(tokens[0][2])

def entrada(tokens):
    #cria um nó chamado "entrada"
    elemento = No("entrada")
    
    #verifica se o próximo token é "textin"
    if tokens[0][1] == "textin":
        #adiciona um filho ao nó "entrada" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é "["
        if tokens[0][1] == "[":
            #adiciona um filho ao nó "entrada" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #verifica se o próximo token é um IDENTIFICADOR
            if tokens[0][0] == "IDENTIFICADOR":
                #adiciona um filho ao nó "entrada" com o valor e tipo do token atual
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                #remove o token processado da lista de tokens
                tokens.pop(0)
                
                #verifica se o próximo token é "]"
                if tokens[0][1] == "]":
                    #adiciona um filho ao nó "entrada" com o valor e tipo do token atual
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    #remove o token processado da lista de tokens
                    tokens.pop(0)
                    
                    #verifica se o próximo token é ";"
                    if tokens[0][1] == ";":
                        #adiciona um filho ao nó "entrada" com o valor e tipo do token atual
                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                        #remove o token processado da lista de tokens
                        tokens.pop(0)
                        
                        #adiciona um filho ao nó "entrada" chamando a função 'programa'
                        elemento.adicionar_filho(programa(tokens))
                        #retorna o nó "entrada" completo
                        return elemento
                    else:
                        #se não houver ponto e vírgula, gera um erro indicando a falta de ";" na linha do token atual
                        assert False, "Faltando ; na linha " + str(tokens[0][2])
                else:
                    #se não houver "]", gera um erro indicando a falta de "]" na linha do token atual
                    assert False, "Faltando ] na linha " + str(tokens[0][2])
            else:
                #se não houver IDENTIFICADOR, gera um erro indicando a falta de IDENTIFICADOR na linha do token atual
                assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
        else:
            #se não houver "[", gera um erro indicando a falta de "[" na linha do token atual
            assert False, "Faltando [ na linha " + str(tokens[0][2])
    else:
        #se não houver "textin", gera um erro indicando a falta de "textin" na linha do token atual
        assert False, "Faltando textin na linha " + str(tokens[0][2])
def saida(tokens):
    #cria um nó chamado "saida"
    elemento = No("saida")
    
    #verifica se o próximo token é "puts"
    if tokens[0][1] == "puts":
        #adiciona um filho ao nó "saida" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é "["
        if tokens[0][1] == "[":
            #adiciona um filho ao nó "saida" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #adiciona um filho ao nó "saida" chamando a função 'conteudo'
            elemento.adicionar_filho(conteudo(tokens))
            
            #verifica se o próximo token é "]"
            if tokens[0][1] == "]":
                #adiciona um filho ao nó "saida" com o valor e tipo do token atual
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                #remove o token processado da lista de tokens
                tokens.pop(0)
                
                #verifica se o próximo token é ";"
                if tokens[0][1] == ";":
                    #adiciona um filho ao nó "saida" com o valor e tipo do token atual
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    #remove o token processado da lista de tokens
                    tokens.pop(0)
                    
                    #adiciona um filho ao nó "saida" chamando a função 'programa'
                    elemento.adicionar_filho(programa(tokens))
                    #retorna o nó "saida" completo
                    return elemento
                else:
                    #se não houver ponto e vírgula, gera um erro indicando a falta de ";" na linha do token atual
                    assert False, "Faltando ; na linha " + str(tokens[0][2])
            else:
                #se não houver "]", gera um erro indicando a falta de "]" na linha do token atual
                assert False, "Faltando ] na linha " + str(tokens[0][2])
        else:
            #se não houver "[", gera um erro indicando a falta de "[" na linha do token atual
            assert False, "Faltando [ na linha " + str(tokens[0][2])
    else:
        #se não houver "puts", gera um erro indicando a falta de "puts" na linha do token atual
        assert False, "Faltando puts na linha " + str(tokens[0][2])

def desvio(tokens):
    #cria um nó chamado "desvio"
    elemento = No("desvio")
    
    #verifica se o próximo token é "case"
    if tokens[0][1] == "case":
        #adiciona um filho ao nó "desvio" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é "["
        if tokens[0][1] == "[":
            #adiciona um filho ao nó "desvio" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #adiciona um filho ao nó "desvio" chamando a função 'termoRelacional'
            elemento.adicionar_filho(termoRelacional(tokens))
            
            #verifica se o próximo token é "]"
            if tokens[0][1] == "]":
                #adiciona um filho ao nó "desvio" com o valor e tipo do token atual
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                #remove o token processado da lista de tokens
                tokens.pop(0)
                
                #verifica se o próximo token é "@"
                if tokens[0][1] == "@":
                    #adiciona um filho ao nó "desvio" com o valor e tipo do token atual
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    #remove o token processado da lista de tokens
                    tokens.pop(0)
                    
                    #adiciona um filho ao nó "desvio" chamando a função 'programa'
                    elemento.adicionar_filho(programa(tokens))
                    
                    #verifica se o próximo token é "@"
                    if tokens[0][1] == "@":
                        #adiciona um filho ao nó "desvio" com o valor e tipo do token atual
                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                        #remove o token processado da lista de tokens
                        tokens.pop(0)
                        
                        #adiciona um filho ao nó "desvio" chamando a função 'programa'
                        elemento.adicionar_filho(programa(tokens))
                        
                        #verifica se o próximo token é "ordo"
                        if tokens[0][1] == "ordo":
                            #adiciona um filho ao nó "desvio" chamando a função 'desvio2'
                            elemento.adicionar_filho(desvio2(tokens))
                        
                        #retorna o nó "desvio" completo
                        return elemento
                    else:
                        #se não houver "@", gera um erro indicando a falta de "@" na linha do token atual
                        assert False, "Faltando @ na linha " + str(tokens[0][2])
                else:
                    #se não houver "@", gera um erro indicando a falta de "@" na linha do token atual
                    assert False, "Faltando @ na linha " + str(tokens[0][2])
            else:
                #se não houver "]", gera um erro indicando a falta de "]" na linha do token atual
                assert False, "Faltando ] na linha " + str(tokens[0][2])
        else:
            #se não houver "[", gera um erro indicando a falta de "[" na linha do token atual
            assert False, "Faltando [ na linha " + str(tokens[0][2])
    else:
        #se não houver "case", gera um erro indicando a falta de "case" na linha do token atual
        assert False, "Faltando case na linha " + str(tokens[0][2])

def desvio2(tokens):
    #cria um nó chamado "desvio2"
    elemento = No("desvio2")
    
    #verifica se o próximo token é "ordo"
    if tokens[0][1] == "ordo":
        #adiciona um filho ao nó "desvio2" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é "@"
        if tokens[0][1] == "@":
            #adiciona um filho ao nó "desvio2" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #adiciona um filho ao nó "desvio2" chamando a função 'programa'
            elemento.adicionar_filho(programa(tokens))
            
            #verifica se o próximo token é "@"
            if tokens[0][1] == "@":
                #adiciona um filho ao nó "desvio2" com o valor e tipo do token atual
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                #remove o token processado da lista de tokens
                tokens.pop(0)
                
                #retorna o nó "desvio2" completo
                return elemento
            else:
                #se não houver "@", gera um erro indicando a falta de "@" na linha do token atual
                assert False, "Faltando @ na linha " + str(tokens[0][2])
        else:
            #se não houver "@", gera um erro indicando a falta de "@" na linha do token atual
            assert False, "Faltando @ na linha " + str(tokens[0][2])
    else:
        #se não houver "ordo", gera um erro indicando a falta de "ordo" na linha do token atual
        assert False, "Faltando ordo na linha " + str(tokens[0][2])

def termoRelacional(tokens):
    #cria um nó chamado "termoRelacional"
    elemento = No("termoRelacional")
    
    #verifica se o próximo token é do tipo adequado
    if tokens[0][0] == "IDENTIFICADOR" or tokens[0][0] == "NUM_INT" or tokens[0][0] == "NUM_FLU" or tokens[0][1] == "TEXT":
        #adiciona um filho ao nó "termoRelacional" chamando a função 'conteudo'
        elemento.adicionar_filho(conteudo(tokens))
        #adiciona um filho ao nó "termoRelacional" chamando a função 'simboloRelacional'
        elemento.adicionar_filho(simboloRelacional(tokens))
        #adiciona um filho ao nó "termoRelacional" chamando a função 'termoRelacional2'
        elemento.adicionar_filho(termoRelacional2(tokens))
        #retorna o nó "termoRelacional" completo
        return elemento
    else:
        #se o tipo de token não for o esperado, gera um erro indicando a falta de conteúdo na linha do token atual
        assert False, "Faltando conteudo na linha " + str(tokens[0][2])

def simboloRelacional(tokens):
    #cria um nó chamado "simboloRelacional"
    elemento = No("simboloRelacional")
    
    #verifica se o próximo token é um dos símbolos relacionais esperados
    if tokens[0][1] == "<<" or tokens[0][1] == ">>" or tokens[0][1] == ">=" or tokens[0][1] == "<=" or tokens[0][1] == "==" or tokens[0][1] == "!=" or tokens[0][1] == "ok" or tokens[0][1] == "notok":
        #adiciona um filho ao nó "simboloRelacional" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        #retorna o nó "simboloRelacional" completo
        return elemento
    else:
        #se o símbolo relacional não for o esperado, gera um erro indicando a falta de símbolo relacional na linha do token atual
        assert False, "Faltando simbolo relacional na linha " + str(tokens[0][2])

def termoRelacional2(tokens):
    #cria um nó chamado "termoRelacional2"
    elemento = No("termoRelacional2")
    
    #verifica se o próximo token é do tipo adequado
    if tokens[0][0] == "IDENTIFICADOR" or tokens[0][0] == "NUM_INT" or tokens[0][0] == "NUM_FLU" or tokens[0][1] == "TEXT":
        #adiciona um filho ao nó "termoRelacional2" chamando a função 'conteudo'
        elemento.adicionar_filho(conteudo(tokens))
        
        #verifica se o próximo token é "&&" ou "||"
        if tokens[0][1] == "&&" or tokens[0][1] == "||":
            #adiciona um filho ao nó "termoRelacional2" chamando a função 'termoLogico'
            elemento.adicionar_filho(termoLogico(tokens))
            #adiciona um filho ao nó "termoRelacional2" chamando a função 'termoRelacional'
            elemento.adicionar_filho(termoRelacional(tokens))
        
        #retorna o nó "termoRelacional2" completo
        return elemento
    else:
        #se o tipo de token não for o esperado, gera um erro indicando a falta de conteúdo na linha do token atual
        assert False, "Faltando conteudo na linha " + str(tokens[0][2])

def termoLogico(tokens):
    #cria um nó chamado "termoLogico"
    elemento = No("termoLogico")
    
    #verifica se o próximo token é "&&" ou "||"
    if tokens[0][1] == "&&" or tokens[0][1] == "||":
        #adiciona um filho ao nó "termoLogico" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #retorna o nó "termoLogico" completo
        return elemento
    else:
        #se o operador lógico não for o esperado, retorna o nó "termoLogico" vazio
        return elemento

def funcao(tokens):
    #cria um nó chamado "funcao"
    elemento = No("funcao")
    
    #verifica se o próximo token é "fn"
    if tokens[0][1] == "fn":
        #adiciona um filho ao nó "funcao" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é do tipo adequado
        if tokens[0][0] == "IDENTIFICADOR":
            #adiciona um filho ao nó "funcao" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #verifica se o próximo token é "["
            if tokens[0][1] == "[":
                #adiciona um filho ao nó "funcao" com o valor e tipo do token atual
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                #remove o token processado da lista de tokens
                tokens.pop(0)
                
                #adiciona um filho ao nó "funcao" chamando a função 'argumento'
                elemento.adicionar_filho(argumento(tokens))
                
                #verifica se o próximo token é "]"
                if tokens[0][1] == "]":
                    #adiciona um filho ao nó "funcao" com o valor e tipo do token atual
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    #remove o token processado da lista de tokens
                    tokens.pop(0)
                    
                    #verifica se o próximo token é "@"
                    if tokens[0][1] == "@":
                        #adiciona um filho ao nó "funcao" com o valor e tipo do token atual
                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                        #remove o token processado da lista de tokens
                        tokens.pop(0)
                        
                        #adiciona um filho ao nó "funcao" chamando a função 'programa'
                        elemento.adicionar_filho(programa(tokens))
                        
                        #verifica se o próximo token é "@"
                        if tokens[0][1] == "@":
                            #adiciona um filho ao nó "funcao" com o valor e tipo do token atual
                            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                            #remove o token processado da lista de tokens
                            tokens.pop(0)
                            
                            #adiciona um filho ao nó "funcao" chamando a função 'programa'
                            elemento.adicionar_filho(programa(tokens))
                            
                            #retorna o nó "funcao" completo
                            return elemento
                        else:
                            #se não houver "@", gera um erro indicando a falta de "@" na linha do token atual
                            assert False, "Faltando @ na linha " + str(tokens[0][2])
                    else:
                        #se não houver "@", gera um erro indicando a falta de "@" na linha do token atual
                        assert False, "Faltando @ na linha " + str(tokens[0][2])
                else:
                    #se não houver "]", gera um erro indicando a falta de "]" na linha do token atual
                    assert False, "Faltando ] na linha " + str(tokens[0][2])
            else:
                #se não houver "[", gera um erro indicando a falta de "[" na linha do token atual
                assert False, "Faltando [ na linha " + str(tokens[0][2])
        else:
            #se o tipo de token não for o esperado, gera um erro indicando a falta de IDENTIFICADOR na linha do token atual
            assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
    else:
        #se não houver "fn", gera um erro indicando a falta de "fn" na linha do token atual
        assert False, "Faltando fn na linha " + str(tokens[0][2])

def argumento(tokens):
    #cria um nó chamado "argumento"
    elemento = No("argumento")
    
    #verifica se o próximo token é "num_int", "num_flu" ou "text"
    if tokens[0][1] == "num_int" or tokens[0][1] == "num_flu" or tokens[0][1] == "text":
        #adiciona um filho ao nó "argumento" chamando a função 'tipoVar'
        elemento.adicionar_filho(tipoVar(tokens))
        
        #verifica se o próximo token é do tipo IDENTIFICADOR
        if tokens[0][0] == "IDENTIFICADOR":
            #adiciona um filho ao nó "argumento" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #adiciona um filho ao nó "argumento" chamando a função 'argumento2'
            elemento.adicionar_filho(argumento2(tokens))
            
            #retorna o nó "argumento" completo
            return elemento
        else:
            #se o tipo de token não for o esperado, gera um erro indicando a falta de IDENTIFICADOR na linha do token atual
            assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
    else:
        #se o próximo token não for "num_int", "num_flu" ou "text", retorna o nó "argumento" vazio
        return elemento

def argumento2(tokens):
    #cria um nó chamado "argumento2"
    elemento = No("argumento2")
    
    #verifica se o próximo token é ","
    if tokens[0][1] == ",":
        #adiciona um filho ao nó "argumento2" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #adiciona um filho ao nó "argumento2" chamando a função 'argumento'
        elemento.adicionar_filho(argumento(tokens))
        
        #retorna o nó "argumento2" completo
        return elemento
    else:
        #se o próximo token não for ",", retorna o nó "argumento2" vazio
        return elemento

def retorno(tokens):
    #cria um nó chamado "retorno"
    elemento = No("retorno")
    
    #verifica se o próximo token é "take"
    if tokens[0][1] == "take":
        #adiciona um filho ao nó "retorno" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #adiciona um filho ao nó "retorno" chamando a função 'conteudo'
        elemento.adicionar_filho(conteudo(tokens))
        
        #verifica se o próximo token é ";"
        if tokens[0][1] == ";":
            #adiciona um filho ao nó "retorno" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #retorna o nó "retorno" completo
            return elemento
        else:
            #se o próximo token não for ";", gera um erro indicando a falta de ";" na linha do token atual
            assert False, "Faltando ; na linha " + str(tokens[0][2])
    else:
        #se o próximo token não for "take", gera um erro indicando a falta de "take" na linha do token atual
        assert False, "Faltando take na linha " + str(tokens[0][2])

def laco(tokens):
    #cria um nó chamado "laco"
    elemento = No("laco")
    
    #verifica se o próximo token é "when"
    if tokens[0][1] == "when":
        #adiciona um filho ao nó "laco" chamando a função 'while_'
        elemento.adicionar_filho(while_(tokens))
        #retorna o nó "laco" completo
        return elemento
    #verifica se o próximo token é "to"
    elif tokens[0][1] == "to":
        #adiciona um filho ao nó "laco" chamando a função 'for_'
        elemento.adicionar_filho(for_(tokens))
        #retorna o nó "laco" completo
        return elemento
    else:
        #se o próximo token não for "when" ou "to", gera um erro indicando a falta de "laco" na linha do token atual
        assert False, "Faltando laco na linha " + str(tokens[0][2])

def while_(tokens):
    #cria um nó chamado "while"
    elemento = No("while")
    
    #verifica se o próximo token é "when"
    if tokens[0][1] == "when":
        #adiciona um filho ao nó "while" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é "["
        if tokens[0][1] == "[":
            #adiciona um filho ao nó "while" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #adiciona um filho ao nó "while" chamando a função 'termoRelacional'
            elemento.adicionar_filho(termoRelacional(tokens))
            
            #verifica se o próximo token é "]"
            if tokens[0][1] == "]":
                #adiciona um filho ao nó "while" com o valor e tipo do token atual
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                #remove o token processado da lista de tokens
                tokens.pop(0)
                
                #verifica se o próximo token é "@"
                if tokens[0][1] == "@":
                    #adiciona um filho ao nó "while" com o valor e tipo do token atual
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    #remove o token processado da lista de tokens
                    tokens.pop(0)
                    
                    #adiciona um filho ao nó "while" chamando a função 'programa'
                    elemento.adicionar_filho(programa(tokens))
                    
                    #verifica se o próximo token é "@"
                    if tokens[0][1] == "@":
                        #adiciona um filho ao nó "while" com o valor e tipo do token atual
                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                        #remove o token processado da lista de tokens
                        tokens.pop(0)
                        
                        #adiciona um filho ao nó "while" chamando a função 'programa'
                        elemento.adicionar_filho(programa(tokens))
                        
                        #retorna o nó "while" completo
                        return elemento
                    else:
                        #se o próximo token não for "@", gera um erro indicando a falta de "@" na linha do token atual
                        assert False, "Faltando @ na linha " + str(tokens[0][2])
                else:
                    #se o próximo token não for "@", gera um erro indicando a falta de "@" na linha do token atual
                    assert False, "Faltando @ na linha " + str(tokens[0][2])
            else:
                #se o próximo token não for "]", gera um erro indicando a falta de "]" na linha do token atual
                assert False, "Faltando ] na linha " + str(tokens[0][2])
        else:
            #se o próximo token não for "[", gera um erro indicando a falta de "[" na linha do token atual
            assert False, "Faltando [ na linha " + str(tokens[0][2])
    else:
        #se o próximo token não for "when", gera um erro indicando a falta de "when" na linha do token atual
        assert False, "Faltando when na linha " + str(tokens[0][2])


def for_(tokens):
    #cria um nó chamado "for"
    elemento = No("for")
    
    #verifica se o próximo token é "to"
    if tokens[0][1] == "to":
        #adiciona um filho ao nó "for" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #verifica se o próximo token é "["
        if tokens[0][1] == "[":
            #adiciona um filho ao nó "for" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #verifica se o próximo token é "num_int"
            if tokens[0][1] == "num_int":
                #adiciona um filho ao nó "for" com o valor e tipo do token atual
                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                #remove o token processado da lista de tokens
                tokens.pop(0)
                
                #verifica se o próximo token é do tipo IDENTIFICADOR
                if tokens[0][0] == "IDENTIFICADOR":
                    #adiciona um filho ao nó "for" com o valor e tipo do token atual
                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                    #remove o token processado da lista de tokens
                    tokens.pop(0)
                    
                    #verifica se o próximo token é "->"
                    if tokens[0][1] == "->":
                        #adiciona um filho ao nó "for" com o valor e tipo do token atual
                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                        #remove o token processado da lista de tokens
                        tokens.pop(0)
                        
                        #verifica se o próximo token é "NUM_INT"
                        if tokens[0][0] == "NUM_INT":
                            #adiciona um filho ao nó "for" com o valor e tipo do token atual
                            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                            #remove o token processado da lista de tokens
                            tokens.pop(0)
                            
                            #verifica se o próximo token é ","
                            if tokens[0][1] == ",":
                                #adiciona um filho ao nó "for" com o valor e tipo do token atual
                                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                #remove o token processado da lista de tokens
                                tokens.pop(0)
                                
                                #verifica se o próximo token é do tipo IDENTIFICADOR
                                if tokens[0][0] == "IDENTIFICADOR":
                                    #adiciona um filho ao nó "for" com o valor e tipo do token atual
                                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                    #remove o token processado da lista de tokens
                                    tokens.pop(0)
                                    
                                    #verifica se o próximo token é "<<" ou ">>" ou ">=" ou "<=" ou "==" ou "!=" ou "ok" ou "notok"
                                    if tokens[0][1] == "<<" or tokens[0][1] == ">>" or tokens[0][1] == ">=" or tokens[0][1] == "<=" or tokens[0][1] == "==" or tokens[0][1] == "!=" or tokens[0][1] == "ok" or tokens[0][1] == "notok":
                                        #adiciona um filho ao nó "for" chamando a função 'simboloRelacional'
                                        elemento.adicionar_filho(simboloRelacional(tokens))
                                        
                                        #verifica se o próximo token é do tipo NUM_INT
                                        if tokens[0][0] == "NUM_INT":
                                            #adiciona um filho ao nó "for" com o valor e tipo do token atual
                                            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                            #remove o token processado da lista de tokens
                                            tokens.pop(0)
                                            
                                            #verifica se o próximo token é ","
                                            if tokens[0][1] == ",":
                                                #adiciona um filho ao nó "for" com o valor e tipo do token atual
                                                elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                                #remove o token processado da lista de tokens
                                                tokens.pop(0)
                                                
                                                #adiciona um filho ao nó "for" chamando a função 'incrementa'
                                                elemento.adicionar_filho(incrementa(tokens))
                                                
                                                #verifica se o próximo token é "]"
                                                if tokens[0][1] == "]":
                                                    #adiciona um filho ao nó "for" com o valor e tipo do token atual
                                                    elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                                    #remove o token processado da lista de tokens
                                                    tokens.pop(0)
                                                    
                                                    #verifica se o próximo token é "@"
                                                    if tokens[0][1] == "@":
                                                        #adiciona um filho ao nó "for" com o valor e tipo do token atual
                                                        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                                        #remove o token processado da lista de tokens
                                                        tokens.pop(0)
                                                        
                                                        #adiciona um filho ao nó "for" chamando a função 'programa'
                                                        elemento.adicionar_filho(programa(tokens))
                                                        
                                                        #verifica se o próximo token é "@"
                                                        if tokens[0][1] == "@":
                                                            #adiciona um filho ao nó "for" com o valor e tipo do token atual
                                                            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
                                                            #remove o token processado da lista de tokens
                                                            tokens.pop(0)
                                                            
                                                            #adiciona um filho ao nó "for" chamando a função 'programa'
                                                            elemento.adicionar_filho(programa(tokens))
                                                            
                                                            #retorna o nó "for" completo
                                                            return elemento
                                                        else:
                                                            #se o próximo token não for "@", gera um erro indicando a falta de "@" na linha do token atual
                                                            assert False, "Faltando @ na linha " + str(tokens[0][2])
                                                    else:
                                                        #se o próximo token não for "@", gera um erro indicando a falta de "@" na linha do token atual
                                                        assert False, "Faltando @ na linha " + str(tokens[0][2])
                                                else:
                                                    #se o próximo token não for "]", gera um erro indicando a falta de "]" na linha do token atual
                                                    assert False, "Faltando ] na linha " + str(tokens[0][2])
                                            else:
                                                #se o próximo token não for ",", gera um erro indicando a falta de "," na linha do token atual
                                                assert False, "Faltando ',' na linha " + str(tokens[0][2])
                                        else:
                                            #se o próximo token não for do tipo NUM_INT, gera um erro indicando a falta de número inteiro na linha do token atual
                                            assert False, "Faltando numero inteiro na linha " + str(tokens[0][2])
                                    else:
                                        #se o próximo token não for "<<" ou ">>" ou ">=" ou "<=" ou "==" ou "!=" ou "ok" ou "notok", gera um erro indicando a falta de símbolo relacional na linha do token atual
                                        assert False, "Faltando simbolo relacional na linha " + str(tokens[0][2])
                                else:
                                    #se o próximo token não for do tipo IDENTIFICADOR, gera um erro indicando a falta de IDENTIFICADOR na linha do token atual
                                    assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
                            else:
                                #se o próximo token não for ",", gera um erro indicando a falta de "," na linha do token atual
                                assert False, "Faltando ',' na linha " + str(tokens[0][2])
                        else:
                            #se o próximo token não for do tipo NUM_INT, gera um erro indicando a falta de número inteiro na linha do token atual
                            assert False, "Faltando numero inteiro na linha " + str(tokens[0][2])
                    else:
                        #se o próximo token não for "->", gera um erro indicando a falta de '->' na linha do token atual
                        assert False, "Faltando '->' na linha " + str(tokens[0][2])
                else:
                    #se o próximo token não for do tipo IDENTIFICADOR, gera um erro indicando a falta de IDENTIFICADOR na linha do token atual
                    assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])
            else:
                #se o próximo token não for "num_int", gera um erro indicando a falta de num_int na linha do token atual
                assert False, "Faltando num_int na linha " + str(tokens[0][2])
        else:
            #se o próximo token não for "[", gera um erro indicando a falta de "[" na linha do token atual
            assert False, "Faltando '[' na linha " + str(tokens[0][2])
    else:
        #se o próximo token não for "to", gera um erro indicando a falta de 'to' na linha do token atual
        assert False, "Faltando 'to' na linha " + str(tokens[0][2])

def argumento3(tokens):
    #cria um nó chamado "argumento3"
    elemento = No("argumento3")
    
    #verifica se o próximo token é do tipo IDENTIFICADOR, NUM_INT, NUM_FLU ou TEXT
    if tokens[0][0] == "IDENTIFICADOR" or tokens[0][0] == "NUM_INT" or tokens[0][0] == "NUM_FLU" or tokens[0][1] == "TEXT":
        #adiciona um filho ao nó "argumento3" chamando a função 'conteudo'
        elemento.adicionar_filho(conteudo(tokens))
        
        #verifica se o próximo token é ","
        if tokens[0][1] == ",":
            #adiciona um filho ao nó "argumento3" com o valor e tipo do token atual
            elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
            #remove o token processado da lista de tokens
            tokens.pop(0)
            
            #adiciona um filho ao nó "argumento3" chamando recursivamente a função 'argumento3'
            elemento.adicionar_filho(argumento3(tokens))
            
            #retorna o nó "argumento3" completo
            return elemento
        
        #se não houver vírgula, retorna o nó "argumento3" sem adicionar mais filhos
        return elemento
    
    else:
        #se o próximo token não for do tipo IDENTIFICADOR, NUM_INT, NUM_FLU ou TEXT, gera um erro indicando a falta de conteúdo na linha do token atual
        assert False, "Faltando conteudo na linha " + str(tokens[0][2])

def incrementa(tokens):
    #cria um nó chamado "incrementa"
    elemento = No("incrementa")
    
    #verifica se o próximo token é do tipo IDENTIFICADOR
    if tokens[0][0] == "IDENTIFICADOR":
        #adiciona um filho ao nó "incrementa" com o valor e tipo do token atual
        elemento.adicionar_filho(No(tokens[0][0], tokens[0][1]))
        #remove o token processado da lista de tokens
        tokens.pop(0)
        
        #adiciona um filho ao nó "incrementa" chamando a função 'operadorA'
        elemento.adicionar_filho(operadorA(tokens))
        
        #adiciona um filho ao nó "incrementa" chamando a função 'valor'
        elemento.adicionar_filho(valor(tokens))
        
        #retorna o nó "incrementa" completo
        return elemento
    
    else:
        #se o próximo token não for do tipo IDENTIFICADOR, gera um erro indicando a falta de IDENTIFICADOR na linha do token atual
        assert False, "Faltando IDENTIFICADOR na linha " + str(tokens[0][2])


#classe para representar um nó na árvore sintática

#Este é o método construtor da classe. Ele é chamado quando um novo objeto da classe No é criado. O construtor aceita dois parâmetros obrigatórios: tipo e lexema, e um parâmetro opcional lexema que é inicializado com o valor padrão None. 
class No:
    def __init__(self, tipo, lexema=None):
        self.tipo = tipo        #Armazena o tipo do nó, como uma string.
        self.lexema = lexema    #Armazena o lexema associado ao nó, que pode ser None se o nó não contiver um lexema.
        self.filhos = []        #Armazena uma lista dos filhos (subárvores) deste nó na árvore sintática.
    
    def __repr__(self, profundidade=0): #Este é um método especial que fornece uma representação de string para o objeto No. Ele é chamado quando o objeto No precisa ser convertido em uma string. O parâmetro opcional profundidade é utilizado para controlar a indentação da representação da árvore sintática.
        indentacao = "\t |--" * profundidade
        representacao = f"{indentacao}{repr(self.tipo)}{repr(self.lexema)}\n"

        for filho in self.filhos:
            representacao += filho.__repr__(profundidade + 1)

        return representacao

    def adicionar_filho(self, elemento):    #Este método adiciona um novo filho (subárvore) ao nó atual. Ele aceita um parâmetro elemento, que representa um nó filho a ser adicionado à lista de filhos (self.filhos).
        self.filhos.append(elemento)


#função principal que constrói a árvore sintática
def arvore(tokens): 
    #cria um nó chamado "Arvore Sintatica"
    raiz = No("Arvore Sintatica")
    
    #adiciona um filho à raiz chamando a função 'inicio'
    raiz.adicionar_filho(inicio(tokens))
    
    #retorna a raiz da árvore sintática
    return raiz
