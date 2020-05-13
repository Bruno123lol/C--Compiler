with open('matriz.txt') as f:
    fil, col = [int(x) for x in next(f).split()]
    simbolos = next(f).split(',')
    M = [[int(x) for x in line.split()] for line in f]


f = open('ejemplo.txt', 'r')
archivo = f.read() 		# lee todo el archivo a tokenizar
archivo += '$?'                 # agregamos $ para representar EOF
longitud = len(archivo) 	# longitud del archivo
estado = 0                      # estado inicial
token = ''                      # token inicial

mapa = {}
for i in range(len(simbolos)):
    for c in simbolos[i]:
        mapa[c]=i

print(mapa)
print(M)

print("Tipo                    Token")
print("-----------------------------")
#se inicializa el contador que controlará la lectura de la string del archivo
contador = 0
#mientras el archivo no termine
while (c!='?'):
    #obtiene el caracter correspondiente a la posición del archivo
    c = archivo[contador]
    #cuando haya terminado el archivo
    if c=='?':
        break
    #se obtien el estado correspondiente al caracter que se obtuvo
    estado = M[estado][mapa[c]]
    #print("Estado : ", estado)
    if estado == 2: 
        print("Entero:                ", token)
        token = ''
        estado = 0
    elif estado == 4:
        print("Resta:                 ", token)
        token = ''
        estado = 0
    elif estado == 7:
        print("Flotante:              ", token)
        token = ''
        estado = 0
    elif estado == 14:
        print("Comentario:            ", token)
        token = ''
        estado = 0
    elif estado == 13:
        print("Division:              ", token)
        token = ''
        estado = 0
    elif estado == 16:
        print("Variable:              ", token)
        token = ''
        estado = 0
    elif estado == 17:
        token += c #Se agrega el caracter actual al token
        print("Suma:                  ", token)
        contador += 1 #se mueve la posición en el archivo porque es un token de caracter único
        token = ''
        estado = 0
    elif estado == 18:
        token += c #Se agrega el caracter actual al token
        print("Multiplicacion:        ", token)
        contador += 1 #se mueve la posición en el archivo porque es un token de caracter único
        token = ''
        estado = 0
    elif estado == 19:
        token += c #Se agrega el caracter actual al token
        print("Potencia:              ", token)
        contador += 1 #se mueve la posición en el archivo porque es un token de caracter único
        token = ''
        estado = 0
    elif estado == 20:
        token += c #Se agrega el caracter actual al token
        print("Parentesis abierto:    ", token)
        contador += 1 #se mueve la posición en el archivo porque es un token de caracter único
        token = ''
        estado = 0
    elif estado == 21:
        token += c #Se agrega el caracter actual al token
        print("Parentesis de cerrado: ", token)
        contador += 1 #se mueve la posición en el archivo porque es un token de caracter único
        token = ''
        estado = 0
    elif estado == 22:
        token += c #Se agrega el caracter actual al token
        print("Asignacion:            ", token)
        contador += 1 #se mueve la posición en el archivo porque es un token de caracter único
        token = ''
        estado = 0
    elif estado == 0: #cuando el estado es 0 solamente sumar a la  posición
        contador += 1
    elif estado != 0:
        token +=c
        contador += 1
        
