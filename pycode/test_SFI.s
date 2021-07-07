	.file	"test_SFI.c"
	.text
	.type	add, @function
add:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	movl	%edi, -68(%rbp)
	movl	%esi, -72(%rbp)
	movl	-68(%rbp), %edx
	movl	-72(%rbp), %eax
	addl	%edx, %eax
	movl	%eax, -52(%rbp)
	movq	$0, -48(%rbp)
	movq	$0, -40(%rbp)
	movq	$0, -32(%rbp)
	movq	$0, -24(%rbp)
	movq	$0, -16(%rbp)
	movq	$0, -8(%rbp)
	cmpl	$0, -52(%rbp)ddddd
	je	.L5
	movl	$90, -52(%rbp)
	jmp	.L3
.L5:
	nop
.L3:
	movl	-52(%rbp), %eax 
	popq	%rbp
	ret
	.size	add, .-add
	.globl	mymain
	.type	mymain, @function
mymain:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$16, %rsp
	movl	$10, -12(%rbp)
	movl	$20, -8(%rbp)
	movl	$0, -4(%rbp) 
	movl	-8(%rbp), %edx
	movl	-12(%rbp), %eax
	movl	%edx, %esi
	movl	%eax, %edi
	call	add
	movl	%eax, -4(%rbp)
	movl	$0, %eax
	leave
	ret
	.size	mymain, .-mymain
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
