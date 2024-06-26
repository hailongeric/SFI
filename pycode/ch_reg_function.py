#! /usr/bin/python3
from build_struct import make_struct
from assem_struct import *
from utilities import *
from define import SFI_ADD_LABLE_NUM


# def replace_stack_reg(s):
#     """
#     # rbp --> r14
#     # rsp --> r15
#     # arg s: string --> read input file convert string
#     # return string --> string after solve ch_rg 
#     """

#     s = s.replace("%rsp","%r15")
#     s = s.replace("%rbp","%r14")
#     s = s.replace("%spl","%r15b")
#     s = s.replace("%bpl","%r14b")
#     s = s.replace("%sp","%r15w")
#     s = s.replace("%bp","%r14w")
#     s = s.replace("%esp","%r15d")
#     s = s.replace("%ebp","%r14d")
#     return s

def replace_stack_reg(s):
    """
    # rsp --> r15
    # arg s: string --> read input file convert string
    # return string --> string after solve ch_rg 
    """
    s = s.replace("%rsp","%r15")
    s = s.replace("%spl","%r15b")
    s = s.replace("%sp","%r15w")
    s = s.replace("%esp","%r15d")
    return s



def assign_orig_str(att_list, orignal_str,att=None):
    for index in range(len(att_list)):
        att_list[index].orignal_str = orignal_str
        if att is not None:
            att_list[index].fdm = att.fdm
    return att_list

def assign_sfi_stack(att_list):
    for index in range(len(att_list)):
        att_list[index].sfi_stack = False
    return att_list

def ch_syscall(att:ATTASM):
    """
    s = s.replace("syscall\n",
    "subq\t$8, %r15\n
    \tlea \t.sfi_lable2{}(%rip), %rbx\n
    \tmovq\t%rbx, (%r15)\n
    \tret\n
    .sfi_lable2{}:
    \n".format(SFI_ADD_LABLE_NUM,SFI_ADD_LABLE_NUM))
    """
    global SFI_ADD_LABLE_NUM

    orignal_str = att.orignal_str
    att_add_0 = make_struct("lea\t-8(%r15), %r15")
    att_add_0.sfi_stack =  False
    att_add_1 = make_struct("lea \t.sfi_lable{}(%rip), %r12".format(SFI_ADD_LABLE_NUM))
    att_add_1.sfi_stack =  False
    att_add_2 = make_struct("movq\t%r12, (%r15)")
    att_add_3 = make_struct("ret")
    att_add_4 = make_struct(".sfi_lable{}:".format(SFI_ADD_LABLE_NUM))
    SFI_ADD_LABLE_NUM += 1
    return assign_orig_str([att_add_0, att_add_1, att_add_2, att_add_3, att_add_4], orignal_str,att)


def ch_push(att:ATTASM):
    """
    # modify push instruction
    # arg s: a line string --> need to modify
    # return ins: string list --> after add some sfi
    """
    orignal_str = att.orignal_str
    att_add = make_struct("lea \t-8(%r15), %r15")
    # s_add = "subq\t$8, %r15"
    s = att.assem_str
    s = s.replace('push','mov')
    s += ", 0(%r15)"
    att = make_struct(s)
    att_add.sfi_stack = False
    att.sfi_stack = False
    return assign_orig_str([att_add, att],orignal_str,att)

    
def ch_pop(att:ATTASM):
    """
    # modify pop instruction
    # arg s: a line string --> need to modify
    # return ins: string list --> after add some sfi
    """
    orignal_str = att.orignal_str
    s = att.assem_str
    s = s.replace('pop','mov')
    s = s.split('\t')
    s[1]  = "0(%r15), "+s[1]
    s = "\t".join(s)
    att = make_struct(s)
    # s_add = "addq\t$8, %r15"
    att_add = make_struct("lea \t8(%r15), %r15")
    att.sfi_stack = False
    att_add.sfi_stack = False
    return assign_orig_str([att, att_add], orignal_str,att)

def ch_ret(att:ATTASM):
    """
    # modify ret instruction
    # arg string : "ret"
    # return ins: string list --> after add some sfi
    """
    orignal_str = att.orignal_str
    att_add = make_struct("lea \t8(%r15), %r15")
    att_add.sfi_stack = False
    att = make_struct("jmp \t*-8(%r15)")
    return assign_orig_str([att_add, att],orignal_str,att)

def ch_call(att:ATTASM):
    """
    # modify call instruction
    # arg string : a line str --> call instrcution string
    # return ins: string list --> after add some sfi
    """
    orignal_str = att.orignal_str
    att_add =make_struct("lea \t-8(%r15), %r15")
    global SFI_ADD_LABLE_NUM
    # s_add_1 ="movq    %rip, (%r15)"
    # !!! using r12 register
    att_add_1 =make_struct("leaq\t.sfi_lable{}(%rip), %r12".format(SFI_ADD_LABLE_NUM))
    # att_add_2 = make_struct("addq\t$12, %rax")
    att_add_2 = make_struct("movq\t%r12, (%r15)")
    # !!! here is error, call calloc@PLT is bad
    
    s = att.assem_str.replace("call","jmp *",1) 
    att = make_struct(s)
    att_add_3 = make_struct(".sfi_lable{}:".format(SFI_ADD_LABLE_NUM))
    SFI_ADD_LABLE_NUM += 1
    att_add.sfi_stack = False
    att_add_1.sfi_stack = False
    att_add_2.sfi_stack = False
    return assign_orig_str([att_add,att_add_1,att_add_2,att,att_add_3],orignal_str,att)

def ch_leave(att:ATTASM):
    """
    # modify leave instruction
    # arg string : a line str --> "leave" instrcution string
    # return ins: string list --> after add some sfi
    """
    orignal_str = att.orignal_str
    assert att.assem_str == "leave"
    att_add = make_struct("movq\t%r14, %r15")
    att_add_1 = make_struct("movq\t(%r15), %r14")
    att_add_2 = make_struct("lea \t8(%r15), %r15")
    att_add.sfi_stack = False
    #!!! att_add_1 must be add sfi movl r14d,r14d, 
    att_add_2.sfi_stack = False
    return assign_orig_str([att_add, att_add_1, att_add_2], orignal_str,att)

def handle_special_ass(att_list):

    for index,att in enumerate(att_list):
        if att.Itype == IINSTR:
            # !!! must place syscall at the head of call 
            # don't using 'in' and use 'is' maybe bad code compatibile

            if "syscall" in att.op:
                att_list[index] = ch_syscall(att)
            elif "push" in  att.op:
                att_list[index] = ch_push(att)
            elif "pop" in att.op:
                att_list[index] = ch_pop(att)
            elif "ret" in att.op:
                att_list[index] = ch_ret(att)
            elif "call" in att.op:
                att_list[index] = ch_call(att)
            # elif "leave" in att.op:
            #     att_list[index] = ch_leave(att)
    att_list = expand_list(att_list)
    return att_list
