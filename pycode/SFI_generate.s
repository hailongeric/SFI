	.file	"SFI_functions.c"
	.text
	.globl	sfi_htons
	.type	sfi_htons, @function
	.align 32
sfi_htons:
	lea 	-8(%r15), %r15
	movq	%r14, 0(%r15)
	movq	%r15, %r14
	movl	%edi, %eax
	movw	%ax, -20(%r14)
	leaq	-20(%r14), %rax
	movq	%rax, -8(%r14)
	movq	-8(%r14), %rax
	.align 32
	mov 	%eax, %eax
	movzbl	(%r13, %rax), %eax
	movzbl	%al, %eax
	sall	$8, %eax
	movl	%eax, %edx
	movq	-8(%r14), %rax
	addq	$1, %rax
	mov 	%eax, %eax
	movzbl	(%r13, %rax), %eax
	.align 32
	movzbl	%al, %eax
	orl	%edx, %eax
	movq	0(%r15), %r14
	lea 	8(%r15), %r15
	.align 32
	lea 	8(%r15), %r15
	movl	-8(%r15), %edi
	mov 	$5, %esi
	shrx	%esi, %edi, %edi
	shlx	%esi, %edi, %edi
	lea 	(%r13, %rdi, 1), %rdi
	jmp 	 %rdi
	.size	sfi_htons, .-sfi_htons
	