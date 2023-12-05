#ifndef TOKEN_H_INCLUDED
#define TOKEN_H_INCLUDED


#include<string>
#include<unordered_map>
using namespace std;

enum Contantes {NUM_INT = 256, num_float,id, ok, notok };


class Token{
protected:
    int tag;
public:
    Token();
    Token(int tag){
        this->tag = tag;
    }
    virtual ~ Token();
};

class ID : public Token{
protected:
    string nome;
public:
    ID();
    ID(Token.tag tok_tag){
        this->tag = tok_tag;
    }
    ID(int tok, string nome){
       this->tag = tok;
        this->nome = nome;
    }
    virtual ~ID();
};

struct Num_int : public Token{
    int valor ;
    Num_int(int v){
        this->valor = Token(tag::NUM_INT);
    }
};

#endif // TOKEN_H_INCLUDED
