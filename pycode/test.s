	.file	"SFI_functions.c"
	.text
	.type	SFI_CALL, @function
SFI_CALL:
	pushq	%rbp
	movq	%rsp, %rbp
	movl	%edi, -20(%rbp)
	movl	%esi, -24(%rbp)
	movl	%edx, -28(%rbp)
	movq	%rcx, -40(%rbp)
	movq	%r8, -48(%rbp)
#APP
# 28 "src/SFI_register.h" 1
	movq	$0x500, %rax
	movl	-20(%rbp), %edi
	movl	-24(%rbp), %esi
	movl	-28(%rbp), %edx
	movl	-40(%rbp), %ecx
	movl	-48(%rbp), %r8d
	syscall
	movl	 %eax, %r9d
# 0 "" 2
#NO_APP
	movl	%r9d, -4(%rbp)
	movl	-4(%rbp), %eax
	popq	%rbp
	ret
	.size	SFI_CALL, .-SFI_CALL
	.type	SFI_LIBRARY_CALL, @function
SFI_LIBRARY_CALL:
	pushq	%rbp
	movq	%rsp, %rbp
	movl	%edi, -20(%rbp)
	movl	%esi, -24(%rbp)
	movl	%edx, -28(%rbp)
	movq	%rcx, -40(%rbp)
	movq	%r8, -48(%rbp)
#APP
# 44 "src/SFI_register.h" 1
	movq	$0x600, %rax
	movl	-20(%rbp), %edi
	movl	-24(%rbp), %esi
	movl	-28(%rbp), %edx
	movl	-40(%rbp), %ecx
	movl	-48(%rbp), %r8d
	syscall
	movl	 %eax, %r9d
# 0 "" 2
#NO_APP
	movl	%r9d, -4(%rbp)
	movl	-4(%rbp), %eax
	popq	%rbp
	ret
	.size	SFI_LIBRARY_CALL, .-SFI_LIBRARY_CALL
	.type	max, @function
max:
	pushq	%rbp
	movq	%rsp, %rbp
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	movl	-4(%rbp), %eax
	cmpl	%eax, -8(%rbp)
	cmovnb	-8(%rbp), %eax
	popq	%rbp
	ret
	.size	max, .-max
	.type	min, @function
min:
	pushq	%rbp
	movq	%rsp, %rbp
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	movl	-4(%rbp), %eax
	cmpl	%eax, -8(%rbp)
	cmovbe	-8(%rbp), %eax
	popq	%rbp
	ret
	.size	min, .-min
	.type	queue_alloc, @function
queue_alloc:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -40(%rbp)
	movq	-40(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, -8(%rbp)
	movq	-8(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	-40(%rbp), %rax
	movq	8(%rax), %rcx
	movq	%rdx, %rax
	movl	$0, %edx
	divq	%rcx
	movq	%rdx, -16(%rbp)
	movq	-40(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, -24(%rbp)
	movq	-40(%rbp), %rax
	movq	24(%rax), %rax
	cmpq	%rax, -16(%rbp)
	jne	.L10
	movl	$-1, %eax
	jmp	.L11
.L10:
	movq	-8(%rbp), %rax
	movl	%eax, %edx
	movq	-24(%rbp), %rax
	imull	%edx, %eax
.L11:
	popq	%rbp
	ret
	.size	queue_alloc, .-queue_alloc
	.type	queue_commit, @function
queue_commit:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -24(%rbp)
	movq	-24(%rbp), %rax
	movq	16(%rax), %rax
	leaq	1(%rax), %rdx
	movq	-24(%rbp), %rax
	movq	8(%rax), %rcx
	movq	%rdx, %rax
	movl	$0, %edx
	divq	%rcx
	movq	%rdx, -8(%rbp)
	movq	-24(%rbp), %rax
	movq	-8(%rbp), %rdx
	movq	%rdx, 16(%rax)
	nop
	popq	%rbp
	ret
	.size	queue_commit, .-queue_commit
	.type	queue_peek, @function
queue_peek:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movq	-24(%rbp), %rax
	movq	24(%rax), %rax
	movq	%rax, -8(%rbp)
	movq	-24(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, -16(%rbp)
	movq	-24(%rbp), %rax
	movq	16(%rax), %rax
	cmpq	%rax, -8(%rbp)
	jne	.L14
	movl	$0, %eax
	jmp	.L15
.L14:
	movq	-8(%rbp), %rax
	movl	%eax, %edx
	movq	-16(%rbp), %rax
	imull	%edx, %eax
	movl	%eax, %edx
	movq	-32(%rbp), %rax
	movl	%edx, (%rax)
	movl	$1, %eax
.L15:
	popq	%rbp
	ret
	.size	queue_peek, .-queue_peek
	.type	queue_discard, @function
queue_discard:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movq	$0, -8(%rbp)
	jmp	.L17
.L20:
	movq	-24(%rbp), %rax
	movq	24(%rax), %rax
	movq	%rax, -16(%rbp)
	movq	-24(%rbp), %rax
	movq	16(%rax), %rax
	cmpq	%rax, -16(%rbp)
	je	.L22
	movq	-16(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	-24(%rbp), %rax
	movq	8(%rax), %rcx
	movq	%rdx, %rax
	movl	$0, %edx
	divq	%rcx
	movq	-24(%rbp), %rax
	movq	%rdx, 24(%rax)
	addq	$1, -8(%rbp)
.L17:
	movq	-8(%rbp), %rax
	cmpq	-32(%rbp), %rax
	jb	.L20
	jmp	.L19
.L22:
	nop
.L19:
	movq	-8(%rbp), %rax
	popq	%rbp
	ret
	.size	queue_discard, .-queue_discard
	.type	queue_isempty, @function
queue_isempty:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	16(%rax), %rdx
	movq	-8(%rbp), %rax
	movq	24(%rax), %rax
	cmpq	%rax, %rdx
	sete	%al
	movzbl	%al, %eax
	popq	%rbp
	ret
	.size	queue_isempty, .-queue_isempty
	.comm	info,20,16
	.comm	mac_broadcast_addr,6,1
	.type	ip_hdr_hlen, @function
ip_hdr_hlen:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	andl	$15, %eax
	sall	$2, %eax
	cltq
	popq	%rbp
	ret
	.size	ip_hdr_hlen, .-ip_hdr_hlen
	.type	sfi_memcpy, @function
sfi_memcpy:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -40(%rbp)
	movq	%rsi, -48(%rbp)
	movq	%rdx, -56(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, -16(%rbp)
	movq	-40(%rbp), %rax
	movq	%rax, -24(%rbp)
	movl	$0, -4(%rbp)
	jmp	.L28
.L29:
	movl	-4(%rbp), %eax
	movslq	%eax, %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movl	-4(%rbp), %edx
	movslq	%edx, %rcx
	movq	-24(%rbp), %rdx
	addq	%rcx, %rdx
	movzbl	(%rax), %eax
	movb	%al, (%rdx)
	addl	$1, -4(%rbp)
.L28:
	movl	-4(%rbp), %eax
	cltq
	cmpq	%rax, -56(%rbp)
	ja	.L29
	nop
	nop
	popq	%rbp
	ret
	.size	sfi_memcpy, .-sfi_memcpy
	.type	sfi_memcmp, @function
sfi_memcmp:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -40(%rbp)
	movq	%rsi, -48(%rbp)
	movl	%edx, -52(%rbp)
	movq	-40(%rbp), %rax
	movq	%rax, -8(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, -16(%rbp)
	movl	$0, -20(%rbp)
	movq	-40(%rbp), %rax
	cmpq	-48(%rbp), %rax
	jne	.L33
	movl	-20(%rbp), %eax
	jmp	.L32
.L38:
	movq	-8(%rbp), %rax
	movzbl	(%rax), %edx
	movq	-16(%rbp), %rax
	movzbl	(%rax), %eax
	cmpb	%al, %dl
	je	.L34
	movq	-8(%rbp), %rax
	movzbl	(%rax), %edx
	movq	-16(%rbp), %rax
	movzbl	(%rax), %eax
	cmpb	%al, %dl
	jbe	.L35
	movl	$1, %eax
	jmp	.L36
.L35:
	movl	$-1, %eax
.L36:
	movl	%eax, -20(%rbp)
	jmp	.L37
.L34:
	subl	$1, -52(%rbp)
	addq	$1, -8(%rbp)
	addq	$1, -16(%rbp)
.L33:
	cmpl	$0, -52(%rbp)
	jg	.L38
.L37:
	movl	-20(%rbp), %eax
.L32:
	popq	%rbp
	ret
	.size	sfi_memcmp, .-sfi_memcmp
	.type	my_memset, @function
my_memset:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -24(%rbp)
	movl	%esi, -28(%rbp)
	movl	%edx, -32(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, -8(%rbp)
	movl	$0, -12(%rbp)
	jmp	.L40
.L41:
	movl	-28(%rbp), %eax
	movl	%eax, %edx
	movq	-8(%rbp), %rax
	movb	%dl, (%rax)
	addq	$1, -8(%rbp)
	subl	$1, -32(%rbp)
.L40:
	cmpl	$0, -32(%rbp)
	jg	.L41
	movq	-24(%rbp), %rax
	popq	%rbp
	ret
	.size	my_memset, .-my_memset
	.type	sfi_ntohl, @function
sfi_ntohl:
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$24, %rsp
	movl	%edi, -20(%rbp)
	movl	$0, -4(%rbp)
	leaq	-20(%rbp), %rcx
	leaq	-4(%rbp), %rax
	movl	$4, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	sfi_memcmp
	movzbl	-1(%rbp), %eax
	movzbl	%al, %eax
	movzbl	-2(%rbp), %edx
	movzbl	%dl, %edx
	sall	$8, %edx
	orl	%eax, %edx
	movzbl	-3(%rbp), %eax
	movzbl	%al, %eax
	sall	$16, %eax
	orl	%eax, %edx
	movzbl	-4(%rbp), %eax
	movzbl	%al, %eax
	sall	$24, %eax
	orl	%edx, %eax
	leave
	ret
	.size	sfi_ntohl, .-sfi_ntohl
	.type	sfi_ntohs, @function
sfi_ntohs:
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$24, %rsp
	movl	%edi, %eax
	movw	%ax, -20(%rbp)
	movw	$0, -2(%rbp)
	leaq	-20(%rbp), %rcx
	leaq	-2(%rbp), %rax
	movl	$2, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	sfi_memcmp
	movzbl	-1(%rbp), %eax
	movzbl	%al, %eax
	movzbl	-2(%rbp), %edx
	movzbl	%dl, %edx
	sall	$8, %edx
	orl	%edx, %eax
	leave
	ret
	.size	sfi_ntohs, .-sfi_ntohs
	.type	sfi_htonl, @function
sfi_htonl:
	pushq	%rbp
	movq	%rsp, %rbp
	movl	%edi, -20(%rbp)
	leaq	-20(%rbp), %rax
	movq	%rax, -8(%rbp)
	movq	-8(%rbp), %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	sall	$24, %eax
	movl	%eax, %edx
	movq	-8(%rbp), %rax
	addq	$1, %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	sall	$16, %eax
	orl	%eax, %edx
	movq	-8(%rbp), %rax
	addq	$2, %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	sall	$8, %eax
	orl	%eax, %edx
	movq	-8(%rbp), %rax
	addq	$3, %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	orl	%edx, %eax
	popq	%rbp
	ret
	.size	sfi_htonl, .-sfi_htonl
	.type	sfi_htons, @function
sfi_htons:
	pushq	%rbp
	movq	%rsp, %rbp
	movl	%edi, %eax
	movw	%ax, -20(%rbp)
	leaq	-20(%rbp), %rax
	movq	%rax, -8(%rbp)
	movq	-8(%rbp), %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	sall	$8, %eax
	movl	%eax, %edx
	movq	-8(%rbp), %rax
	addq	$1, %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	orl	%edx, %eax
	popq	%rbp
	ret
	.size	sfi_htons, .-sfi_htons
	.local	ip_global_id
	.comm	ip_global_id,4,4
	.section	.rodata
	.align 16
	.type	ip_hdr_template, @object
	.size	ip_hdr_template, 20
ip_hdr_template:
	.byte	69
	.byte	0
	.zero	4
	.value	16384
	.byte	64
	.zero	11
	.text
	.type	dump_pkt, @function
dump_pkt:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -24(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, -8(%rbp)
	nop
	popq	%rbp
	ret
	.size	dump_pkt, .-dump_pkt
	.type	ip_checksum, @function
ip_checksum:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$48, %rsp
	movq	%rdi, -40(%rbp)
	movq	%rsi, -48(%rbp)
	movq	-40(%rbp), %rax
	movq	%rax, -24(%rbp)
	movl	$65535, -4(%rbp)
	movq	$0, -16(%rbp)
	jmp	.L53
.L55:
	movq	-24(%rbp), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movzwl	(%rax), %eax
	movw	%ax, -26(%rbp)
	movzwl	-26(%rbp), %eax
	movzwl	%ax, %eax
	addl	%eax, -4(%rbp)
	cmpl	$65535, -4(%rbp)
	jbe	.L54
	movl	$65535, %edi
	call	sfi_ntohs
	movzwl	%ax, %eax
	subl	%eax, -4(%rbp)
.L54:
	addq	$2, -16(%rbp)
.L53:
	movq	-16(%rbp), %rax
	addq	$1, %rax
	cmpq	%rax, -48(%rbp)
	ja	.L55
	movq	-48(%rbp), %rax
	andl	$1, %eax
	testq	%rax, %rax
	je	.L56
	movw	$0, -26(%rbp)
	movq	-48(%rbp), %rax
	leaq	-1(%rax), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	movb	%al, -26(%rbp)
	movzwl	-26(%rbp), %eax
	movzwl	%ax, %eax
	addl	%eax, -4(%rbp)
	cmpl	$65535, -4(%rbp)
	jbe	.L56
	movl	$65535, %edi
	call	sfi_ntohs
	movzwl	%ax, %eax
	subl	%eax, -4(%rbp)
.L56:
	movl	-4(%rbp), %eax
	notl	%eax
	leave
	ret
	.size	ip_checksum, .-ip_checksum
	.type	udp_checksum, @function
udp_checksum:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$72, %rsp
	movq	%rdi, -56(%rbp)
	movq	%rsi, -64(%rbp)
	movl	%edx, -68(%rbp)
	movl	%ecx, -72(%rbp)
	movq	-56(%rbp), %rax
	movq	%rax, -8(%rbp)
	leaq	-68(%rbp), %rax
	movq	%rax, -24(%rbp)
	leaq	-72(%rbp), %rax
	movq	%rax, -32(%rbp)
	movq	-64(%rbp), %rax
	movq	%rax, -40(%rbp)
	movl	$0, -12(%rbp)
	jmp	.L59
.L61:
	movq	-8(%rbp), %rax
	leaq	2(%rax), %rdx
	movq	%rdx, -8(%rbp)
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	addl	%eax, -12(%rbp)
	movl	-12(%rbp), %eax
	testl	%eax, %eax
	jns	.L60
	movl	-12(%rbp), %eax
	movzwl	%ax, %eax
	movl	-12(%rbp), %edx
	shrl	$16, %edx
	addl	%edx, %eax
	movl	%eax, -12(%rbp)
.L60:
	subq	$2, -64(%rbp)
.L59:
	cmpq	$1, -64(%rbp)
	ja	.L61
	movq	-64(%rbp), %rax
	andl	$1, %eax
	testq	%rax, %rax
	je	.L62
	movq	-8(%rbp), %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	addl	%eax, -12(%rbp)
.L62:
	movq	-24(%rbp), %rax
	leaq	2(%rax), %rdx
	movq	%rdx, -24(%rbp)
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	addl	%eax, -12(%rbp)
	movq	-24(%rbp), %rax
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	addl	%eax, -12(%rbp)
	movq	-32(%rbp), %rax
	leaq	2(%rax), %rdx
	movq	%rdx, -32(%rbp)
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	addl	%eax, -12(%rbp)
	movq	-32(%rbp), %rax
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	addl	%eax, -12(%rbp)
	movl	$17, %edi
	call	sfi_htons
	movzwl	%ax, %eax
	addl	%eax, -12(%rbp)
	movq	-40(%rbp), %rax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_htons
	movzwl	%ax, %eax
	addl	%eax, -12(%rbp)
	jmp	.L63
.L64:
	movl	-12(%rbp), %eax
	movzwl	%ax, %eax
	movl	-12(%rbp), %edx
	shrl	$16, %edx
	addl	%edx, %eax
	movl	%eax, -12(%rbp)
.L63:
	movl	-12(%rbp), %eax
	shrl	$16, %eax
	testl	%eax, %eax
	jne	.L64
	movl	-12(%rbp), %eax
	notl	%eax
	leave
	ret
	.size	udp_checksum, .-udp_checksum
	.type	ip_hton, @function
ip_hton:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$32, %rsp
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	call	ip_hdr_hlen
	movq	%rax, -8(%rbp)
	movq	-24(%rbp), %rax
	movzbl	(%rax), %edx
	movq	-32(%rbp), %rax
	movb	%dl, (%rax)
	movq	-24(%rbp), %rax
	movzbl	1(%rax), %edx
	movq	-32(%rbp), %rax
	movb	%dl, 1(%rax)
	movq	-24(%rbp), %rax
	movzwl	2(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_htons
	movq	-32(%rbp), %rdx
	movw	%ax, 2(%rdx)
	movq	-24(%rbp), %rax
	movzwl	4(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_htons
	movq	-32(%rbp), %rdx
	movw	%ax, 4(%rdx)
	movq	-24(%rbp), %rax
	movzwl	6(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_htons
	movq	-32(%rbp), %rdx
	movw	%ax, 6(%rdx)
	movq	-24(%rbp), %rax
	movzbl	8(%rax), %edx
	movq	-32(%rbp), %rax
	movb	%dl, 8(%rax)
	movq	-24(%rbp), %rax
	movzbl	9(%rax), %edx
	movq	-32(%rbp), %rax
	movb	%dl, 9(%rax)
	movq	-24(%rbp), %rax
	movzwl	10(%rax), %edx
	movq	-32(%rbp), %rax
	movw	%dx, 10(%rax)
	movq	-24(%rbp), %rax
	movl	12(%rax), %eax
	movl	%eax, %edi
	call	sfi_htonl
	movq	-32(%rbp), %rdx
	movl	%eax, 12(%rdx)
	movq	-24(%rbp), %rax
	movl	16(%rax), %eax
	movl	%eax, %edi
	call	sfi_htonl
	movq	-32(%rbp), %rdx
	movl	%eax, 16(%rdx)
	movq	-32(%rbp), %rax
	movw	$0, 10(%rax)
	movq	-8(%rbp), %rdx
	movq	-32(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	ip_checksum
	movq	-32(%rbp), %rdx
	movw	%ax, 10(%rdx)
	nop
	leave
	ret
	.size	ip_hton, .-ip_hton
	.type	ip_ntoh, @function
ip_ntoh:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movq	-8(%rbp), %rax
	movzbl	(%rax), %edx
	movq	-16(%rbp), %rax
	movb	%dl, (%rax)
	movq	-8(%rbp), %rax
	movzbl	1(%rax), %edx
	movq	-16(%rbp), %rax
	movb	%dl, 1(%rax)
	movq	-8(%rbp), %rax
	movzwl	2(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_ntohs
	movq	-16(%rbp), %rdx
	movw	%ax, 2(%rdx)
	movq	-8(%rbp), %rax
	movzwl	4(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_ntohs
	movq	-16(%rbp), %rdx
	movw	%ax, 4(%rdx)
	movq	-8(%rbp), %rax
	movzwl	6(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_ntohs
	movq	-16(%rbp), %rdx
	movw	%ax, 6(%rdx)
	movq	-8(%rbp), %rax
	movzbl	8(%rax), %edx
	movq	-16(%rbp), %rax
	movb	%dl, 8(%rax)
	movq	-8(%rbp), %rax
	movzbl	9(%rax), %edx
	movq	-16(%rbp), %rax
	movb	%dl, 9(%rax)
	movq	-8(%rbp), %rax
	movzwl	10(%rax), %edx
	movq	-16(%rbp), %rax
	movw	%dx, 10(%rax)
	movq	-8(%rbp), %rax
	movl	12(%rax), %eax
	movl	%eax, %edi
	call	sfi_ntohl
	movq	-16(%rbp), %rdx
	movl	%eax, 12(%rdx)
	movq	-8(%rbp), %rax
	movl	16(%rax), %eax
	movl	%eax, %edi
	call	sfi_ntohl
	movq	-16(%rbp), %rdx
	movl	%eax, 16(%rdx)
	movq	-16(%rbp), %rax
	movq	%rax, %rdi
	call	ip_hdr_hlen
	leave
	ret
	.size	ip_ntoh, .-ip_ntoh
	.type	ip_reply_header, @function
ip_reply_header:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$32, %rsp
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, -8(%rbp)
	movq	-8(%rbp), %rax
	movl	12(%rax), %eax
	movl	%eax, -12(%rbp)
	movq	-8(%rbp), %rax
	movl	16(%rax), %edx
	movq	-8(%rbp), %rax
	movl	%edx, 12(%rax)
	movq	-8(%rbp), %rax
	movl	-12(%rbp), %edx
	movl	%edx, 16(%rax)
	movq	-8(%rbp), %rax
	movb	$64, 8(%rax)
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	call	ip_hdr_hlen
	addq	%rax, -32(%rbp)
	movq	-32(%rbp), %rax
	movl	%eax, %edx
	movq	-8(%rbp), %rax
	movw	%dx, 2(%rax)
	movq	-8(%rbp), %rdx
	movq	-8(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	ip_hton
	movq	-32(%rbp), %rax
	leave
	ret
	.size	ip_reply_header, .-ip_reply_header
	.type	udp_hton, @function
udp_hton:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movq	-8(%rbp), %rax
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_htons
	movq	-16(%rbp), %rdx
	movw	%ax, (%rdx)
	movq	-8(%rbp), %rax
	movzwl	2(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_htons
	movq	-16(%rbp), %rdx
	movw	%ax, 2(%rdx)
	movq	-8(%rbp), %rax
	movzwl	4(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_htons
	movq	-16(%rbp), %rdx
	movw	%ax, 4(%rdx)
	nop
	leave
	ret
	.size	udp_hton, .-udp_hton
	.type	udp_ntoh, @function
udp_ntoh:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movq	-8(%rbp), %rax
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_ntohs
	movq	-16(%rbp), %rdx
	movw	%ax, (%rdx)
	movq	-8(%rbp), %rax
	movzwl	2(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_ntohs
	movq	-16(%rbp), %rdx
	movw	%ax, 2(%rdx)
	movq	-8(%rbp), %rax
	movzwl	4(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_ntohs
	movq	-16(%rbp), %rdx
	movw	%ax, 4(%rdx)
	nop
	leave
	ret
	.size	udp_ntoh, .-udp_ntoh
	.type	ether_fcs, @function
ether_fcs:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -104(%rbp)
	movq	%rsi, -112(%rbp)
	movq	-104(%rbp), %rax
	movq	%rax, -24(%rbp)
	movl	$1304293916, -96(%rbp)
	movl	$1342890616, -92(%rbp)
	movl	$1993593556, -88(%rbp)
	movl	$1801765552, -84(%rbp)
	movl	$996258700, -80(%rbp)
	movl	$651600872, -76(%rbp)
	movl	$1020740, -72(%rbp)
	movl	$498631456, -68(%rbp)
	movl	$-1610256068, -64(%rbp)
	movl	$-1112383144, -60(%rbp)
	movl	$-1687465484, -56(%rbp)
	movl	$-2032385648, -52(%rbp)
	movl	$-690409300, -48(%rbp)
	movl	$-881975096, -44(%rbp)
	movl	$-306769820, -40(%rbp)
	movl	$-268435456, -36(%rbp)
	movl	$0, -4(%rbp)
	movq	$0, -16(%rbp)
	jmp	.L74
.L75:
	movl	-4(%rbp), %eax
	shrl	$4, %eax
	movl	%eax, %ecx
	movq	-24(%rbp), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	xorl	-4(%rbp), %eax
	andl	$15, %eax
	movl	%eax, %eax
	movl	-96(%rbp,%rax,4), %eax
	xorl	%ecx, %eax
	movl	%eax, -4(%rbp)
	movl	-4(%rbp), %eax
	shrl	$4, %eax
	movl	%eax, %ecx
	movq	-24(%rbp), %rdx
	movq	-16(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	shrb	$4, %al
	movzbl	%al, %eax
	xorl	-4(%rbp), %eax
	andl	$15, %eax
	movl	%eax, %eax
	movl	-96(%rbp,%rax,4), %eax
	xorl	%ecx, %eax
	movl	%eax, -4(%rbp)
	addq	$1, -16(%rbp)
.L74:
	movq	-16(%rbp), %rax
	cmpq	-112(%rbp), %rax
	jb	.L75
	movl	-4(%rbp), %eax
	popq	%rbp
	ret
	.size	ether_fcs, .-ether_fcs
	.type	e1000_send, @function
e1000_send:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$32, %rsp
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movl	$0, %r8d
	movl	$0, %ecx
	movl	$0, %edx
	movl	$0, %esi
	movl	$1539, %edi
	call	SFI_LIBRARY_CALL
	cltq
	movq	%rax, -8(%rbp)
	movq	-8(%rbp), %rax
	movl	(%rax), %eax
	movl	%eax, -12(%rbp)
	movq	-8(%rbp), %rax
	movl	4(%rax), %eax
	movl	%eax, -16(%rbp)
	movl	-16(%rbp), %eax
	addl	$1, %eax
	movzbl	%al, %eax
	cmpl	%eax, -12(%rbp)
	je	.L78
	movl	-16(%rbp), %eax
	salq	$12, %rax
	leaq	16(%rax), %rdx
	movq	-8(%rbp), %rax
	leaq	(%rdx,%rax), %rcx
	movq	-32(%rbp), %rdx
	movq	-24(%rbp), %rax
	movq	%rax, %rsi
	movq	%rcx, %rdi
	call	sfi_memcpy
	movq	-32(%rbp), %rax
	movl	%eax, %ecx
	movq	-8(%rbp), %rax
	movl	-16(%rbp), %edx
	addq	$1048584, %rdx
	movw	%cx, (%rax,%rdx,2)
	movl	-16(%rbp), %eax
	addl	$1, %eax
	movzbl	%al, %edx
	movq	-8(%rbp), %rax
	movl	%edx, 4(%rax)
	movl	$0, %r8d
	movl	$0, %ecx
	movl	$0, %edx
	movl	$2001, %esi
	movl	$1, %edi
	call	SFI_CALL
	movq	-32(%rbp), %rax
	jmp	.L79
.L78:
	movl	$-1, %eax
.L79:
	leave
	ret
	.size	e1000_send, .-e1000_send
	.type	ether_send, @function
ether_send:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	pushq	%rbx
	subq	$152, %rsp
	movq	%rdi, -104(%rbp)
	movl	%esi, %eax
	movq	%rdx, -120(%rbp)
	movq	%rcx, -128(%rbp)
	movw	%ax, -108(%rbp)
	movq	%rsp, %rax
	movq	%rax, %rbx
	movb	$0, -78(%rbp)
	movb	$12, -77(%rbp)
	movb	$41, -76(%rbp)
	movb	$77, -75(%rbp)
	movb	$84, -74(%rbp)
	movb	$-58, -73(%rbp)
	movq	-128(%rbp), %rax
	movl	$56, %esi
	movl	%eax, %edi
	call	max
	addl	$18, %eax
	movl	%eax, %eax
	movq	%rax, -32(%rbp)
	movq	-32(%rbp), %rax
	subq	$1, %rax
	movq	%rax, -40(%rbp)
	movq	-32(%rbp), %rax
	movq	%rax, -144(%rbp)
	movq	$0, -136(%rbp)
	movq	-32(%rbp), %rax
	movq	%rax, -160(%rbp)
	movq	$0, -152(%rbp)
	movq	-32(%rbp), %rax
	leaq	8(%rax), %rdx
	movl	$16, %eax
	subq	$1, %rax
	addq	%rdx, %rax
	movl	$16, %ecx
	movl	$0, %edx
	divq	%rcx
	imulq	$16, %rax, %rax
	movq	%rax, %rdx
	andq	$-4096, %rdx
	movq	%rsp, %rsi
	subq	%rdx, %rsi
	movq	%rsi, %rdx
.L81:
	cmpq	%rdx, %rsp
	je	.L82
	subq	$4096, %rsp
	orq	$0, 4088(%rsp)
	jmp	.L81
.L82:
	movq	%rax, %rdx
	andl	$4095, %edx
	subq	%rdx, %rsp
	movq	%rax, %rdx
	andl	$4095, %edx
	testq	%rdx, %rdx
	je	.L83
	andl	$4095, %eax
	subq	$8, %rax
	addq	%rsp, %rax
	orq	$0, (%rax)
.L83:
	movq	%rsp, %rax
	addq	$15, %rax
	shrq	$4, %rax
	salq	$4, %rax
	movq	%rax, -48(%rbp)
	movq	-48(%rbp), %rax
	addq	$14, %rax
	movq	%rax, -56(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, -64(%rbp)
	movq	-32(%rbp), %rax
	leaq	-4(%rax), %rdx
	movq	-48(%rbp), %rax
	addq	%rdx, %rax
	movq	%rax, -72(%rbp)
	cmpq	$0, -120(%rbp)
	setne	%al
	movzbl	%al, %eax
	movl	$89478485, %r8d
	movl	$89478485, %ecx
	movl	$0, %edx
	movl	%eax, %esi
	movl	$1570, %edi
	call	SFI_LIBRARY_CALL
	cmpq	$1518, -32(%rbp)
	jbe	.L84
	movl	$-90, -20(%rbp)
	jmp	.L85
.L84:
	movq	-64(%rbp), %rax
	movq	-104(%rbp), %rcx
	movl	$6, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	sfi_memcpy
	movq	-64(%rbp), %rax
	leaq	6(%rax), %rcx
	leaq	-78(%rbp), %rax
	movl	$6, %edx
	movq	%rax, %rsi
	movq	%rcx, %rdi
	call	sfi_memcpy
	movzwl	-108(%rbp), %eax
	movl	%eax, %edi
	call	sfi_htons
	movq	-64(%rbp), %rdx
	movw	%ax, 12(%rdx)
	movq	-128(%rbp), %rdx
	movq	-120(%rbp), %rcx
	movq	-56(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	sfi_memcpy
	movq	-32(%rbp), %rax
	movl	%eax, %edx
	movq	-128(%rbp), %rax
	subl	%eax, %edx
	movl	%edx, %eax
	subl	$14, %eax
	movl	%eax, %ecx
	movq	-56(%rbp), %rdx
	movq	-128(%rbp), %rax
	addq	%rdx, %rax
	movl	%ecx, %edx
	movl	$0, %esi
	movq	%rax, %rdi
	call	my_memset
	movq	-32(%rbp), %rax
	leaq	-4(%rax), %rdx
	movq	-48(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	ether_fcs
	movl	%eax, -84(%rbp)
	leaq	-84(%rbp), %rcx
	movq	-72(%rbp), %rax
	movl	$4, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	sfi_memcpy
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	dump_pkt
	movq	-32(%rbp), %rdx
	movq	-48(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	e1000_send
	movl	%eax, -20(%rbp)
.L85:
	movl	-20(%rbp), %eax
	movq	%rbx, %rsp
	movq	-8(%rbp), %rbx
	leave
	ret
	.size	ether_send, .-ether_send
	.type	ip_send, @function
ip_send:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	pushq	%rbx
	subq	$120, %rsp
	movl	%edi, -100(%rbp)
	movl	%esi, %eax
	movq	%rdx, -112(%rbp)
	movq	%rcx, -120(%rbp)
	movb	%al, -104(%rbp)
	movq	%rsp, %rax
	movq	%rax, -128(%rbp)
	movq	-120(%rbp), %rax
	addq	$20, %rax
	movq	%rax, -24(%rbp)
	movl	$167772162, -28(%rbp)
	movb	$0, -82(%rbp)
	movb	$12, -81(%rbp)
	movb	$41, -80(%rbp)
	movb	$77, -79(%rbp)
	movb	$84, -78(%rbp)
	movb	$-68, -77(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, %rdx
	subq	$1, %rdx
	movq	%rdx, -40(%rbp)
	movq	%rax, %r10
	movl	$0, %r11d
	movq	%rax, %r8
	movl	$0, %r9d
	movl	$16, %edx
	subq	$1, %rdx
	addq	%rdx, %rax
	movl	$16, %ebx
	movl	$0, %edx
	divq	%rbx
	imulq	$16, %rax, %rax
	movq	%rax, %rdx
	andq	$-4096, %rdx
	movq	%rsp, %rbx
	subq	%rdx, %rbx
	movq	%rbx, %rdx
.L88:
	cmpq	%rdx, %rsp
	je	.L89
	subq	$4096, %rsp
	orq	$0, 4088(%rsp)
	jmp	.L88
.L89:
	movq	%rax, %rdx
	andl	$4095, %edx
	subq	%rdx, %rsp
	movq	%rax, %rdx
	andl	$4095, %edx
	testq	%rdx, %rdx
	je	.L90
	andl	$4095, %eax
	subq	$8, %rax
	addq	%rsp, %rax
	orq	$0, (%rax)
.L90:
	movq	%rsp, %rax
	addq	$0, %rax
	movq	%rax, -48(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, -56(%rbp)
	movq	-56(%rbp), %rax
	movl	$20, %edx
	leaq	ip_hdr_template(%rip), %rsi
	movq	%rax, %rdi
	call	sfi_memcpy
	movq	-24(%rbp), %rax
	movl	%eax, %edx
	movq	-56(%rbp), %rax
	movw	%dx, 2(%rax)
	movl	ip_global_id(%rip), %eax
	leal	1(%rax), %edx
	movl	%edx, ip_global_id(%rip)
	movl	%eax, %edx
	movq	-56(%rbp), %rax
	movw	%dx, 4(%rax)
	movq	-56(%rbp), %rax
	movl	-28(%rbp), %edx
	movl	%edx, 12(%rax)
	movq	-56(%rbp), %rax
	movl	-100(%rbp), %edx
	movl	%edx, 16(%rax)
	movq	-56(%rbp), %rax
	movzbl	-104(%rbp), %edx
	movb	%dl, 9(%rax)
	cmpb	$17, -104(%rbp)
	jne	.L91
	movq	-112(%rbp), %rax
	movq	%rax, -64(%rbp)
	movq	-64(%rbp), %rax
	movzwl	4(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, -68(%rbp)
	movq	-64(%rbp), %rax
	movzwl	6(%rax), %eax
	testw	%ax, %ax
	sete	%al
	movzbl	%al, %eax
	movl	$89478485, %r8d
	movl	$89478485, %ecx
	movl	$0, %edx
	movl	%eax, %esi
	movl	$1570, %edi
	call	SFI_LIBRARY_CALL
	movq	-64(%rbp), %rdx
	movq	-64(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	udp_hton
	movq	-56(%rbp), %rax
	movl	16(%rax), %eax
	movl	%eax, %edi
	call	sfi_htonl
	movl	%eax, %ebx
	movq	-56(%rbp), %rax
	movl	12(%rax), %eax
	movl	%eax, %edi
	call	sfi_htonl
	movl	%eax, %edx
	movl	-68(%rbp), %eax
	movslq	%eax, %rsi
	movq	-64(%rbp), %rax
	movl	%ebx, %ecx
	movq	%rax, %rdi
	call	udp_checksum
	movzwl	%ax, %eax
	movl	%eax, -72(%rbp)
	movl	-72(%rbp), %eax
	movl	%eax, %edx
	movq	-64(%rbp), %rax
	movw	%dx, 6(%rax)
	movq	-56(%rbp), %rax
	movl	16(%rax), %eax
	movl	%eax, %edi
	call	sfi_htonl
	movl	%eax, %ebx
	movq	-56(%rbp), %rax
	movl	12(%rax), %eax
	movl	%eax, %edi
	call	sfi_htonl
	movl	%eax, %edx
	movl	-68(%rbp), %eax
	movslq	%eax, %rsi
	movq	-64(%rbp), %rax
	movl	%ebx, %ecx
	movq	%rax, %rdi
	call	udp_checksum
	movzwl	%ax, %eax
	movl	%eax, -72(%rbp)
	cmpl	$0, -72(%rbp)
	je	.L91
	movl	$-1, %eax
	jmp	.L92
.L91:
	movq	-48(%rbp), %rax
	leaq	20(%rax), %rcx
	movq	-120(%rbp), %rdx
	movq	-112(%rbp), %rax
	movq	%rax, %rsi
	movq	%rcx, %rdi
	call	sfi_memcpy
	movq	-56(%rbp), %rdx
	movq	-56(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	ip_hton
	cmpq	$1500, -120(%rbp)
	setbe	%al
	movzbl	%al, %eax
	movl	$89478485, %r8d
	movl	$89478485, %ecx
	movl	$0, %edx
	movl	%eax, %esi
	movl	$1570, %edi
	call	SFI_LIBRARY_CALL
	movq	-24(%rbp), %rcx
	movq	-48(%rbp), %rdx
	leaq	-82(%rbp), %rax
	movl	$2048, %esi
	movq	%rax, %rdi
	call	ether_send
	movl	%eax, -76(%rbp)
	movl	-76(%rbp), %eax
.L92:
	movq	-128(%rbp), %rsp
	movq	-8(%rbp), %rbx
	leave
	ret
	.size	ip_send, .-ip_send
	.type	nstack_udp_send, @function
nstack_udp_send:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	pushq	%rbx
	subq	$56, %rsp
	movq	%rdi, -56(%rbp)
	movq	%rsi, -64(%rbp)
	movq	%rsp, %rax
	movq	%rax, %rbx
	movq	-64(%rbp), %rax
	movq	16(%rax), %rax
	addq	$7, %rax
	movq	%rax, -24(%rbp)
	movq	-64(%rbp), %rax
	movq	16(%rax), %rax
	addq	$8, %rax
	movq	%rax, %r10
	movl	$0, %r11d
	movq	-64(%rbp), %rax
	movq	16(%rax), %rax
	addq	$8, %rax
	movq	%rax, %r8
	movl	$0, %r9d
	movq	-64(%rbp), %rax
	movq	16(%rax), %rax
	leaq	8(%rax), %rdx
	movl	$16, %eax
	subq	$1, %rax
	addq	%rdx, %rax
	movl	$16, %edi
	movl	$0, %edx
	divq	%rdi
	imulq	$16, %rax, %rax
	movq	%rax, %rdx
	andq	$-4096, %rdx
	movq	%rsp, %rsi
	subq	%rdx, %rsi
	movq	%rsi, %rdx
.L95:
	cmpq	%rdx, %rsp
	je	.L96
	subq	$4096, %rsp
	orq	$0, 4088(%rsp)
	jmp	.L95
.L96:
	movq	%rax, %rdx
	andl	$4095, %edx
	subq	%rdx, %rsp
	movq	%rax, %rdx
	andl	$4095, %edx
	testq	%rdx, %rdx
	je	.L97
	andl	$4095, %eax
	subq	$8, %rax
	addq	%rsp, %rax
	orq	$0, (%rax)
.L97:
	movq	%rsp, %rax
	addq	$0, %rax
	movq	%rax, -32(%rbp)
	movq	-32(%rbp), %rax
	movq	%rax, -40(%rbp)
	movq	-40(%rbp), %rax
	addq	$8, %rax
	movq	%rax, -48(%rbp)
	movq	-64(%rbp), %rax
	movq	16(%rax), %rax
	testq	%rax, %rax
	je	.L98
	movq	-64(%rbp), %rax
	movq	16(%rax), %rax
	cmpq	$65506, %rax
	jbe	.L99
.L98:
	movl	$-22, %eax
	jmp	.L100
.L99:
	movq	-56(%rbp), %rax
	movl	16(%rax), %eax
	movl	%eax, %edx
	movq	-40(%rbp), %rax
	movw	%dx, (%rax)
	movq	-64(%rbp), %rax
	movl	12(%rax), %eax
	movl	%eax, %edx
	movq	-40(%rbp), %rax
	movw	%dx, 2(%rax)
	movq	-64(%rbp), %rax
	movq	16(%rax), %rax
	leal	8(%rax), %edx
	movq	-40(%rbp), %rax
	movw	%dx, 4(%rax)
	movq	-40(%rbp), %rax
	movw	$0, 6(%rax)
	movq	-64(%rbp), %rax
	movq	16(%rax), %rdx
	movq	-64(%rbp), %rax
	leaq	24(%rax), %rcx
	movq	-48(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	sfi_memcpy
	movq	-64(%rbp), %rax
	movq	16(%rax), %rax
	leaq	8(%rax), %rcx
	movq	-64(%rbp), %rax
	movl	8(%rax), %eax
	movq	-32(%rbp), %rdx
	movl	$17, %esi
	movl	%eax, %edi
	call	ip_send
.L100:
	movq	%rbx, %rsp
	movq	-8(%rbp), %rbx
	leave
	ret
	.size	nstack_udp_send, .-nstack_udp_send
	.globl	nstack_egress
	.type	nstack_egress, @function
nstack_egress:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$64, %rsp
	movl	%edi, -36(%rbp)
	movq	%rsi, -48(%rbp)
	movq	%rdx, -56(%rbp)
	movl	$0, %r8d
	movl	$0, %ecx
	movl	$0, %edx
	movl	$0, %esi
	movl	$1538, %edi
	call	SFI_LIBRARY_CALL
	cltq
	movq	%rax, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	56(%rax), %rax
	movq	%rax, %rdi
	call	queue_isempty
	testl	%eax, %eax
	jne	.L103
	nop
.L104:
	movq	-8(%rbp), %rax
	movq	56(%rax), %rax
	leaq	-20(%rbp), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	queue_peek
	xorl	$1, %eax
	testb	%al, %al
	jne	.L104
	movq	-8(%rbp), %rax
	movq	48(%rax), %rdx
	movl	-20(%rbp), %eax
	cltq
	addq	%rdx, %rax
	movq	%rax, -16(%rbp)
	movq	-8(%rbp), %rax
	movl	8(%rax), %eax
	cmpl	$2, %eax
	jne	.L105
	movq	-16(%rbp), %rdx
	movq	-8(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	nstack_udp_send
.L105:
	movq	-8(%rbp), %rax
	movq	56(%rax), %rax
	movl	$1, %esi
	movq	%rax, %rdi
	call	queue_discard
.L103:
	movl	$0, %eax
	leave
	ret
	.size	nstack_egress, .-nstack_egress
	.type	e1000_receive, @function
e1000_receive:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$32, %rsp
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movl	$0, %r8d
	movl	$0, %ecx
	movl	$0, %edx
	movl	$0, %esi
	movl	$1539, %edi
	call	SFI_LIBRARY_CALL
	cltq
	movq	%rax, -8(%rbp)
	movq	-8(%rbp), %rax
	movl	8(%rax), %eax
	movl	%eax, -12(%rbp)
	movq	-8(%rbp), %rax
	movl	12(%rax), %eax
	movl	%eax, -16(%rbp)
	movl	-12(%rbp), %eax
	cmpl	-16(%rbp), %eax
	jne	.L108
	movq	-32(%rbp), %rdx
	movq	-8(%rbp), %rax
	movl	2098192(%rax), %eax
	movq	%rdx, %r8
	movl	$0, %ecx
	movl	%eax, %edx
	movl	$2001, %esi
	movl	$2, %edi
	call	SFI_CALL
	movl	%eax, %edx
	movq	-8(%rbp), %rax
	movl	%edx, 2098192(%rax)
	movq	-8(%rbp), %rax
	movl	8(%rax), %edx
	movq	-8(%rbp), %rax
	movl	12(%rax), %eax
	cmpl	%eax, %edx
	setne	%al
	movzbl	%al, %eax
	movl	$89478485, %r8d
	movl	$89478485, %ecx
	movl	$0, %edx
	movl	%eax, %esi
	movl	$1570, %edi
	call	SFI_LIBRARY_CALL
.L108:
	movq	-8(%rbp), %rax
	movl	8(%rax), %eax
	movl	%eax, -12(%rbp)
	movq	-8(%rbp), %rax
	movl	12(%rax), %eax
	movl	%eax, -16(%rbp)
	movq	-8(%rbp), %rax
	movl	-12(%rbp), %edx
	addq	$1048840, %rdx
	movzwl	(%rax,%rdx,2), %eax
	testw	%ax, %ax
	setne	%al
	movzbl	%al, %eax
	movl	$89478485, %r8d
	movl	$89478485, %ecx
	movl	$0, %edx
	movl	%eax, %esi
	movl	$1570, %edi
	call	SFI_LIBRARY_CALL
	movq	-8(%rbp), %rax
	movl	-12(%rbp), %edx
	addq	$1048840, %rdx
	movzwl	(%rax,%rdx,2), %eax
	movzwl	%ax, %eax
	movq	%rax, -32(%rbp)
	movq	-32(%rbp), %rdx
	movl	-12(%rbp), %eax
	salq	$12, %rax
	leaq	1048592(%rax), %rcx
	movq	-8(%rbp), %rax
	addq	%rax, %rcx
	movq	-24(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	sfi_memcpy
	movq	-8(%rbp), %rax
	movl	-12(%rbp), %edx
	addq	$1048840, %rdx
	movw	$0, (%rax,%rdx,2)
	movl	-12(%rbp), %eax
	addl	$1, %eax
	movzbl	%al, %edx
	movq	-8(%rbp), %rax
	movl	%edx, 8(%rax)
	movq	-32(%rbp), %rax
	leave
	ret
	.size	e1000_receive, .-e1000_receive
	.type	ether_receive, @function
ether_receive:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$1584, %rsp
	movq	%rdi, -1560(%rbp)
	movq	%rsi, -1568(%rbp)
	movq	%rdx, -1576(%rbp)
	leaq	-1536(%rbp), %rax
	movq	%rax, -8(%rbp)
	movb	$0, -1542(%rbp)
	movb	$12, -1541(%rbp)
	movb	$41, -1540(%rbp)
	movb	$77, -1539(%rbp)
	movb	$84, -1538(%rbp)
	movb	$-58, -1537(%rbp)
	cmpq	$0, -1560(%rbp)
	setne	%al
	movzbl	%al, %eax
	movl	$89478485, %r8d
	movl	$89478485, %ecx
	movl	$0, %edx
	movl	%eax, %esi
	movl	$1570, %edi
	call	SFI_LIBRARY_CALL
	cmpq	$0, -1568(%rbp)
	setne	%al
	movzbl	%al, %eax
	movl	$89478485, %r8d
	movl	$89478485, %ecx
	movl	$0, %edx
	movl	%eax, %esi
	movl	$1570, %edi
	call	SFI_LIBRARY_CALL
.L113:
	leaq	-1536(%rbp), %rax
	movl	$1514, %esi
	movq	%rax, %rdi
	call	e1000_receive
	movl	%eax, -12(%rbp)
	cmpl	$-1, -12(%rbp)
	jne	.L111
	movl	$-1, %eax
	jmp	.L114
.L111:
	movq	-8(%rbp), %rax
	leaq	6(%rax), %rcx
	leaq	-1542(%rbp), %rax
	movl	$6, %edx
	movq	%rax, %rsi
	movq	%rcx, %rdi
	call	sfi_memcmp
	testl	%eax, %eax
	je	.L113
	leaq	-1536(%rbp), %rax
	movq	%rax, %rdi
	call	dump_pkt
	movq	-8(%rbp), %rcx
	movq	-1560(%rbp), %rax
	movl	$6, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	sfi_memcpy
	movq	-8(%rbp), %rax
	leaq	6(%rax), %rcx
	movq	-1560(%rbp), %rax
	addq	$6, %rax
	movl	$6, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	sfi_memcpy
	movq	-8(%rbp), %rax
	movzwl	12(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, %edi
	call	sfi_ntohs
	movq	-1560(%rbp), %rdx
	movw	%ax, 12(%rdx)
	subl	$14, -12(%rbp)
	movq	-1576(%rbp), %rax
	movl	%eax, %edx
	movl	-12(%rbp), %eax
	movl	%edx, %esi
	movl	%eax, %edi
	call	min
	movl	%eax, %edx
	leaq	-1536(%rbp), %rax
	addq	$14, %rax
	movq	-1568(%rbp), %rcx
	movq	%rax, %rsi
	movq	%rcx, %rdi
	call	sfi_memcpy
	movl	-12(%rbp), %eax
.L114:
	leave
	ret
	.size	ether_receive, .-ether_receive
	.type	nstack_sock_dgram_input, @function
nstack_sock_dgram_input:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$48, %rsp
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movq	%rdx, -40(%rbp)
	movq	%rcx, -48(%rbp)
	nop
.L116:
	movq	-24(%rbp), %rax
	movq	40(%rax), %rax
	movq	%rax, %rdi
	call	queue_alloc
	movl	%eax, -4(%rbp)
	cmpl	$-1, -4(%rbp)
	je	.L116
	movq	-24(%rbp), %rax
	movq	32(%rax), %rdx
	movl	-4(%rbp), %eax
	cltq
	addq	%rdx, %rax
	movq	%rax, -16(%rbp)
	movq	-16(%rbp), %rax
	movq	-32(%rbp), %rdx
	movq	(%rdx), %rdx
	movq	%rdx, (%rax)
	movq	-16(%rbp), %rax
	movq	-24(%rbp), %rdx
	movq	12(%rdx), %rdx
	movq	%rdx, 8(%rax)
	movq	-16(%rbp), %rax
	movq	-48(%rbp), %rdx
	movq	%rdx, 16(%rax)
	movq	-16(%rbp), %rax
	leaq	24(%rax), %rcx
	movq	-48(%rbp), %rdx
	movq	-40(%rbp), %rax
	movq	%rax, %rsi
	movq	%rcx, %rdi
	call	sfi_memcpy
	movq	-24(%rbp), %rax
	movq	40(%rax), %rax
	movq	%rax, %rdi
	call	queue_commit
	movl	$0, %eax
	leave
	ret
	.size	nstack_sock_dgram_input, .-nstack_sock_dgram_input
	.type	udp_input, @function
udp_input:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$72, %rsp
	movq	%rdi, -56(%rbp)
	movq	%rsi, -64(%rbp)
	movq	%rdx, -72(%rbp)
	movq	-64(%rbp), %rax
	movq	%rax, -8(%rbp)
	movl	$0, %r8d
	movl	$0, %ecx
	movl	$0, %edx
	movl	$0, %esi
	movl	$1538, %edi
	call	SFI_LIBRARY_CALL
	cltq
	movq	%rax, -16(%rbp)
	cmpq	$0, -16(%rbp)
	setne	%al
	movzbl	%al, %eax
	movl	$89478485, %r8d
	movl	$89478485, %ecx
	movl	$0, %edx
	movl	%eax, %esi
	movl	$1570, %edi
	call	SFI_LIBRARY_CALL
	cmpq	$7, -72(%rbp)
	ja	.L119
	movl	$-74, %eax
	jmp	.L121
.L119:
	movq	-8(%rbp), %rdx
	movq	-8(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	udp_ntoh
	movq	-56(%rbp), %rax
	movl	16(%rax), %eax
	movl	%eax, -28(%rbp)
	movq	-8(%rbp), %rax
	movzwl	2(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, -24(%rbp)
	movq	-56(%rbp), %rax
	movl	12(%rax), %eax
	movl	%eax, -36(%rbp)
	movq	-8(%rbp), %rax
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	movl	%eax, -32(%rbp)
	movq	-72(%rbp), %rax
	leaq	-8(%rax), %rcx
	movq	-64(%rbp), %rax
	leaq	8(%rax), %rdx
	leaq	-36(%rbp), %rsi
	movq	-16(%rbp), %rax
	movq	%rax, %rdi
	call	nstack_sock_dgram_input
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %eax
.L121:
	leave
	ret
	.size	udp_input, .-udp_input
	.type	ip_input, @function
ip_input:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$56, %rsp
	movq	%rdi, -40(%rbp)
	movq	%rsi, -48(%rbp)
	movq	%rdx, -56(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, -16(%rbp)
	cmpq	$0, -40(%rbp)
	je	.L123
	movq	-16(%rbp), %rdx
	movq	-16(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	ip_ntoh
.L123:
	movq	-16(%rbp), %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	andl	$64, %eax
	testl	%eax, %eax
	jne	.L124
	movl	$0, %eax
	jmp	.L125
.L124:
	movq	-16(%rbp), %rax
	movq	%rax, %rdi
	call	ip_hdr_hlen
	movq	%rax, -24(%rbp)
	cmpq	$19, -24(%rbp)
	ja	.L126
	movl	$0, %eax
	jmp	.L125
.L126:
	cmpq	$46, -56(%rbp)
	jbe	.L127
	movq	-16(%rbp), %rax
	movzwl	2(%rax), %eax
	movzwl	%ax, %eax
	cmpq	%rax, -56(%rbp)
	jne	.L128
.L127:
	movq	-16(%rbp), %rax
	movzwl	2(%rax), %eax
	movzwl	%ax, %eax
	cmpq	%rax, -56(%rbp)
	jnb	.L129
.L128:
	movl	$0, %eax
	jmp	.L125
.L129:
	movq	-16(%rbp), %rax
	movzbl	9(%rax), %eax
	cmpb	$17, %al
	jne	.L130
	movq	-56(%rbp), %rax
	subq	-24(%rbp), %rax
	movq	%rax, %rdx
	movq	-48(%rbp), %rcx
	movq	-24(%rbp), %rax
	addq	%rax, %rcx
	movq	-16(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	udp_input
	movl	%eax, -4(%rbp)
	cmpl	$0, -4(%rbp)
	jle	.L131
	movl	-4(%rbp), %eax
	movslq	%eax, %rdx
	movq	-16(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	ip_reply_header
	movl	%eax, -4(%rbp)
.L131:
	movl	-4(%rbp), %eax
	jmp	.L125
.L130:
	movl	$-1, %eax
.L125:
	leave
	ret
	.size	ip_input, .-ip_input
	.type	ether_input, @function
ether_input:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$40, %rsp
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movq	%rdx, -40(%rbp)
	movq	-40(%rbp), %rdx
	movq	-32(%rbp), %rcx
	movq	-24(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	ip_input
	movl	%eax, -4(%rbp)
	cmpl	$0, -4(%rbp)
	jns	.L133
	movl	$-1, -4(%rbp)
.L133:
	movl	-4(%rbp), %eax
	leave
	ret
	.size	ether_input, .-ether_input
	.type	ether_output_reply, @function
ether_output_reply:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$48, %rsp
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movq	%rdx, -40(%rbp)
	movq	-24(%rbp), %rax
	movzwl	12(%rax), %eax
	movzwl	%ax, %eax
	movq	-24(%rbp), %rdx
	leaq	6(%rdx), %rdi
	movq	-40(%rbp), %rcx
	movq	-32(%rbp), %rdx
	movl	%eax, %esi
	call	ether_send
	movl	%eax, -4(%rbp)
	cmpl	$0, -4(%rbp)
	jns	.L136
	movl	$-1, -4(%rbp)
.L136:
	movl	-4(%rbp), %eax
	leave
	ret
	.size	ether_output_reply, .-ether_output_reply
	.globl	nstack_ingress
	.type	nstack_ingress, @function
nstack_ingress:
	endbr64
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$64, %rsp
	movl	%edi, -36(%rbp)
	movq	%rsi, -48(%rbp)
	movq	%rdx, -56(%rbp)
	leaq	-18(%rbp), %rax
	movl	$1514, %edx
	leaq	rx_buffer.5380(%rip), %rsi
	movq	%rax, %rdi
	call	ether_receive
	movl	%eax, -4(%rbp)
	cmpl	$-1, -4(%rbp)
	je	.L139
	cmpl	$0, -4(%rbp)
	jle	.L139
	movl	-4(%rbp), %eax
	movslq	%eax, %rdx
	leaq	-18(%rbp), %rax
	leaq	rx_buffer.5380(%rip), %rsi
	movq	%rax, %rdi
	call	ether_input
	movl	%eax, -4(%rbp)
.L139:
	movl	-4(%rbp), %eax
	leave
	ret
	.size	nstack_ingress, .-nstack_ingress
	.local	rx_buffer.5380
	.comm	rx_buffer.5380,1514,32
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
