from globalTypes import *
from Parser import *

#Lista utilizada para mantener el control sobre el scope que se está usando actualmente y su padre
stack = [0]
#variable utilizada para insertar en la tabla la ubicación en memoria del identificador
location = 0
#Variable global para mantener el número del scope de las tablas de símbolos
scope = 0
#Diccionario de diccionarios para almacenar y controlar las tablas de símbolos 
SymTableDictionary = {0:{'outputParam':[2,'int',False,'void',-1,0],'input':[0,'int',False,0,0,0],'output':[1,'void',False,1,0,0]}}

#Función para instertar los valores en la tabla correspondiente al scope actual
#recibe como parametros todos los valores a insertar en la tabla y el scope donde se debe insertar
def st_insert(name, tipo, isArray, arrSize, lineno, scope, funcScope=-1):
    global location 
    if name in SymTableDictionary[scope]: #en caso de que ya se encuentre en la ST solo agregar la linea de uso
        if SymTableDictionary[scope][name][-1] != lineno:
            SymTableDictionary[scope][name].append(lineno)
    else:
        location += 1 #Aumentar la posición de memeoria en la que se va a encontrar el identificador
        SymTableDictionary[scope][name] = [location,tipo,isArray,arrSize, funcScope,lineno]

#función para buscar el identificador en las tablas de simbolos que se encuentren en el stack
# recibe como parámetro el identificador a buscar y devuelve el stack donde se encontró
def st_lookup(name):
    for x in range(1,len(stack)+1):
        if name in SymTableDictionary[stack[(-x)]]:
            return stack[-x]
    return stack[-1]   

#función para buscar si un identificador ya fue declarado, recibe como parámetro el identificador a encontrar y el scope donde buscar
#Devueve verdadero cuando lo encuentra, devuelve falso en caso contrario
def st_dec_lookup(name, scopeB):
    if name in SymTableDictionary[scopeB]:
        return True
    return False

#Función para recorrer el AST e insertar los identificadores en las ST correspondiente en el momento que se deba hacer
def table(tree, imprime = True):
    global scope
    numScopesCreated = 0 #contador para saber cuantos scopes fueron creados en esta rama del AST
    
    while tree != None:
        shouldCheckChilds = True #variable para saber cuando se requieren checar los hijos de la rama
       
        if(tree.nType == TipoNodo.DEC): #si el nodo actual es una declaración
           
            if(tree.decType == DecTipo.VARIABLE): #si es una declaración de variable
                
                if st_dec_lookup(tree.child[0].str, scope): #si ya fue declarada anteriormente en el mismo scope
                    errorFunction(tree.lineno,"Error, está tratando de declarar una variable dos o más veces",tree.child[0].str)
                
                else:
                   
                    if tree.str == 'int': #si la variable es de tipo int
                        st_insert( tree.child[0].str,tree.str,False,-1,tree.lineno,scope)
                   
                    elif tree.str ==  'void': #si la variable se intenta asignar a un tipo void
                        errorFunction(tree.lineno,"Error, está tratando de declarar variables de tipo void ",tree.child[0].str)
                shouldCheckChilds = False
            
            elif(tree.decType == DecTipo.ARREGLO): #si es la declaración de un arreglo
            
                if st_dec_lookup(tree.child[0].str, scope): #si ya fue declarada en el mismo scope acutal
                    errorFunction(tree.lineno,"Error, está tratando de declarar un arreglo dos o más veces",tree.child[0].str)
                
                else:  
                    if tree.str == 'int': #si el arreglo es de tipo int
                    
                        if tree.child[1] != None: #si no es la declaración de un parámtero
                            st_insert(tree.child[0].str,tree.str,True,tree.child[1].val,tree.lineno,scope)
                   
                        else: # si el arreglo es un parámetro
                            st_insert(tree.child[0].str,tree.str,True,"void",tree.lineno,scope)
                   
                    elif tree.str ==  'void': # si se intenta declarar un arreglo de tipo void
                        errorFunction(tree.linno,"Error no se pueden declarar arreglos de tipo void ",tree.child[0].str)
                shouldCheckChilds = False

            elif(tree.decType == DecTipo.FUNCION): #si es la declaración de una función
                
                if(stack[-1]!=0): #sacar del stack los demás scopes porque solo se pueden declarar funciones en el scope global
                    stack.pop()
                
                if st_dec_lookup(tree.child[0].str, 0): #si ya fue declarada anteriormente en el mismo scope
                    errorFunction(tree.lineno,"Error, está tratando de declarar una función dos o más veces",tree.child[0].str)

                aux_tree = tree.child[1]
                numberOfParams = 0
                while(aux_tree != None and aux_tree.stmtType != StmtTipo.COMPOUND): #contar el número de parámetros de la función 
                    numberOfParams += 1
                    aux_tree = aux_tree.sibling
                
                st_insert(tree.child[0].str,tree.str,False,numberOfParams,tree.lineno,stack[0],scope+1)

                scope+=1 #aumentar el número de scopes
                numScopesCreated += 1  #avisar que se está creando un scope
                stack.append(scope) #agregar el scope al stack
                SymTableDictionary[scope] = {} #añadir el scope al diccionario
            
        elif(tree.nType == TipoNodo.EXP): #si es una expresion

            if(tree.expType == ExpTipo.IDENTIFIER): #si es un identificador
                st_insert(tree.str,"",False,-1,tree.lineno,st_lookup(tree.str))
                if SymTableDictionary[st_lookup(tree.str)][tree.str][1] == "": #si no tiene tipo
                    errorFunction(tree.lineno,"Error, está tratando de usar una variable no definida ",tree.str)
            
            if(tree.expType == ExpTipo.ARREGLO): #si es un arreglo
                st_insert(tree.child[0].str,"",True,-1,tree.lineno,st_lookup(tree.child[0].str))
                table(tree.child[1]) #checar solo el segundo hijo
                shouldCheckChilds = False
        
        elif(tree.nType == TipoNodo.STMT): #si es un statement
        
            if(tree.stmtType == StmtTipo.IF or tree.stmtType == StmtTipo.WHILE): #si es un if o un while
                scope+=1 #aumentar el número de scopes
                numScopesCreated += 1 #avisar que se está creando un scope
                stack.append(scope) #agregar el scope al stack
                SymTableDictionary[scope] = {} #añadir el scope al diccionario
        
        if shouldCheckChilds: #si se deben checar los hijos
            for child in tree.child:
                table(child)
        
        tree = tree.sibling
    
    for x in range(numScopesCreated): #sacar cada scope creado
        if(stack[-1]!=0):
            stack.pop()

#Función que ayuda encontrar la definición de una variable en la ST y devuelve TRue si esta es un arreglo y False en caso contrario
#name es el identificador a buscar y lineno es el número de línea donde se encuentra
def isArray(name, lineno):
    found = [] #arreglo de scopes dónde aparece la variable
    for scope in SymTableDictionary: 
        if name in SymTableDictionary[scope]:
            found.append(scope) #adjuntar el scope

    for i in found: #por cada scope buscar si es el scope correspondiente a la variable que se busca
        for j in range(5,len(SymTableDictionary[i][name])):
            if lineno == SymTableDictionary[i][name][j]:
                return SymTableDictionary[i][name][2] #devolver el valor del atributo isArray
            
    return False

#Función que recorre el árbol en postorden para identificar los errores en los tipos de variables usados
def checkNode(tree):
    if tree != None: 
        for child in tree.child: #hacer la llamada de todos los hijos
            checkNode(child)
        checkNode(tree.sibling) #hacer la llamada de todos los hermanos

        if tree.nType == TipoNodo.EXP: #si es una expresión
            
            if tree.expType == ExpTipo.OPERATION or tree.expType == ExpTipo.ASSIGN: #si es operación o asignación
                #si el hijo no es arreglo o entero
                if ((tree.child[0].type not in [OpTipo.INTEGER, OpTipo.ARRAY]) or (tree.child[1].type not in [OpTipo.INTEGER, OpTipo.ARRAY])):
                    errorFunction(tree.lineno,"Error, está tratando de hacer una operación con valores no enteros ",tree.str)
                #si es una operador booleano
                if (tree.op in booleanOperators):
                    tree.type = OpTipo.BOOLEAN
                #si no, es entero
                else:
                    tree.type = OpTipo.INTEGER
            #Si es identificador o constante
            elif tree.expType in [ExpTipo.IDENTIFIER, ExpTipo.CONST]:
                tree.type = OpTipo.INTEGER
            #si es arreglo
            elif tree.expType == ExpTipo.ARREGLO:
                #si el valor dentro del arreglo es entero
                if tree.child[1].type != OpTipo.INTEGER:
                    errorFunction(tree.lineno,"Error, está tratando de usar algún tipo de valor no entero ",tree.str)
                tree.type = OpTipo.ARRAY
        
        if tree.nType == TipoNodo.STMT: #si es un statement
        
            if tree.stmtType == StmtTipo.IF or tree.stmtType == StmtTipo.WHILE: #si es un if o un while
        
                if(tree.child[0].type != OpTipo.BOOLEAN): #si el hijo o el resultado no es booleano
                    errorFunction(tree.lineno,"Error, está tratando de usar algún tipo de valor no booleano ",tree.str)
        
            elif tree.stmtType == StmtTipo.CALL: #si es una llamada
                funcScope = SymTableDictionary[0][tree.child[0].str][4] #scope de la funcion
                paramNum = SymTableDictionary[0][tree.child[0].str][3] #número de parámetros
                actualParam = 0 #contador de los parámetros recorridos
                aux_tree = tree.child[1] #auxiliar del árbol
        
                if(aux_tree != None and paramNum>0): #si no es null la lista de parámetros y si se esperaa algún parámetro
        
                    for name in SymTableDictionary[funcScope]: #por cada parámetro dentro del scope de la función
        
                        if aux_tree.type == OpTipo.ARRAY and aux_tree.child[0] != None: #si es arreglo y no está vacío el hijo hacer entero
                            aux_tree.type = OpTipo.INTEGER

                        if SymTableDictionary[funcScope][name][2] == True: #si se espera que el parametro sea un arreglo
        
                            if not isArray(aux_tree.str,aux_tree.lineno): #si no es arreglo la variable que se manda
                                errorFunction(aux_tree.lineno,"Error, se esperaba un arreglo como parámetro",aux_tree.str)
        
                        elif isArray(aux_tree.str,aux_tree.lineno): #si es arreglo la variable que se manda
                            errorFunction(aux_tree.lineno,"Error, se esperaba una variable entera como parámetro",aux_tree.str)
        
                        elif aux_tree.type != OpTipo.INTEGER: #si no es entera la variable
                            errorFunction(tree.lineno,"Error, se esperaba una variable entera parámetro",tree.str)
        
                        actualParam+=1 #aumentar el contador de parámetros
                       
                        aux_tree = aux_tree.sibling #pasar al siguiente hermano

                        if aux_tree==None or actualParam == paramNum: #si ya se acabó lo que se manda en la llamada o si ya no se esperan más parámetros
                            break
                    
                    if actualParam < paramNum or aux_tree != None: #si es menor el número de parámetros que se envían o si había más parámetros
                        errorFunction(tree.lineno,"Error, el número de parámetros no coincide",tree.str)
                
                elif aux_tree == None and paramNum>0: #si no se envían parámetros y se esperaban más de 0
                    errorFunction(tree.lineno,"Error, se esperaba uno o más parámetros",tree.str)
                
                elif aux_tree != None and paramNum<=0: #si se envían parámetros y no se esperaba ningúno
                    errorFunction(tree.lineno,"Error, no se esperaba un parámetro",tree.str)
                
                if SymTableDictionary[0][tree.child[0].str][1] == "int": #si la función es de tipo int
                    tree.type = OpTipo.INTEGER
                    tree.child[0].type = OpTipo.INTEGER
                
                else: #si la función es de tipo void
                    tree.type = OpTipo.VOID
                    tree.child[0].type = OpTipo.VOID
            
            elif tree.stmtType == StmtTipo.RETURN: #si es un return
            
                if tree.child[0] != None: #si está regresando algo
            
                    if tree.child[0].type != OpTipo.INTEGER: #si el valor que devuelve no es entero
                        errorFunction(tree.lineno,"Error, está tratando de regresar algún tipo de valor no entero ",tree.str)

#Función para imprimir el diccionario de ST's
def printSymTab():
    center = 15
    title = "Scope number".center(center)+"Variable Name".center(center)+"Location".center(center)+"Type".center(center)
    title += "Is Array".center(center)+"Array Size".center(center)+"Function Scope".center(center+2)+"Line Numbers"
    lines = "-".center(len(title),"-")
    for scope in SymTableDictionary:
        
        if SymTableDictionary[scope] == {}:
            print("El scope: ", scope," está vacio porque no tiene declaraciones dentro")
        
        else:
            tabltaTitle = "Tabla del scope: "+str(scope)
            print("\n"+tabltaTitle.center(len(title)), end = '\n\n')
            print(title)
            print(lines)

            for name in SymTableDictionary[scope]:
                print(str(scope).center(center), end ='')
                print(name.center(center), end ="")

                for i in range(len(SymTableDictionary[scope][name])):

                    if(i < 5):
                        print(str(SymTableDictionary[scope][name][i]).center(center), end="")
                    else:
                        print(str(SymTableDictionary[scope][name][i]).center(3), end="")

                print(end="\n\n")

        print(end="\n")

#función que inicia el programa
def semantica(tree, imprime = True):
    table(tree,imprime)
    if(imprime):
        printSymTab()
    checkNode(tree)
    pass