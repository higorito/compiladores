#include<iostream>
#include<sstrem> //fluxo de stream, um "buffer"
#include "lexico.h"

using namespace std;

Lexico::Lexico(){
    //palavras reservadas for while if.....
    id_tabela[""] = id
}

Token Lexico::Escanear(){
    while(isspace(peek)){
        if(peek == '\n')
            linha +=1; //ma pratica tive q colocar protected
        peek.cin.get();
    }

    if(isdigit(peek)){
        int num = 0;

        do{
            int n = peek - '0';
            v = 10*num+n;

            peek = cin.get();
        }while(isdigit(peek));

        count<<"<num_int, "<<num<<" > ";

        return Num_int{num};

    }

    //se nao for digito pd ser palavra chave ou id

    if(isalpha(peek)){
        stringstream ss;
        //tipo um buffer q analisa enquanto ele for letra
        do{
            ss <<peek;
            peek = cin.get();
        }while(isalpha(peek));

        string s = ss.str();

        auto pos = id_tabela.find(s);

        if(pos !id_tabela.end()){
            switch(pos->second.tag){
                default: cout<<"ID, "<<pos->second.name<<">";break;
            }
            return pos->second;
        }


        Token::ID() new



    }
}
