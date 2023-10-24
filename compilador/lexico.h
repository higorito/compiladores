#ifndef LEXICO_H_INCLUDED
#define LEXICO_H_INCLUDED

#include<string>
#include<unordered_map>
#include "token.h"
using namespace std;

enum Contantes {NUM_INT = 256, num_float,id, ok, notok };



class Lexico:public Token{
protected:
        int peek = ' ';
        int linha = 1;
        unordered_map<string, id> id_tabela;

public:
    Lexico();

    Token Escanear();
    void Iniciar();


};



#endif // LEXICO_H_INCLUDED
