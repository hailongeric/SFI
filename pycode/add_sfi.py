# python 
from typing import Optional
from ch_reg_function import assign_orig_str
from utilities import expand_list, Fdebug
from assem_struct import *
from build_struct import make_struct
from define import *

DEBUG = False


op_list = ["push", "mov", "add", "cmp", "jmp", "sub", "mul", "div", "rcp", "sqrt", "rsqrt", "lea", "call", "load", ""]
special_op = ["aaa"]

def reg_swtich_low(reg):
    reg_low_table = {"%rax":"%eax","%rbx":"%ebx","%rcx":"%ecx","%rdx":"%edx","%rsi":"%esi","%rdi":"%edi","%rbp":"%ebp","%rsp":"%esp","%r8":"%r8d","%r9":"%r9d","%r10":"%r10d","%r11":"%r11d","%r12":"%r12d","%r13":"%r13d","%r14":"%r14d","%r15":"%r15d"}
    reg = reg.strip()
    return reg_low_table[reg]

def op_switch_low(op):
    op =op.strip()
    if op[-1] == 'q':
        if op not in special_op:
            op = op[:-1]+'l'
        else:
            op = "happy"
    return op

# TODO this may be avoid memory
def is_stack_op(att:ATTASM):
    if "r14" in str(att.dst_opd) or "r15" in str(att.dst_opd):
        return True
    else:
        return False

# def memory_confine_base(op_data:OP_DATA):
def memory_confine_base(op_data:OPD, tmp_reg="%r12"):

    # !!! in special deal with mov lable(%rip), %reg
    if "rip" in str(op_data):
        return [op_data]
    dst_dtype =  op_data.get_Dtype()

    if dst_dtype == 0x00100 or dst_dtype == 0x01100:   # also solve 0x01000
        base = op_data.base
        if "r14" in base or "r15" in base:
            return [op_data]
        s = "mov \t" + reg_swtich_low(base) + ", " + reg_swtich_low(base)
        op_data.base = "%r13"
        op_data.index = base
        # !!! in special  solve push and pop rsp rbp check 
        return [s, op_data ]
        
    else:
        base = op_data.base
        # TODO judge if stack register

        # if "r14" in base or "r15" in base:
        #     if "%" in op_data.index:
        #         base = op_data.index
        s = "lea \t" + str(op_data) +", " + tmp_reg

        s2 = "mov \t" + reg_swtich_low(tmp_reg) + ", " + reg_swtich_low(tmp_reg)
        ret_op_data = OPD()
        ret_op_data.base = "%r13"
        ret_op_data.index = tmp_reg
        ret_op_data.scale = "1"
        ret_op_data.accesss_memory = True
        # !!! in special  solve push and pop rsp rbp check 
        # unnecessary checking 

        # if "r14" in s or "r15" in s:
        #     return [s, ret_op_data]
        # else:
        return [s, s2, ret_op_data]
        
def memory_confine_REGMEM(att:ATTASM):
    dst_data =  att.dst_opd
    dst_data:OPD
    ret_data = memory_confine_base(dst_data)
    att.dst_opd = ret_data[-1]
    ret_data = ret_data[:-1]
    ret_att = []
    for s in ret_data:
        ret_att.append(make_struct(s))
    ret_att.append(att)
    return assign_orig_str(ret_att, att.orignal_str)

def memory_confine_MEMREG(att:ATTASM):
    if is_stack_op(att):
        return confinemnet_stack_point(att)
    src_data =  att.src_opd
    src_data:OPD

    ret_data = memory_confine_base(src_data)
    att.src_opd = ret_data[-1]
    ret_data = ret_data[:-1]
    ret_att = []
    for s in ret_data:
        ret_att.append(make_struct(s))
    ret_att.append(att)
    return assign_orig_str(ret_att, att.orignal_str)

def memory_confine_MEMMEM(att:ATTASM):
    src_data =  att.src_opd
    src_data:OPD
    ret_data = memory_confine_base(src_data)
    att.src_opd = ret_data[-1]
    ret_data = ret_data[:-1]
    ret_att = []
    for s in ret_data:
        ret_att.append(make_struct(s))
    dst_data =  att.dst_opd
    dst_data:OPD
    ret_data = memory_confine_base(dst_data)
    att.dst_opd = ret_data[-1] 
    ret_data = ret_data[:-1]
    for s in ret_data:
        ret_att.append(make_struct(s))
    ret_att.append(att)
    return assign_orig_str(ret_att,att.orignal_str)
    
def memory_confine_MEM(att:ATTASM):
    att_list = memory_confine_MEMREG(att)
    return att_list

def memory_confine_IMEREG(att:ATTASM):
    return att

def memory_confine_IMEMEMREG(att:ATTASM):
    return memory_confine_REGMEM(att)

def jmpaddress_confine(att:ATTASM):
    Fdebug("jmpaddress_confine:--> " +str(att.src_opd))
    if att.DataType == OPDMEM:
        att_add_1 = make_struct("movl\t"+str(att.src_opd).replace('*','')+", %edi")
    else:
        att_add_1 = make_struct("mov\t"+str(att.src_opd.base).replace('*','')+", %edi")
    # att_add_2 = make_struct("andl\t$0xffffffe0, %edi")
    att_add_2= make_struct("mov \t$5, %esi")
    att_add_2_1 = make_struct("shrx\t%esi, %edi, %edi")
    att_add_2_2 = make_struct("shlx\t%esi, %edi, %edi")
    att_add_3 = make_struct("lea \t(%r13, %rdi, 1), %rdi")
    att_add_4 = make_struct("jmp \t*%rdi")
    return assign_orig_str([att_add_1, att_add_2, att_add_2_1, att_add_2_2, att_add_3, att_add_4], att.orignal_str)

def confinemnet_stack_point(att:ATTASM):
    # MEMREG OR REGEREG
    if att.DataType == OPDREGREG:
        if "r14" in str(att.src_opd) or "r15" in str(att.src_opd):
            return att
        else:
            att_add = make_struct(op_switch_low(att.op)+"\t"+reg_swtich_low(att.src_opd.base)+", "+reg_swtich_low(att.dst_opd.base))
            att_add_1 = make_struct("lea \t(%r13, {}, 1), {}".format(att.dst_opd.base,att.dst_opd.base))
    elif att.DataType == OPDIMEREG:
        att_add = make_struct(op_switch_low(att.op)+"\t" + att.src_opd.base + ", "+reg_swtich_low(att.dst_opd.base))
        att_add_1 = make_struct("lea \t(%r13, {}, 1), {}".format(att.dst_opd.base,att.dst_opd.base))
    else:
        att_add = make_struct(op_switch_low(att.op)+'\t'+str(att.src_opd)+", "+ reg_swtich_low(att.dst_opd.base))
        att_add_1 = make_struct("lea \t(%r13, {}, 1), {}".format(att.dst_opd.base,att.dst_opd.base))
    return assign_orig_str([att_add, att_add_1], att.orignal_str)

def confinement_rep_ins(att:ATTASM):
    att_add_1 = make_struct("mov \t%esi, %esi")
    att_add_2 = make_struct("mov \t%edi, %edi")
    att_add_3 = make_struct("lea \t(%r13, %rsi), %rsi")
    att_add_4 = make_struct("lea \t(%r13, %rdi), %rdi")
    return assign_orig_str([att_add_1, att_add_2, att_add_3, att_add_4, att], att.orignal_str)


def avoid_stack(att:ATTASM):
    if att.dst_opd.Dtype == 0x01100 and ("r14" in att.dst_opd.base or "r15" in  att.dst_opd.base):
        return True
    if att.src_opd.Dtype == 0x01100 and ("r14" in att.src_opd.base or "r15" in  att.src_opd.base):
        return True
    return False

def add_sfi_main(att_list):
    global OPDIMEREG,IINSTR,ILABEL,OPDREGMEM,OPDMEMMEM,OPDMEM,OPDMEMREG,OPDLABLE
    confin_fun = {
        OPDREGMEM : memory_confine_REGMEM,
        OPDMEMREG : memory_confine_MEMREG,
        OPDMEMMEM : memory_confine_MEMMEM,
        OPDMEM    : memory_confine_MEM,
        OPDIMEREG : memory_confine_IMEREG,
        OPDIMEMEMREG: memory_confine_IMEMEMREG,
        OPDLABLE  : jmpaddress_confine
    }

    # how to solve lea:ISA 
    for index,att in enumerate(att_list):
        att:ATTASM
        # print(att)
        # !!! add confinement rsp rbp as r14 r15 
        if att.sfi_stack == False:
            continue

        # !!! in special handle rep operation
        if len(re.findall(r'\w\w\ws[bwd]',att.assem_str))!=0:
             att_list[index] = confinement_rep_ins(att)
             continue

        if att.Itype == IINSTR and att.operand_size != 1:
            if att.DataType in [OPDREG , OPDREGREG , OPDIMEREG , OPDLABLE, OPDIMEREGREG]:
                if is_stack_op(att):
                    att_list[index] = confinemnet_stack_point(att)
                continue
            # ！！！
            # 
            #  special deal with leaq	.sfi_lable0(%rip),  %rax
            if "lea" in att.op and att.DataType is OPDMEMREG:
                continue
            if avoid_stack(att):
                continue
            att_list[index] = confin_fun[att.DataType](att)

    att_list =  expand_list(att_list)

    for index,att in enumerate(att_list):
        att:ATTASM
        if att.Itype == IINSTR and "jmp" in att.op and att.DataType != OPDLABLE :
            att_list[index] = jmpaddress_confine(att)

    att_list = expand_list(att_list)
    ret_att = []
    for att in att_list:
        att.update_str()
        ret_att.append(att)

    # print([str(i) for i in ret_att])
    return ret_att
    

def add_align(att_list):
    ret_att = []
    op_size = []
    tmp_att = []
    align = 32
    tmp_align = 0
    tmp_str = ""
    for att in att_list:
        att:ATTASM
        if att.Itype == ILABEL:
            ret_att.append(tmp_att)
            op_size.append(tmp_align)
            tmp_att= []
            tmp_align = 0
            ret_att.append(att)
            op_size.append(32)
        else:
            if tmp_str != att.orignal_str:
                ret_att.append(tmp_att)
                op_size.append(tmp_align)
                tmp_att= [att]
                tmp_str = att.orignal_str
                tmp_align = att.get_opcode_size()
            else:
                tmp_att.append(att)
                tmp_align += att.get_opcode_size()

    ret_att.append(tmp_att)
    op_size.append(tmp_align)

    assert len(ret_att) == len(op_size)
    tmp_att = ret_att
    Fdebug(op_size)
    ret_att = []
    for size,att in zip(op_size,tmp_att):
        if size == 32:
            ret_att.append((make_struct(".align 32")))
            align = 32
        else:
            align -= size
            if align < 0:
                align += size
                assert align >= 0
                ret_att.append(make_struct(".align 32"))
                align =  32 - size
        ret_att.append(att)
    ret_att = expand_list(ret_att)
    return ret_att

