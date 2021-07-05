# python 
from ins_struct import *


def replace_stack_reg(s):
    # rbp --> r14
    # rsp --> r15
    # arg s: string --> read input file convert string
    # return string --> string after solve ch_rg 
    s = s.replace("%rsp","%r15")
    s = s.replace("%rbp","%r14")
    s = s.replace("%spl","%r15b")
    s = s.replace("%bpl","%r14b")
    s = s.replace("%sp","%r15w")
    s = s.replace("%bp","%r14w")
    s = s.replace("%esp","%r15d")
    s = s.replace("%ebp","%r14d")
    return s

def ch_push(s):
    # modify push instruction
    # arg s: a line string --> need to modify
    # return ins: string list --> after add some sfi
    s_add = "subq\t$8, %r15"
    s = s.replace('push','mov')
    s += ", 0(%r15)"
    return ['\t'+s_add, '\t'+s]

def ch_pop(s):
    # modify pop instruction
    # arg s: a line string --> need to modify
    # return ins: string list --> after add some sfi
    s = s.replace('pop','mov')
    s = s.split('\t')
    s[1]  = "0(%r15), "+s[1]
    s = "\t".join(s)
    s_add = "addq\t$8, %r15"
    return ['\t'+s, '\t'+s_add]

def ch_ret(s):
    # modify ret instruction
    # arg string : "ret"
    # return ins: string list --> after add some sfi
    s_add = "addq\t$8, %r15"
    s = "jmp\t*-8(%r15)"
    return ['\t'+s_add, '\t'+s]

def ch_call(s):
    # modify call instruction
    # arg string : a line str --> call instrcution string
    # return ins: string list --> after add some sfi
    s_add ="subq\t$8, %r15"
    # s_add_1 ="movq    %rip, (%r15)"
    s_add_1 ="lea\t0(%rip), %rax"
    s_add_2 = "addq\t$12, %rax"
    s_add_3 ="movq\t%rax, (%r15)"
    s = s.replace("call","jmp *")
    return ['\t'+s_add,'\t'+s_add_1,'\t'+s_add_2,'\t'+s_add_3,'\t'+s]

def ch_leave(s):
    # modify leave instruction
    # arg string : a line str --> "leave" instrcution string
    # return ins: string list --> after add some sfi
    assert s == "leave"
    s_add = "movq\t%r14, %r15"
    s_add_1 = "movq\t(%r15), %r14"
    s_add_2 = "addq\t$8, %r15"
    return ['\t'+s_add, '\t'+s_add_1, '\t'+s_add_2]
