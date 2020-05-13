from enum import Enum
#arreglo de strings con las palabras reservadas del lenguaje
reservedKeyWords = ['if','else','int','return','void','while']
#calse de enums para identificar los tokens del lenguaje
class TokenType(Enum):
    ENDFILE = 0
    ERROR = 1
    #palabras reservadas
    IF = 'if'
    ELSE = 'else'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'
    #simbolos especiales
    PLUS = '+'
    LESS = '-'
    MULT = '*'
    DIV = '/'
    LOWERTHAN = '<'
    GREATERT = '>'
    LTEQUAL = '<='
    GTEQUAL = '>='
    EQUAL = "=="
    DIFF = '!='
    ASSIGN = '='
    SEMICOL = ';'
    COMMA = ','
    OPENB = '('
    CLOSEB = ')'
    OPENSQUAREB = '['
    CLOSESQUAREB = ']'
    OPENCURLYB = '{'
    CLOSECURLYB = '}'
    #simbolos de varios caracteres
    ID = 2
    NUM = 3
    COMMENT = 4
    pass