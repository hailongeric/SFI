	.file	"test_SFI.c"
	.text
	.type	test_ptr_function, @function
test_ptr_function:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	movl	$0, %eax
	popq	%rbp
	ret
	.size	test_ptr_function, .-test_ptr_function
	.globl	sfimain
	.type	sfimain, @function
sfimain:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$96, %rsp
	movl	$0, -12(%rbp)
	jmp	.L4
.L13:
	movl	$0, -16(%rbp)
	jmp	.L5
.L12:
	movl	$0, -20(%rbp)
	movl	$0, -24(%rbp)
	jmp	.L6
.L11:
	movl	-24(%rbp), %eax
	movl	%eax, -28(%rbp)
	cmpl	$4096, -28(%rbp)
	je	.L15
	cmpl	$4112, -28(%rbp)
	jne	.L9
	movl	-20(%rbp), %eax
	addl	%eax, %eax
	addl	$1, %eax
	movl	%eax, -20(%rbp)
.L9:
	leaq	test_ptr_function(%rip), %rax
	movq	%rax, -8(%rbp)
	jmp	.L10
.L15:
	nop
.L10:
	movq	-8(%rbp), %rdx
	movl	$0, %eax
	call	*%rdx
	addl	$1, -24(%rbp)
.L6:
	cmpl	$1, -24(%rbp)
	jle	.L11
	movl	-16(%rbp), %eax
	cltq
	movl	-12(%rbp), %edx
	movslq	%edx, %rdx
	salq	$2, %rdx
	addq	%rax, %rdx
	movl	-20(%rbp), %eax
	movl	%eax, -96(%rbp,%rdx,4)
	addl	$1, -16(%rbp)
.L5:
	cmpl	$1, -16(%rbp)
	jle	.L12
	addl	$1, -12(%rbp)
.L4:
	cmpl	$1, -12(%rbp)
	jle	.L13
	movl	$-1, %eax
	leave
	ret
	.size	sfimain, .-sfimain
	.ident	"GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
