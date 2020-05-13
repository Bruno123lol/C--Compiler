from globalTypes import *
from Parser import *

stack = [0]
location = 0
scope = 0
SymTableDictionary = {0:{'outputParam':[2,'int',False,'void',-1,0],'input':[0,'int',False,0,0,0],'output':[1,'void',False,1,0,0]}}


def st_insert(name, tipo, isArray, arrSize, lineno, scope, funcScope=-1):
    global location
    if name in SymTableDictionary[scope]:
        if SymTableDictionary[scope][name][-1] != lineno:
            SymTableDictionary[scope][name].append(lineno)
    else:
        location += 1
        SymTableDictionary[scope][name] = [location,tipo,isArray,arrSize, funcScope,lineno]

def st_lookup(name):
    for x in range(1,len(stack)+1):
        if name in SymTableDictionary[stack[(-x)]]:
            return stack[-x]
    return stack[-1]   

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
                    if tree.child[1] != None:
                        st_insert(tree.child[0].str,tree.str,True,tree.child[1].val,tree.lineno,scope)
                    else:
                        st_insert(tree.child[0].str,tree.str,True,"void",tree.lineno,scope)
                elif tree.str ==  'void':
                    print("Error no se pueden declarar arreglos de tipo void ",tree.lineno)
                shouldCheck = False

            elif(tree.decType == DecTipo.FUNCION):
                if(stack[-1]!=0):
                    stack.pop()

                aux_tree = tree.child[1]
                numberOfParams = 0
                while(aux_tree != None and aux_tree.stmtType != StmtTipo.COMPOUND):
                    numberOfParams += 1
                    aux_tree = aux_tree.sibling
                
                st_insert(tree.child[0].str,tree.str,False,numberOfParams,tree.lineno,stack[0],scope+1)

                scope+=1
                scopesCreated += 1
                stack.append(scope)
                SymTableDictionary[scope] = {}
            
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
                stack.append(scope)
                SymTableDictionary[scope] = {}
        if shouldCheck:
            for child in tree.child:
                table(child)
        
        tree = tree.sibling
    for x in range(scopesCreated):
        if(stack[-1]!=0):
            stack.pop()

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
                if tree.child[1].type != OpTipo.INTEGER:
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

                        if SymTableDictionary[funcScope][name][2] == True:
                            if not buscarScope(aux_tree.str,aux_tree.lineno):
                                print("Se esperaba un arreglo como parametro",aux_tree.lineno)
                        elif buscarScope(aux_tree.str,aux_tree.lineno):
                            print("Se esperaba una variable de tipo int como parametro",aux_tree.lineno)
                        elif aux_tree.type != OpTipo.INTEGER:
                            print("Se esperaba una variable de tipo int como parametro",aux_tree.lineno)
                        actualParam+=1
                        
                       
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

def printSymTab():
    title = "Scope number   Variable Name  Location Type   Is Array   Array Size  Function Scope Line Numbers"
    lines = "-".center(len(title),"-")
    for scope in SymTableDictionary:
        print(title)
        print(lines)
        for name in SymTableDictionary[scope]:
            print(str(scope).center(15), end ='')
            print(name.center(12), end ="")
            for i in range(len(SymTableDictionary[scope][name])):
                if(i < 5):
                    print(str(SymTableDictionary[scope][name][i]).center(12), end="")
                else:
                    print(str(SymTableDictionary[scope][name][i]).center(3), end="")
            print(end="\n\n")
    print(end="\n")


def semantica(tree, imprime = True):
    table(tree,imprime)
    if(imprime):
        printSymTab()
    checkNode(tree)
    pass