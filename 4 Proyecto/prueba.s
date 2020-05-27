        .data
        .align 2
    x: .space 4
        .data
        .align 2
    y: .space 40            

        .text
        .globl main

main:   li $t0, 1
        sw $t0, x
        li $t1, 2
        sw $t1, y
        li $t1, 3
        sw $t1, y

        add $t2 $t1 $t0
        
        
        


        
