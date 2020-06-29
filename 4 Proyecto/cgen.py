from globalTypes import * 
from semantica import *
import sys

#variable para hacer la escritura en el archivo
file= ""
#variable global para el control de etiquetas para los if
ifCounter = 0
#variable global para el control de etiquetas para los while
whileCounter = 0
#variable global para el control de la cantidad de variables locales que tiene una función
numeroLocales = 0

#funcion para cambiar la ubicación de memoria de un parametro en específico
def changeParamLocation(funcName, paramPosition, paramLocation):
    funcScope = SymTableDictionary[0][funcName][4]
    i = 0
    for name in SymTableDictionary[funcScope]:
        if(i == paramPosition):
            SymTableDictionary[funcScope][name][0] = paramLocation
            break
        i += 1

#función para obtener el numero de parametros de una función y el numero de declaraciones locales
#nota: el numero de declaraciones locales contiene tambien el número de parametros
def getFuncInfo(name):
    numParam = SymTableDictionary[0][name][3]
    numLocalDec = SymTableDictionary[0][name][5]
    return numParam, numLocalDec

#función que controla la generación de código en ensamblador dependiendo del tipo de noso que se reciba 
def cgen(tree, checkSiblings = True):
    global ifCounter, whileCounter, numeroLocales
    if tree != None:
        shouldCheckChilds = True #variable para saber cuando se requieren checar los hijos de la rama
        if(tree.nType == TipoNodo.DEC): #si es una declaración 
            if(tree.decType == DecTipo.FUNCION): #si es la declaración de una funcón
                if(tree.child[0].str == "main"): #si es la función principal inicializar todo
                    shouldCheckChilds = False #no checar a los hijos del nodo
                    file.write("\t\t.data\n") #declarar la sección de data
                    file.write("\t\tglobalVars: .word 2\n") #declarar la variable donde se guardarán las variables globales y arreglos
                    _, numLocDec = getFuncInfo(tree.child[0].str) #obtener numero de declaraciones locales
                    file.write("\t\t.text\n") #declarar la sección de código
                    file.write("\t\t.globl main\n") #declarar que existe la función main
                    file.write("main:") #etiqueta main
                    file.write("\tla $t7, globalVars\n") #guardar la dirección de las variables globales
                    file.write("\t\tmove $fp $sp\n")  #mover el fram pointer a dónde comienza el stack
                    #push space for locals
                    z = numLocDec*4 #obtener el espacio en memoria que representan las varibales globales y archivos
                    file.write("\t\taddiu $sp, $sp, "+str(z)+"\n") #hacer espacio para dichas varibales
                    for child in tree.child: #generar código para todos los hijos
                        cgen(child)
                    file.write("\n\t\tli $v0 10\n") #Terminar el programa
                    file.write("\t\tsyscall")
                else: #si otra función
                    shouldCheckChilds = False #no checar a los hijos del nodo
                    numParams, numLocDec = getFuncInfo(tree.child[0].str) #obtener información de la función
                    file.write("\t\t.text\n") #declarar la parte del código
                    file.write(tree.child[0].str+":") #poner la etiqueta que la representa
                    z = (numParams*-4)-4 #obtener la cantidad de numero de parametros y uno más para poner la ra
                    file.write("\taddiu $sp, $sp, "+str(z)+"\n") #mover stack pointer
                    file.write("\t\tsw $ra, 0($sp)\n") #guardar la dirección de regreso
                    file.write("\t\taddiu $sp, $sp, 4\n") #mover el stack pointer
                    file.write("\t\tmove $fp, $sp\n") #mover el frame pointer a donde están las declaraciones locales
                    z = (numLocDec*4) #cantidad que se debe mover el stack pointer al final de las declaraciones
                    file.write("\t\taddiu $sp, $sp, "+str(z)+"\n")
                    numeroLocales = numLocDec #uso de varibale globar para que el return sepa cuanto debe regresar el stack pointer
                    cgen(tree.child[2]) #generar el código de dentro de la función
                    file.write("\t\tlw $ra, -4($fp)\n") #cargar la dirección de regreso que guardamos antes
                    file.write("\t\tlw $fp, -8($fp)\n") #cargar el old fp que guardamos desde la llamada
                    z = numLocDec*-4 - 8 #cantidad que debe regresar el stack pointer
                    file.write("\t\taddiu $sp, $sp, "+str(z)+"\n") #mover sp
                    file.write("\t\tjr $ra\n\n") #regresar a donde se llamó la función
            elif(tree.decType == DecTipo.VARIABLE): #si es la declaración de una varibale
                shouldCheckChilds = False #no checar hijos
            elif(tree.decType == DecTipo.ARREGLO):#si es la declaración de un arreglo
                shouldCheckChilds = False #no checar hijos
        elif(tree.nType == TipoNodo.EXP): #si es una expresion
            if(tree.expType == ExpTipo.IDENTIFIER): #si es un identificador
                idLocation, idScope = getLocation(tree.str, tree.lineno) #Obtener la dirección donde está la variable
                if idScope == 0: #si es global
                    file.write("\t\tlw $a0, "+str(idLocation)+"($t7)\n") #Cargarla al acumulador
                else:
                    file.write("\t\tlw $a0, "+str(idLocation)+"($fp)\n") #Cargarla al acumulador
            elif(tree.expType == ExpTipo.ARREGLO): #si es un arreglo
                arrLocation,_ = getLocation(tree.child[0].str, tree.lineno) #Obtener la dirección donde está la variable
                aux_tree = tree.child[1] #para mayor legibilidad
                if(aux_tree.expType == ExpTipo.CONST): #si dentro de los corchetes hay una constante
                    pos = int(aux_tree.val) * 4 #representa el numero específico de espacios dentro del arreglo
                    file.write("\t\tlw $a0, "+str(arrLocation+pos)+"($t7)\n") #cargar al acumulador
                else:
                    cgen(tree.child[1]) #hacer la llamada de lo que esté dentro de los corchetes
                    file.write("\t\tmul $a0, $a0, 4\n") #multiplicar el resultado por 4
                    file.write("\t\tadd $t7, $t7, $a0\n") #sumarlo a la posición del arreglo
                    file.write("\t\tmove$t0 $a0\n") #mover el resultado a un temporal
                    file.write("\t\tlw $a0, "+str(arrLocation)+"($t7)\n") #cargar la posición del arreglo al acumulador
                    file.write("\t\tsub $t7, $t7, $t0\n") #regresar el apuntador al inicio del arreglo
                shouldCheckChilds = False #no checar hijos
            elif (tree.expType == ExpTipo.OPERATION): #si es operación
                cgen(tree.child[0])#generar código del hijo izquierdo
                file.write("\t\tsw $a0 0($sp)\n") #guardarlo en el sp
                file.write("\t\taddiu $sp $sp 4\n") #mover el sp
                cgen(tree.child[1]) #generar código del hijo derecho
                file.write("\t\tlw $t1 -4($sp)\n") #guardarlo en el temporarl
                if(tree.op == TokenType.PLUS): #hacer la operación que corresponda
                    file.write("\t\tadd $a0 $t1 $a0\n")
                elif(tree.op == TokenType.LESS):
                    file.write("\t\tsubu $a0 $t1 $a0\n")
                elif(tree.op == TokenType.MULT):
                    file.write("\t\tmul $a0 $t1 $a0\n")
                elif(tree.op == TokenType.DIV):
                    file.write("\t\tdiv $a0 $t1 $a0\n")
                file.write("\t\taddiu $sp $sp -4\n") #regresar el sp a su posición
                shouldCheckChilds = False #no checar hijos
            elif(tree.expType == ExpTipo.ASSIGN): #si es una asignación
                cgen(tree.child[1]) #hacer el código de lo que esté a la derecha del signo
                if(tree.child[0].expType == ExpTipo.ARREGLO): #si es un arreglo lo de la izquierda
                    aux_tree = tree.child[0].child[0] #variable para ayudar a la lectura
                    arrLocation,_ = getLocation(aux_tree.str,tree.lineno) #obtener la ubicación en memoria del arreglo
                    aux_tree = tree.child[0].child[1] #variable para ayudar a la lectura
                    #repetir el códgio de arreglo con la direfencia que este código es de guardado y no de carga
                    if(aux_tree.expType == ExpTipo.CONST): #si es constante
                        pos = int(aux_tree.val) * 4
                        file.write("\t\tsw $a0, "+str(arrLocation+pos)+"($t7)\n") #guardar en la posición indicada
                    else: #si es cualquier otra cosa
                        file.write("\t\tmove $t1, $a0\n") #guardar en temporal lo que se quiere almacenar
                        cgen(tree.child[0].child[1]) #generar el código que esté dentro de los corchetes
                        file.write("\t\tmul $a0, $a0, 4\n")
                        file.write("\t\tadd $t7, $t7, $a0\n")
                        file.write("\t\tsw $t1, "+str(arrLocation)+"($t7)\n") #guardar en la posición indicada
                        file.write("\t\tsub $t7, $t7, $a0\n")
                else: #si no es arreglo es variable
                    arrLocation, arrScope = getLocation(tree.child[0].str,tree.child[0].lineno)
                    if arrScope == 0: #si es global usar t7
                        file.write("\t\tsw $a0, "+str(arrLocation)+"($t7)\n")
                    else: #sino usar el fp
                        file.write("\t\tsw $a0, "+str(arrLocation)+"($fp)\n")
                shouldCheckChilds = False
            elif(tree.expType == ExpTipo.CONST): #si es una constante
                file.write("\t\tli $a0 "+str(tree.val)+"\n") #cargar al acumulador la constante
        elif(tree.nType == TipoNodo.STMT): #si es un statement
            if(tree.stmtType == StmtTipo.IF): #si es un if
                file.write("#empieza el if\n")
                cgen(tree.child[0].child[0]) #generar el código de la izquierda de la operación dentro del if
                file.write("\t\tsw $a0 0($sp)\n") #guardar en el sp
                file.write("\t\taddiu $sp $sp 4\n") #mover el sp
                cgen(tree.child[0].child[1]) #generar el código de la derecha de la operación dentro del if
                file.write("\t\tlw $t1 -4($sp)\n") #cargar lo del sp al t1
                file.write("\t\taddiu $sp $sp -4\n") #mover sp
                ifCounter += 1 #aumentar variable global de ifs
                localIfCounter = ifCounter #guardar en la local
                if(tree.child[0].op == TokenType.EQUAL): #generar código correspondiente a la operación que venga
                    file.write("\t\tbeq $a0 $t1 true_branch_if_"+str(localIfCounter)+"\n")
                elif(tree.child[0].op == TokenType.DIFF):
                    file.write("\t\tbne $a0 $t1 true_branch_if_"+str(localIfCounter)+"\n")
                elif(tree.child[0].op == TokenType.GREATERT):
                    file.write("\t\tbgt $t1 $a0 true_branch_if_"+str(localIfCounter)+"\n")
                elif(tree.child[0].op == TokenType.GTEQUAL):
                    file.write("\t\tbge $t1 $a0 true_branch_if_"+str(localIfCounter)+"\n")
                elif(tree.child[0].op == TokenType.LOWERTHAN):
                    file.write("\t\tblt $t1 $a0 true_branch_if_"+str(localIfCounter)+"\n")
                elif(tree.child[0].op == TokenType.LTEQUAL):
                    file.write("\t\tble $t1 $a0 true_branch_if_"+str(localIfCounter)+"\n")
                file.write("false_branch_if_"+str(localIfCounter)+":\n") #etiqueta en caso de no cumplirse la condición
                cgen(tree.child[2]) #generar código del else en caso de existir
                file.write("\t\tb end_if_"+str(localIfCounter)+"\n") # saltar al final cuando este termine
                file.write("true_branch_if_"+str(localIfCounter)+":\n") #etiqueta en caso de ser veradera la condición
                cgen(tree.child[1]) #generar código de la parte verdadera del if
                file.write("end_if_"+str(localIfCounter)+":\n") #etiqueta del fin del if
                shouldCheckChilds = False #no checar a los hijos
                pass
            elif(tree.stmtType == StmtTipo.WHILE): #si es un while
                #El código del while es muy parecido al código del if
                whileCounter+=1 #sumar al contador global
                localWhileCounter = whileCounter #guardar para el uso local
                file.write("#empieza el if\n")
                file.write("start_while_"+str(localWhileCounter)+":\n") #etiqueta de inicio
                cgen(tree.child[0].child[0]) #generar el código de la izquierda de la operación dentro del while
                file.write("\t\tsw $a0 0($sp)\n") #guardar en el sp
                file.write("\t\taddiu $sp $sp 4\n") #mover sp
                cgen(tree.child[0].child[1]) #generar el código de la derecha de la operación dentro del while
                file.write("\t\tlw $t1 -4($sp)\n") 
                file.write("\t\taddiu $sp $sp -4\n")
                if(tree.child[0].op == TokenType.EQUAL): #código correspondiente a la operación
                    file.write("\t\tbeq $a0 $t1 true_branch_while_"+str(localWhileCounter)+"\n")
                elif(tree.child[0].op == TokenType.DIFF):
                    file.write("\t\tbne $a0 $t1 true_branch_while_"+str(localWhileCounter)+"\n")
                elif(tree.child[0].op == TokenType.GREATERT):
                    file.write("\t\tbgt $t1 $a0 true_branch_while_"+str(localWhileCounter)+"\n")
                elif(tree.child[0].op == TokenType.GTEQUAL):
                    file.write("\t\tbge $t1 $a0 true_branch_while_"+str(localWhileCounter)+"\n")
                elif(tree.child[0].op == TokenType.LOWERTHAN):
                    file.write("\t\tblt $t1 $a0 true_branch_while_"+str(localWhileCounter)+"\n")
                elif(tree.child[0].op == TokenType.LTEQUAL):
                    file.write("\t\tble $t1 $a0 true_branch_while_"+str(localWhileCounter)+"\n")
                file.write("\t\tb end_while_"+str(localWhileCounter)+"\n") #si no se cumple la condición saltar al final
                file.write("true_branch_while_"+str(localWhileCounter)+":\n") #etiqueta en caso de que cumpla
                cgen(tree.child[1]) #generar código dentro del while
                file.write("\t\tb start_while_"+str(localWhileCounter)+"\n") #salto al incio
                file.write("end_while_"+str(localWhileCounter)+":\n") #etiqueta de fin del while
                shouldCheckChilds = False #checar hijos
            elif(tree.stmtType == StmtTipo.CALL): #si es una llamada
                if(tree.child[0].str == "output"): #código para imprimir variables enteras en consola
                    cgen(tree.child[1]) #generar código para lo que se quiera imprimir
                    file.write("\t\tli $v0 1\n")
                    file.write("\t\tsyscall\n")
                elif(tree.child[0].str == "input"): #código para recibir variables desde la consola
                    file.write("\t\tli $v0 5\n")
                    file.write("\t\tsyscall\n")
                    file.write("\t\tmove $a0 $v0\n") #mover el valor recibido al acumulador
                else: #si es cualquier otra llamada
                    numParams, localDec = getFuncInfo(tree.child[0].str) #obtener información de la función
                    file.write("\t\tsw $fp, 0($sp)\n") #guardar el fp donde está el sp actualmente antes de los parametros
                    file.write("\t\taddiu $sp, $sp, 8\n") #mover dos para después guardar la ra en ese espacio libre
                    aux_tree = tree.child[1] #variable ayudante con los parámetros
                    for i in range(numParams): #por cada parametro esperado
                        cgen(aux_tree, False) #generar el código de ese parámetro
                        file.write("\t\tsw $a0 0($sp)\n") #guardar en el sp
                        file.write("\t\taddiu $sp, $sp, 4\n") #mover #sp
                        aux_tree = aux_tree.sibling #siguiente parámetro
                        if(aux_tree == None): #terminar en caso de acabar con los parámtros
                            break
                    file.write("\t\tjal "+tree.child[0].str+"\n") #saltar a la función deseada
                shouldCheckChilds = False #no checar a los hijos
            elif(tree.stmtType == StmtTipo.RETURN): #si es un return
                shouldCheckChilds =False #no checar a los hijos
                for child in tree.child: #por cada hijo que tenga el return
                    cgen(child)
                #es el mismo código de salida de la declaración de funciones
                file.write("\t\tlw $ra, -4($fp)\n") #cargar la dirección de regreso
                file.write("\t\tlw $fp, -8($fp)\n") #cargar el anterior fp
                z = numeroLocales*-4 - 8 #cantidad que se debe regresar el sp
                file.write("\t\taddiu $sp, $sp, "+str(z)+"\n") #regresar sp
                file.write("\t\tjr $ra\n\n") # regresar a donde sea necesario
        if shouldCheckChilds: #si se deben checar los hijos
            for child in tree.child:
                cgen(child)
        if checkSiblings:
            cgen(tree.sibling)

#función que inicia el proceso de generación de código
def codeGen(tree, arch):
    global file
    file = open(arch, "w") #abrir o generar el archivo a escribir
    cgen(tree) #llamada a la función que genera el código
    file.close() #cerrar el archivo