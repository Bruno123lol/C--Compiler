		.text
gcd:	addiu $sp, $sp, -12
		sw $ra, 0($sp)
		addiu $sp, $sp, 4
		move $fp, $sp
		addiu $sp, $sp, 8
#empieza el if
		lw $a0, 4($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		li $a0 0
		lw $t1 -4($sp)
		addiu $sp $sp -4
		beq $a0 $t1 true_branch_if_1
false_branch_if_1:
		sw $fp, 0($sp)
		addiu $sp, $sp, 8
		lw $a0, 4($fp)
		sw $a0 0($sp)
		addiu $sp, $sp, 4
		lw $a0, 0($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		lw $a0, 0($fp)
		sw $a0 0($sp)
		addiu $sp $sp 4
		lw $a0, 4($fp)
		lw $t1 -4($sp)
		div $a0 $t1 $a0
		addiu $sp $sp -4
		sw $a0 0($sp)
		addiu $sp $sp 4
		lw $a0, 4($fp)
		lw $t1 -4($sp)
		mul $a0 $t1 $a0
		addiu $sp $sp -4
		lw $t1 -4($sp)
		subu $a0 $t1 $a0
		addiu $sp $sp -4
		sw $a0 0($sp)
		addiu $sp, $sp, 4
		jal gcd
		lw $ra, -4($fp)
		lw $fp, -8($fp)
		addiu $sp, $sp, -16
		jr $ra

		b end_if_1
true_branch_if_1:
		lw $a0, 0($fp)
		lw $ra, -4($fp)
		lw $fp, -8($fp)
		addiu $sp, $sp, -16
		jr $ra

end_if_1:
		lw $ra, -4($fp)
		lw $fp, -8($fp)
		addiu $sp, $sp, -16
		jr $ra

		.data
		globalVars: .word 2
		.text
		.globl main
main:	la $t7, globalVars
		move $fp $sp
		addiu $sp, $sp, 8
		lw $a0, 0($t7)
		li $v0 5
		syscall
		move $a0 $v0
		sw $a0, 0($fp)
		li $v0 5
		syscall
		move $a0 $v0
		sw $a0, 4($fp)
		sw $fp, 0($sp)
		addiu $sp, $sp, 8
		lw $a0, 0($fp)
		sw $a0 0($sp)
		addiu $sp, $sp, 4
		lw $a0, 4($fp)
		sw $a0 0($sp)
		addiu $sp, $sp, 4
		jal gcd
		li $v0 1
		syscall

		li $v0 10
		syscall