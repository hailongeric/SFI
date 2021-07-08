#! /usr/bin/python3
from build_struct import make_struct
from ins_struct import *
from utilities import *
from define import SFI_ADD_LABLE_NUM


def replace_stack_reg(s):
    """
    # rbp --> r14
    # rsp --> r15
    # arg s: string --> read input file convert string
    # return string --> string after solve ch_rg 
    """

    s = s.replace("%rsp","%r15")
    s = s.replace("%rbp","%r14")
    s = s.replace("%spl","%r15b")
    s = s.replace("%bpl","%r14b")
    s = s.replace("%sp","%r15w")
    s = s.replace("%bp","%r14w")
    s = s.replace("%esp","%r15d")
    s = s.replace("%ebp","%r14d")
    return s

def ch_push(att:ATT_Syntax):
    """
    # modify push instruction
    # arg s: a line string --> need to modify
    # return ins: string list --> after add some sfi
    """

    att_add = make_struct("subq\t$8, %r15")
    # s_add = "subq\t$8, %r15"
    s = att.ori_str
    s = s.replace('push','mov')
    s += ", 0(%r15)"
    att = make_struct(s)
    return [att_add, att]

    
def ch_pop(att:ATT_Syntax):
    """
    # modify pop instruction
    # arg s: a line string --> need to modify
    # return ins: string list --> after add some sfi
    """

    s = att.ori_str
    s = s.replace('pop','mov')
    s = s.split('\t')
    s[1]  = "0(%r15), "+s[1]
    s = "\t".join(s)
    att = make_struct(s)
    # s_add = "addq\t$8, %r15"
    att_add = make_struct("addq\t$8, %r15")
    return [att, att_add]

def ch_ret(att:ATT_Syntax):
    """
    # modify ret instruction
    # arg string : "ret"
    # return ins: string list --> after add some sfi
    """

    att_add = make_struct("addq\t$8, %r15")
    att = make_struct("jmp \t*-8(%r15)")
    return [att_add, att]

def ch_call(att:ATT_Syntax):
    """
    # modify call instruction
    # arg string : a line str --> call instrcution string
    # return ins: string list --> after add some sfi
    """

    att_add =make_struct("subq\t$8, %r15")
    global SFI_ADD_LABLE_NUM
    # s_add_1 ="movq    %rip, (%r15)"
    att_add_1 =make_struct("leaq\t.sfi_lable{}(%rip), %rax".format(SFI_ADD_LABLE_NUM))
    # att_add_2 = make_struct("addq\t$12, %rax")
    att_add_2 = make_struct("movq\t%rax, (%r15)")
    s = att.ori_str.replace("call","jmp *")
    att = make_struct(s)
    att_add_3 = make_struct(".sfi_lable{}:".format(SFI_ADD_LABLE_NUM))
    SFI_ADD_LABLE_NUM += 1
    return [att_add,att_add_1,att_add_2,att,att_add_3]

def ch_leave(att:ATT_Syntax):
    """
    # modify leave instruction
    # arg string : a line str --> "leave" instrcution string
    # return ins: string list --> after add some sfi
    """

    assert att.ori_str == "leave"
    att_add = make_struct("movq\t%r14, %r15")
    att_add_1 = make_struct("movq\t(%r15), %r14")
    att_add_2 = make_struct("addq\t$8, %r15")
    return [att_add, att_add_1, att_add_2]

def solve_jump_ins_main(att_list):

    for index,att in enumerate(att_list):
        if att.Itype == 3:
            if "push" in  att.op:
                att_list[index] = ch_push(att)
            elif "pop" in att.op:
                att_list[index] = ch_pop(att)
            elif "ret" in att.op:
                att_list[index] = ch_ret(att)
            elif "call" in att.op:
                att_list[index] = ch_call(att)
            elif "leave" in att.op:
                att_list[index] = ch_leave(att)
    att_list = expand_list(att_list)
    return att_list
