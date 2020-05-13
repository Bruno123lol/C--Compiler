from globalTypes import *


def globales(prog, pos, long):
    global programa
    global posicion
    global progLong
    programa = prog
    posicion = pos
    progLong = long
    pass

def getToken(imprime = True):
    with open('matriz.txt') as f:
        fil, col = [int(x) for x in next(f).split()]
        simbolos = next(f).split('.')
        M = [[int(x) for x in line.split()] for line in f]

    mapa = {}
    for i in range(len(simbolos)):
        for c in simbolos[i]:
            mapa[c]=i
    token = ''
    archivo = programa

    estado = 0
    print(mapa)
    print(M)
    #se inicializa el contador que controlará la lectura de la string del archivo
    contador = posicion
    #mientras el archivo no termine
    while (c!='$'):
        #obtiene el caracter correspondiente a la posición del archivo
        c = archivo[contador]
        #cuando haya terminado el archivo
        if c=='$':
            break
        #se obtien el estado correspondiente al caracter que se obtuvo
        estado = M[estado][mapa[c]]
        #print("Estado : ", estado)
        if estado == 2: 
            print(TokenType.NUM," ",token)
            token = ''
            estado = 0
        elif estado == 3:
            #token += c #Se agrega el caracter actual al token
            print(TokenType.PLUS," ",token)
            #contador += 1 #se mueve la posición en el archivo porque es un token de caracter único
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 4:
            token += c #Se agrega el caracter actual al token
            print(TokenType.LESS," ",token)
            contador += 1 #se mueve la posición en el archivo porque es un token de caracter único
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 5:
            token += c #Se agrega el caracter actual al token
            print(TokenType.MULT," ",token)
            contador += 1 #se mueve la posición en el archivo porque es un token de caracter único
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 25:
            print(TokenType.DIV," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 27:
            print(TokenType.COMMENT," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 9:
            print(TokenType.EQUAL," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 29:
            print(TokenType.LTEQUAL," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 28:
            print(TokenType.LT," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 10:
            print(TokenType.MTEQUAL," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 12:
            print(TokenType.ID," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 34:
            print(TokenType.ERR," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 14:
            print(TokenType.EQUAL," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 15:
            print(TokenType.ASSIGN," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 16:
            print(TokenType.SEMICOL," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 17:
            print(TokenType.COMMA," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 18:
            print(TokenType.OPENB," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 19:
            print(TokenType.CLOSEB," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 20:
            print(TokenType.OPENCB," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 21:
            print(TokenType.CLOSECB," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 22:
            print(TokenType.OPENSB," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 23:
            token += c #Se agrega el caracter actual al token
            print(TokenType.CLOSESB," ",token)
            contador += 1 #se mueve la posición en el archivo porque es un token de caracter único
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 35:
            print(TokenType.ERR," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 31:
            print(TokenType.DIFF," ",token)
            auxToken = token
            token = ''
            estado = 0
            return TokenType, auxToken
        elif estado == 0: #cuando el estado es 0 solamente sumar a la  posición

            contador += 1
        elif estado != 0:
            token +=c
            contador += 1
    pass
