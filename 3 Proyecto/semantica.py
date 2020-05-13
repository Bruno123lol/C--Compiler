from globalTypes import *
from Parser import *

location = 0

# the stack for hash tables
stack = [0]

# the hash table

SymTableDictionary = {0:{'outputParam':[2,'int',False,'void',-1,0],'input':[0,'int',False,0,0,0],'output':[1,'void',False,1,0,0]}}

# Procedure st_insert inserts line numbers and
# memory locations into the symbol table
# loc = memory location is inserted only the
# first time, otherwise ignored
location = 0
def st_insert(name, tipo, arrType, arrSize, lineno, scope, funcScope=-1):
    global location
    if name in SymTableDictionary[scope]:
        if SymTableDictionary[scope][name][-1] != lineno:
            SymTableDictionary[scope][name].append(lineno)
    else:
        location += 1
        SymTableDictionary[scope][name] = [location,tipo,arrType,arrSize, funcScope,lineno]
    # print("Scope: ",scope)
    # print(SymTableDictionary[scope])


# Function st_lookup returns the memory 
# location of a variable or -1 if not found
def st_lookup(name):
    for x in range(1,len(stack)+1):
        if name in SymTableDictionary[stack[(-x)]]:
            return stack[-x]
    return stack[-1]   

scope = 0

def table(tree, imprime = True):
    global scope
    scopesCreated = 0
    while tree != None:
        shouldCheck = True
        if(tree.nType == TipoNodo.DEC):
            if(tree.decType == DecTipo.VARIABLE):
                if tree.str == 'int':
                    st_insert( tree.child[0].str,tree.str,False,-1,tree.lineno,scope)
                elif tree.str ==  'void':
                    print("Error no se pueden declarar variables de tipo void ",tree.lineno)
                shouldCheck = False
            elif(tree.decType == DecTipo.ARREGLO):
                if tree.str == 'int':
                    st_insert( tree.child[0].str,tree.str,False,-1,tree.lineno,scope)
                    if tree.child[1] != None:
                        st_insert(tree.child[0].str,tree.str,True,tree.child[1].val,tree.lineno,scope)
                    else:
                        st_insert(tree.child[0].str,tree.str,True,"void",tree.lineno,scope)
                elif tree.str ==  'void':
                    print("Error no se pueden declarar arreglos de tipo void ",tree.lineno)
                shouldCheck = False

            elif(tree.decType == DecTipo.FUNCION):
                if(stack[-1]!=0):
                    # print("Scope number: ", stack[-1], " popped out")
                    stack.pop()

                aux_tree = tree.child[1]
                numberOfParams = 0
                while(aux_tree != None and aux_tree.stmtType != StmtTipo.COMPOUND):
                    numberOfParams += 1
                    aux_tree = aux_tree.sibling
                
                st_insert(tree.child[0].str,tree.str,False,numberOfParams,tree.lineno,stack[0],scope+1)

                scope+=1
                scopesCreated += 1
                # print("Scope number: ", scope, " created")
                # print("Number of scopes created in this scope: ", scopesCreated)
                stack.append(scope)
                SymTableDictionary[scope] = {}
                # print("Es de funcion")
            
        elif(tree.nType == TipoNodo.EXP):
            if(tree.expType == ExpTipo.IDENTIFIER):
                st_insert(tree.str,"",False,-1,tree.lineno,st_lookup(tree.str))
                if SymTableDictionary[st_lookup(tree.str)][tree.str][1] == "":
                    print("Variable not defined in line: ",tree.lineno)
            if(tree.expType == ExpTipo.ARREGLO):
                st_insert(tree.child[0].str,"",True,-1,tree.lineno,st_lookup(tree.child[0].str))
                shouldCheck = False
        elif(tree.nType == TipoNodo.STMT):
            if(tree.stmtType == StmtTipo.IF or tree.stmtType == StmtTipo.WHILE):
                scope+=1
                scopesCreated += 1
                # print("Scope number: ", scope, " created")
                # print("Number of scopes created in this scope: ", scopesCreated)
                stack.append(scope)
                SymTableDictionary[scope] = {}
                # print("Es de stmt")
        if shouldCheck:
            for child in tree.child:
                table(child)
        
        tree = tree.sibling
    for x in range(scopesCreated):
        # print("Scope number: ", stack[-1], " popped out")
        if(stack[-1]!=0):
            stack.pop()

def printSymTab():
    print("Variable Name  Location    Line Numbers")
    print("-------------  --------    ------------")
    for scope in SymTableDictionary:
        print("Scope number: ",scope)
        for name in SymTableDictionary[scope]:
            print("name :",name)
            for i in range(len(SymTableDictionary[scope][name])):
                print("info in symtable: ",SymTableDictionary[scope][name][i])

# def buscarScope(name, lineno):
# 	found = [] 
# 	for scope in SymTableDictionary:
# 		if name in SymTableDictionary[scope]:
# 			found.append(scope) 
# 	for i in found:
#         for j in range(5,len(SymTableDictionary[i][name])):
#             if lineno == SymTableDictionary[i][name][j]:
#                 if SymTableDictionary[i][name][2]:
#                     return True
# 	return False

def buscarScope(name, lineno):
    found = []
    for scope in SymTableDictionary:
        if name in SymTableDictionary[scope]:
            found.append(scope)
        pass
    pass
    for i in found:
        for j in range(5,len(SymTableDictionary[i][name])):
            if lineno == SymTableDictionary[i][name][j]:
                return SymTableDictionary[i][name][2]
            pass
        pass
    return False


def checkNode(tree):
    if tree != None:
        for child in tree.child:
            checkNode(child)
        checkNode(tree.sibling)
        if tree.nType == TipoNodo.EXP:
            if tree.expType == ExpTipo.OPERATION or tree.expType == ExpTipo.ASSIGN:
                if ((tree.child[0].type not in [OpTipo.INTEGER, OpTipo.ARRAY]) or (tree.child[1].type not in [OpTipo.INTEGER, OpTipo.ARRAY])):
                    print("Op applied to non-integer ",tree.lineno, " str: ", tree.str)
                if (tree.op in booleanOperators):
                    tree.type = OpTipo.BOOLEAN
                else:
                    tree.type = OpTipo.INTEGER
            elif tree.expType in [ExpTipo.IDENTIFIER, ExpTipo.CONST]:
                tree.type = OpTipo.INTEGER
            elif tree.expType == ExpTipo.ARREGLO:
                if tree.sibling.type != OpTipo.INTEGER:
                    print("Esto es void!!! u otra cosa xd", tree.lineno)
                else:
                    tree.type = OpTipo.ARRAY
        if tree.nType == TipoNodo.STMT:
            if tree.stmtType == StmtTipo.IF or tree.stmtType == StmtTipo.WHILE:
                if(tree.child[0].type != OpTipo.BOOLEAN):
                    print("Boolean expresion expected ",tree.lineno)
            elif tree.stmtType == StmtTipo.CALL:
                funcScope = SymTableDictionary[0][tree.child[0].str][4]
                paramNum = SymTableDictionary[0][tree.child[0].str][3]
                actualParam = 0
                aux_tree = tree.child[1]
                if(aux_tree != None and paramNum>0):
                    for name in SymTableDictionary[funcScope]:
                        bandera = False
                        if aux_tree.type == OpTipo.ARRAY and aux_tree.child[0] != None:
                            aux_tree.type = OpTipo.INTEGER
                            bandera = True
                        if SymTableDictionary[funcScope][name][2] == True:
                            if not buscarScope(aux_tree.str,aux_tree.lineno):
                                print("Se esperaba un arreglo como parametro",aux_tree.lineno)
                        elif buscarScope(aux_tree.str,aux_tree.lineno):
                            print("Se esperaba una variable de tipo int como parametro",aux_tree.lineno)
                        elif aux_tree.type != OpTipo.INTEGER:
                            print("Se esperaba una variable de tipo int como parametro",aux_tree.lineno)
                        actualParam+=1
                        
                        if bandera:
                            aux_tree = aux_tree.sibling.sibling
                        else: 
                            aux_tree = aux_tree.sibling
                        
                        if aux_tree==None or actualParam == paramNum:
                            break
                    if actualParam < paramNum or aux_tree != None:
                        print("Error, el numero de parametros no coincide", tree.lineno)
                elif aux_tree == None and paramNum>0:
                    print("Se esperaba un parametro",tree.lineno)
                elif aux_tree != None and paramNum<=0:
                    print("No se esperaba un parametro",aux_tree.lineno)
                
                if SymTableDictionary[0][tree.child[0].str][1] == "int":
                    tree.type = OpTipo.INTEGER
                    tree.child[0].type = OpTipo.INTEGER
                else:
                    tree.type = OpTipo.VOID
                    tree.child[0].type = OpTipo.VOID
            elif tree.stmtType == StmtTipo.RETURN:
                if tree.child[0] != None:
                    if tree.child[0].type != OpTipo.INTEGER:
                        print("Return no regresa una variable de tipo entero")
        #checkNode(tree.sibling)

def semantica(tree, imprime = True):
    table(tree,imprime)
    if(imprime):
        printSymTab()
    checkNode(tree)
    pass