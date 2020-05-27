from globalTypes import * 
from semantica import *
import sys

f= ""
# TM location number for current instruction emission
emitLoc = 0
# Highest TM location emitted so far for use in conjunction with emitSkip,
# emitBackup, and emitRestore
highEmitLoc = 0

def cgen(tree):
    
    if tree != None:
        shouldCheckChilds = True #variable para saber cuando se requieren checar los hijos de la rama
        if(tree.nType == TipoNodo.DEC):
            if(tree.decType == DecTipo.FUNCION):
                if(tree.child[0].str == "main"):
                    f.write("\t\t.text\n")
                    f.write("\t\t.globl main\n")
                    f.write("main:")
                else: 
                    f.write("\t\t.text\n")
                    f.write(tree.child[0].str+":")
                pass
        elif(tree.nType == TipoNodo.EXP): #si es una expresion

            if(tree.expType == ExpTipo.IDENTIFIER): #si es un identificador
                pass
            
            if(tree.expType == ExpTipo.ARREGLO): #si es un arreglo
                pass

            if (tree.expType == ExpTipo.OPERATION):
                # if(tree.op == TokenType.PLUS):

                pass
            if(tree.expType == ExpTipo.ASSIGN):
                cgen(tree.child[1])
                if(tree.child[0].expType == ExpTipo.ARREGLO):
                    aux_tree = tree.child[0].child[0]
                    location, scope = getLocation(aux_tree.str,aux_tree.lineno)
                    aux_tree = tree.child[0].child[1]
                    pos = int(aux_tree.val) * 4
                    f.write("\tsw $a0 "+str(location+pos)+"($sp)\n")
                else: 
                    location, scope = getLocation(tree.child[0].str,tree.child[0].lineno)
                    f.write("\tsw $a0 "+str(location)+"($sp)\n")
                # f.write("\tsw $a0 "+str(location)+"($sp)\n")
                # cgen(tree.child[1])
                shouldCheckChilds = False
                pass
            if(tree.expType == ExpTipo.CONST):
                f.write("\tli $a0 "+str(tree.val)+"\n")
            if(tree.expType == ExpTipo.IDENTIFIER):
                # location, scope = getLocation(tree.child[0].str,tree.child[0].lineno)
                pass
        if shouldCheckChilds: #si se deben checar los hijos
            for child in tree.child:
                cgen(child)
        
        cgen(tree.sibling)
    pass


def codeGen(tree, file):
    global f
    f = open(file, "w")
    f.write("\t\t.data\n")
    f.write("\t\tglob: .word 0\n")
    cgen(tree)
    # f.close()
    pass