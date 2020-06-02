from globalTypes import * 
from semantica import *
import sys

f= ""

ifCounter = 0

whileCounter = 0

numeroLocales = 0

def cgen(tree, checkSiblings = True):
    global ifCounter, whileCounter, numeroLocales
    if tree != None:
        shouldCheckSiblings = checkSiblings
        shouldCheckChilds = True #variable para saber cuando se requieren checar los hijos de la rama
        if(tree.nType == TipoNodo.DEC):
            if(tree.decType == DecTipo.FUNCION):
                shouldCheckChilds = False
                if(tree.child[0].str == "main"):
                    f.write("\t\t.data\n")
                    f.write("\t\tglobalVars: .word 2\n")
                    numParams, numLocDec = getFuncInfo(tree.child[0].str)
                    f.write("\t\t.text\n")
                    f.write("\t\t.globl main\n")
                    f.write("main:")
                    f.write("\tla $t7, globalVars\n")
                    f.write("\t\tmove $fp $sp\n")
                    #push space for locals
                    z = numLocDec*4
                    f.write("\t\taddiu $sp, $sp, "+str(z)+"\n")
                    for child in tree.child:
                        cgen(child)                 
                else:
                    numParams, numLocDec = getFuncInfo(tree.child[0].str)
                    f.write("\t\t.text\n")
                    f.write(tree.child[0].str+":")
                    #push return addr
                    z = (numParams*-4)-4
                    f.write("\taddiu $sp, $sp, "+str(z)+"\n")
                    f.write("\t\tsw $ra, 0($sp)\n")
                    f.write("\t\taddiu $sp, $sp, 4\n")
                    #push control link, store old fp for paramter list
                    f.write("\t\tmove $fp, $sp\n")
                    z = (numLocDec*4)
                    f.write("\t\taddiu $sp, $sp, "+str(z)+"\n")
                    
                    numeroLocales = numLocDec
                    
                    cgen(tree.child[2])
                    
                    #load return address
                    f.write("\t\tlw $ra, -4($fp)\n")
                    #guardar en el fp el fp con offset -8
                    f.write("\t\tlw $fp, -8($fp)\n")
                    #restore sp
                    z = numLocDec*-4 - 8
                    f.write("\t\taddiu $sp, $sp, "+str(z)+"\n")
                    f.write("\t\tjr $ra\n\n") # return
            elif(tree.decType == DecTipo.VARIABLE):
                shouldCheckChilds = False
            elif(tree.decType == DecTipo.ARREGLO):
                shouldCheckChilds = False
        elif(tree.nType == TipoNodo.EXP): #si es una expresion
            if(tree.expType == ExpTipo.IDENTIFIER): #si es un identificador
                #Buscar la dirección donde está la variable
                #Cargarla al acumulador
                location, scope = getLocation(tree.str, tree.lineno)
                if scope == 0:
                    f.write("\t\tlw $a0, "+str(location)+"($t7)\n")
                else:
                    f.write("\t\tlw $a0, "+str(location)+"($fp)\n")
                pass      
            elif(tree.expType == ExpTipo.ARREGLO): #si es un arreglo
                location, scope = getLocation(tree.child[0].str, tree.lineno)
                aux_tree = tree.child[1]
                if(aux_tree.expType == ExpTipo.CONST):
                    pos = int(aux_tree.val) * 4
                    f.write("\t\tlw $a0, "+str(location+pos)+"($t7)\n")
                else:
                    cgen(tree.child[1])
                    f.write("\t\tmul $a0, $a0, 4\n")
                    f.write("\t\tadd $t7, $t7, $a0\n")
                    f.write("\t\tmove$t0 $a0\n")
                    f.write("\t\tlw $a0, "+str(location)+"($t7)\n")
                    f.write("\t\tsub $t7, $t7, $t0\n")
                shouldCheckChilds = False
                pass
            elif (tree.expType == ExpTipo.OPERATION):
                cgen(tree.child[0])
                f.write("\t\tsw $a0 0($sp)\n")
                f.write("\t\taddiu $sp $sp 4\n")
                cgen(tree.child[1])
                f.write("\t\tlw $t1 -4($sp)\n")
                if(tree.op == TokenType.PLUS):
                    f.write("\t\tadd $a0 $t1 $a0\n")
                elif(tree.op == TokenType.LESS):
                    f.write("\t\tsubu $a0 $t1 $a0\n")
                elif(tree.op == TokenType.MULT):
                    f.write("\t\tmul $a0 $t1 $a0\n")
                elif(tree.op == TokenType.DIV):
                    f.write("\t\tdiv $a0 $t1 $a0\n")

                f.write("\t\taddiu $sp $sp -4\n")
                shouldCheckChilds = False
            elif(tree.expType == ExpTipo.ASSIGN):
                cgen(tree.child[1])
                if(tree.child[0].expType == ExpTipo.ARREGLO):
                    aux_tree = tree.child[0].child[0]
                    location, scope = getLocation(aux_tree.str,tree.lineno)
                    aux_tree = tree.child[0].child[1]
                    if(aux_tree.expType == ExpTipo.CONST):
                        pos = int(aux_tree.val) * 4
                        f.write("\t\tsw $a0, "+str(location+pos)+"($t7)\n")
                    else:
                        f.write("\t\tmove $t1, $a0\n")
                        cgen(tree.child[0].child[1])
                        f.write("\t\tmul $a0, $a0, 4\n")
                        f.write("\t\tadd $t7, $t7, $a0\n")
                        f.write("\t\tsw $t1, "+str(location)+"($t7)\n")
                        f.write("\t\tsub $t7, $t7, $a0\n")
                else: 
                    location, scope = getLocation(tree.child[0].str,tree.child[0].lineno)
                    if scope == 0:
                        f.write("\t\tsw $a0, "+str(location)+"($t7)\n")
                    else:
                        f.write("\t\tsw $a0, "+str(location)+"($fp)\n")
                    
                # f.write("\tsw $a0 "+str(location)+"($sp)\n")
                # cgen(tree.child[1])
                shouldCheckChilds = False
                pass
            elif(tree.expType == ExpTipo.CONST):
                f.write("\t\tli $a0 "+str(tree.val)+"\n")
        elif(tree.nType == TipoNodo.STMT):
            if(tree.stmtType == StmtTipo.IF):
                f.write("#empieza el if\n")
                cgen(tree.child[0].child[0])
                f.write("\t\tsw $a0 0($sp)\n")
                f.write("\t\taddiu $sp $sp 4\n")
                cgen(tree.child[0].child[1])
                f.write("\t\tlw $t1 -4($sp)\n")
                f.write("\t\taddiu $sp $sp -4\n")
                ifCounter += 1
                localIfCounter = ifCounter
                if(tree.child[0].op == TokenType.EQUAL):
                    f.write("\t\tbeq $a0 $t1 true_branch_if_"+str(localIfCounter)+"\n")
                elif(tree.child[0].op == TokenType.DIFF):
                    f.write("\t\tbne $a0 $t1 true_branch_if_"+str(localIfCounter)+"\n")
                elif(tree.child[0].op == TokenType.GREATERT):
                    f.write("\t\tbgt $t1 $a0 true_branch_if_"+str(localIfCounter)+"\n")
                elif(tree.child[0].op == TokenType.GTEQUAL):
                    f.write("\t\tbge $t1 $a0 true_branch_if_"+str(localIfCounter)+"\n")
                elif(tree.child[0].op == TokenType.LOWERTHAN):
                    f.write("\t\tblt $t1 $a0 true_branch_if_"+str(localIfCounter)+"\n")
                elif(tree.child[0].op == TokenType.LTEQUAL):
                    f.write("\t\tble $t1 $a0 true_branch_if_"+str(localIfCounter)+"\n")
                f.write("false_branch_if_"+str(localIfCounter)+":\n")
                cgen(tree.child[2])
                f.write("\t\tb end_if_"+str(localIfCounter)+"\n")
                f.write("true_branch_if_"+str(localIfCounter)+":\n")
                cgen(tree.child[1])
                f.write("end_if_"+str(localIfCounter)+":\n")
                shouldCheckChilds = False
                pass
            elif(tree.stmtType == StmtTipo.WHILE):
                whileCounter+=1
                localWhileCounter = whileCounter
                f.write("#empieza el if\n")
                f.write("start_while_"+str(localWhileCounter)+":\n")
                cgen(tree.child[0].child[0])
                f.write("\t\tsw $a0 0($sp)\n")
                f.write("\t\taddiu $sp $sp 4\n")
                cgen(tree.child[0].child[1])
                f.write("\t\tlw $t1 -4($sp)\n")
                f.write("\t\taddiu $sp $sp -4\n")
                if(tree.child[0].op == TokenType.EQUAL):
                    f.write("\t\tbeq $a0 $t1 true_branch_while_"+str(localWhileCounter)+"\n")
                elif(tree.child[0].op == TokenType.DIFF):
                    f.write("\t\tbne $a0 $t1 true_branch_while_"+str(localWhileCounter)+"\n")
                elif(tree.child[0].op == TokenType.GREATERT):
                    f.write("\t\tbgt $t1 $a0 true_branch_while_"+str(localWhileCounter)+"\n")
                elif(tree.child[0].op == TokenType.GTEQUAL):
                    f.write("\t\tbge $t1 $a0 true_branch_while_"+str(localWhileCounter)+"\n")
                elif(tree.child[0].op == TokenType.LOWERTHAN):
                    f.write("\t\tblt $t1 $a0 true_branch_while_"+str(localWhileCounter)+"\n")
                elif(tree.child[0].op == TokenType.LTEQUAL):
                    f.write("\t\tble $t1 $a0 true_branch_while_"+str(localWhileCounter)+"\n")
                f.write("\t\tb end_while_"+str(localWhileCounter)+"\n")
                f.write("true_branch_while_"+str(localWhileCounter)+":\n")
                cgen(tree.child[1])
                f.write("\t\tb start_while_"+str(localWhileCounter)+"\n")
                f.write("end_while_"+str(localWhileCounter)+":\n")
                shouldCheckChilds = False
                pass
            elif(tree.stmtType == StmtTipo.CALL):
                if(tree.child[0].str == "output"):
                    cgen(tree.child[1])
                    f.write("\t\tli $v0 1\n")
                    f.write("\t\tsyscall\n")
                elif(tree.child[0].str == "input"):
                    f.write("\t\tli $v0 5\n")
                    f.write("\t\tsyscall\n")
                    f.write("\t\tmove $a0 $v0\n")
                else:
                    numParams, localDec = getFuncInfo(tree.child[0].str)
                    #setear frame pointer donde empieza a guardar los parametros
                    f.write("\t\tsw $fp, 0($sp)\n")
                    f.write("\t\taddiu $sp, $sp, 8\n")
                    #recorrer el primer hijo y sus siblings
                    aux_tree = tree.child[1]

                    for i in range(numParams):
                        cgen(aux_tree, False)
                        f.write("\t\tsw $a0 0($sp)\n")
                        f.write("\t\taddiu $sp, $sp, 4\n")
                        aux_tree = aux_tree.sibling
                        if(aux_tree == None):
                            break
                    
                    f.write("\t\tjal "+tree.child[0].str+"\n")

                shouldCheckChilds = False
            elif(tree.stmtType == StmtTipo.RETURN):
                shouldCheckChilds =False
                for child in tree.child:
                    cgen(child)
                #load return address
                f.write("\t\tlw $ra, -4($fp)\n")
                #guardar en el fp el fp con offset -8
                f.write("\t\tlw $fp, -8($fp)\n")
                #restore sp
                z = numeroLocales*-4 - 8
                f.write("\t\taddiu $sp, $sp, "+str(z)+"\n")
                f.write("\t\tjr $ra\n\n") # return
                pass
        if shouldCheckChilds: #si se deben checar los hijos
            for child in tree.child:
                cgen(child)
        if shouldCheckSiblings:
            cgen(tree.sibling)
    pass

def codeGen(tree, file):
    global f
    f = open(file, "w")
    cgen(tree)
    f.write("\n\t\tli $v0 10\n")
    f.write("\t\tsyscall")
    f.close()
    pass