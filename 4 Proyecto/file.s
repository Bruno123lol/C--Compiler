		.text
minloc:	addiu $sp, $sp, -16
		sw $ra, 0($sp)
		addiu $sp, $sp, 4
		move $fp, $sp
		addiu $sp, $sp, 24
		lw $a0, 4($fp)
		sw $a0, 20($fp)
		lw $a0, 4($fp)
		mul $a0, $a0, 4
		add $t7, $t7, $a0
		move$t0 $a0
		lw $a0, 0($t7)
		sub $t7, $t7, $t0
		sw $a0, 16($fp)
		lw $a0, 4($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		li $a0 1
		lw $t1 -4($sp)
		add $a0 $t1 $a0
		addiu $sp $sp -4
		sw $a0, 12($fp)
#empieza el if
start_while_1:
		lw $a0, 12($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		lw $a0, 8($fp)
		lw $t1 -4($sp)
		addiu $sp $sp -4
		blt $t1 $a0 true_branch_while_1
		b end_while_1
true_branch_while_1:
#empieza el if
		lw $a0, 12($fp)
		mul $a0, $a0, 4
		add $t7, $t7, $a0
		move$t0 $a0
		lw $a0, 0($t7)
		sub $t7, $t7, $t0
		sw $a0 0($sp)
		addiu $sp $sp 4
		lw $a0, 16($fp)
		lw $t1 -4($sp)
		addiu $sp $sp -4
		blt $t1 $a0 true_branch_if_1
false_branch_if_1:
		b end_if_1
true_branch_if_1:
		lw $a0, 12($fp)
		mul $a0, $a0, 4
		add $t7, $t7, $a0
		move$t0 $a0
		lw $a0, 0($t7)
		sub $t7, $t7, $t0
		sw $a0, 16($fp)
		lw $a0, 12($fp)
		sw $a0, 20($fp)
end_if_1:
		lw $a0, 12($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		li $a0 1
		lw $t1 -4($sp)
		add $a0 $t1 $a0
		addiu $sp $sp -4
		sw $a0, 12($fp)
		b start_while_1
end_while_1:
		lw $a0, 20($fp)
		lw $ra, -4($fp)
		lw $fp, -8($fp)
		addiu $sp, $sp, -32
		jr $ra

		lw $ra, -4($fp)
		lw $fp, -8($fp)
		addiu $sp, $sp, -32
		jr $ra

		.text
sort:	addiu $sp, $sp, -16
		sw $ra, 0($sp)
		addiu $sp, $sp, 4
		move $fp, $sp
		addiu $sp, $sp, 20
		lw $a0, 4($fp)
		sw $a0, 12($fp)
#empieza el if
start_while_2:
		lw $a0, 12($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		lw $a0, 8($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		li $a0 1
		lw $t1 -4($sp)
		subu $a0 $t1 $a0
		addiu $sp $sp -4
		lw $t1 -4($sp)
		addiu $sp $sp -4
		blt $t1 $a0 true_branch_while_2
		b end_while_2
true_branch_while_2:
		sw $fp, 0($sp)
		addiu $sp, $sp, 8
		lw $a0, 0($fp)
		sw $a0 0($sp)
		addiu $sp, $sp, 4
		lw $a0, 12($fp)
		sw $a0 0($sp)
		addiu $sp, $sp, 4
		lw $a0, 8($fp)
		sw $a0 0($sp)
		addiu $sp, $sp, 4
		jal minloc
		sw $a0, 16($fp)
		lw $a0, 16($fp)
		mul $a0, $a0, 4
		add $t7, $t7, $a0
		move$t0 $a0
		lw $a0, 0($t7)
		sub $t7, $t7, $t0
		sw $a0, 20($fp)
		lw $a0, 12($fp)
		mul $a0, $a0, 4
		add $t7, $t7, $a0
		move$t0 $a0
		lw $a0, 0($t7)
		sub $t7, $t7, $t0
		move $t1, $a0
		lw $a0, 16($fp)
		mul $a0, $a0, 4
		add $t7, $t7, $a0
		sw $t1, 0($t7)
		sub $t7, $t7, $a0
		lw $a0, 20($fp)
		move $t1, $a0
		lw $a0, 12($fp)
		mul $a0, $a0, 4
		add $t7, $t7, $a0
		sw $t1, 0($t7)
		sub $t7, $t7, $a0
		lw $a0, 12($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		li $a0 1
		lw $t1 -4($sp)
		add $a0 $t1 $a0
		addiu $sp $sp -4
		sw $a0, 12($fp)
		b start_while_2
end_while_2:
		lw $ra, -4($fp)
		lw $fp, -8($fp)
		addiu $sp, $sp, -28
		jr $ra

		.data
		globalVars: .word 2
		.text
		.globl main
main:	la $t7, globalVars
		move $fp $sp
		addiu $sp, $sp, 4
		lw $a0, 0($t7)
		li $a0 0
		sw $a0, 0($fp)
#empieza el if
start_while_3:
		lw $a0, 0($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		li $a0 10
		lw $t1 -4($sp)
		addiu $sp $sp -4
		blt $t1 $a0 true_branch_while_3
		b end_while_3
true_branch_while_3:
		li $v0 5
		syscall
		move $a0 $v0
		move $t1, $a0
		lw $a0, 0($fp)
		mul $a0, $a0, 4
		add $t7, $t7, $a0
		sw $t1, 0($t7)
		sub $t7, $t7, $a0
		lw $a0, 0($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		li $a0 1
		lw $t1 -4($sp)
		add $a0 $t1 $a0
		addiu $sp $sp -4
		sw $a0, 0($fp)
		b start_while_3
end_while_3:
		sw $fp, 0($sp)
		addiu $sp, $sp, 8
		lw $a0, 0($t7)
		sw $a0 0($sp)
		addiu $sp, $sp, 4
		li $a0 0
		sw $a0 0($sp)
		addiu $sp, $sp, 4
		li $a0 10
		sw $a0 0($sp)
		addiu $sp, $sp, 4
		jal sort
		li $a0 0
		sw $a0, 0($fp)
#empieza el if
start_while_4:
		lw $a0, 0($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		li $a0 10
		lw $t1 -4($sp)
		addiu $sp $sp -4
		blt $t1 $a0 true_branch_while_4
		b end_while_4
true_branch_while_4:
		lw $a0, 0($fp)
		mul $a0, $a0, 4
		add $t7, $t7, $a0
		move$t0 $a0
		lw $a0, 0($t7)
		sub $t7, $t7, $t0
		li $v0 1
		syscall
		lw $a0, 0($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		li $a0 1
		lw $t1 -4($sp)
		add $a0 $t1 $a0
		addiu $sp $sp -4
		sw $a0, 0($fp)
		b start_while_4
end_while_4:

		li $v0 10
		syscall