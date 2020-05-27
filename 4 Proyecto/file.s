		.data
		glob: .word 0
		.text
		.globl main
main:	li $a0 5
	li $a0 1
	sw $a0 4($sp)
