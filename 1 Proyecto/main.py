from globalTypes import *
from lexer import *

f = open('sample.c-', 'r')
programa = f.read()     # lee todo el archivo a compCrograma
progLong = len(programa)
programa = programa + '$'   # agregar un caracter $ que represente EOF
posicion = 0       # posición del caracter actual del string
# función para pasar los valores iniciales de las variables globales
globales(programa, posicion, progLong)
token, tokenString = getToken(False)

while (token != TokenType.ENDFILE):
    token, tokenString = getToken(True)