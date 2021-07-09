# python 
from utilities import expand_list
from ins_struct import *
from build_struct import make_struct
from define import *

DEBUG = False

op_list = ["push", "mov", "add", "cmp", "jmp", "sub", "mul", "div", "rcp", "sqrt", "rsqrt", "lea", "call", "load", ""]

def reg_swtich_low(reg):
    reg_low_table = {"%rax":"%eax","%rbx":"%ebx","%rcx":"%ecx","%rdx":"%edx","%rsi":"%esi","%rdi":"%edi","%rbp":"%ebp","%rsp":"%esp","%r8":"%r8d","%r9":"%r9d","%r10":"%r10d","%r11":"%r11d","%r12":"%r12d","%r13":"%r13d","%r14":"%r14d","%r15":"%r15d"}
    reg = reg.strip()
    return reg_low_table[reg]

# def memory_confine_base(op_data:OP_DATA):
def memory_confine_base(op_data:OP_DATA):
    # print(op_data)

    # !!! in special deal with mov lable(%rip), %reg
    if "rip" in str(op_data):
        return [op_data]
    dst_dtype =  op_data.get_Dtype()
    if dst_dtype == 0x00100 or dst_dtype == 0x01100:   # also solve 0x01000
        base = op_data.base
        s = "mov \t" + reg_swtich_low(base) + ", " + reg_swtich_low(base)
        op_data.base = "%r13"
        op_data.index = base
        return [ s, op_data ]
    else:
        base = op_data.base
        s = "lea \t" + str(op_data) +", " + base
        s2 = "mov \t" + reg_swtich_low(base) + ", " + reg_swtich_low(base)
        ret_op_data = OP_DATA()
        ret_op_data.base = "%r13"
        ret_op_data.index = base
        ret_op_data.scale = "1"
        return [s, s2, ret_op_data]
        
def memory_confine_REGMEM(att:ATT_Syntax):
    dst_data =  att.destination
    dst_data:OP_DATA
    ret_data = memory_confine_base(dst_data)
    att.destination = ret_data[-1]
    ret_data = ret_data[:-1]
    ret_att = []
    for s in ret_data:
        ret_att.append(make_struct(s))
    ret_att.append(att)
    return ret_att

def memory_confine_MEMREG(att:ATT_Syntax):
    src_data =  att.source
    src_data:OP_DATA
    ret_data = memory_confine_base(src_data)
    att.source = ret_data[-1]
    ret_data = ret_data[:-1]
    ret_att = []
    for s in ret_data:
        ret_att.append(make_struct(s))
    ret_att.append(att)
    return ret_att

def memory_confine_MEMMEM(att:ATT_Syntax):
    src_data =  att.source
    src_data:OP_DATA
    ret_data = memory_confine_base(src_data)
    att.source = ret_data[-1]
    ret_data = ret_data[:-1]
    ret_att = []
    for s in ret_data:
        ret_att.append(make_struct(s))
    dst_data =  att.destination
    dst_data:OP_DATA
    ret_data = memory_confine_base(dst_data)
    att.destination = ret_data[-1] 
    ret_data = ret_data[:-1]
    for s in ret_data:
        ret_att.append(make_struct(s))
    ret_att.append(att)
    return ret_att
    
def memory_confine_MEM(att:ATT_Syntax):
    att_list = memory_confine_MEMREG(att)
    return att_list

def memory_confine_IMEREG(att:ATT_Syntax):
    return att

def jmpaddress_confine(att:ATT_Syntax):
    if att.DataType == OPDMEM:
        att_add_1 = make_struct("movl\t"+str(att.source).replace('*','')+", %edi")
    else:
        att_add_1 = make_struct("mov\t"+str(att.source.base).replace('*','')+", %edi")
    att_add_2 = make_struct("andl\t$0xffffffe0, %edi")
    att_add_3 = make_struct("addq\t%r13, %rdi")
    att_add_4 = make_struct("jmp \t*%rdi")
    return [att_add_1, att_add_2, att_add_3, att_add_4]

def add_sfi_main(att_list):
    global OPDIMEREG,IINSTR,ILABEL,OPDREGMEM,OPDMEMMEM,OPDMEM,OPDMEMREG,OPDLABLE
    confin_fun = {
        OPDREGMEM : memory_confine_REGMEM,
        OPDMEMREG : memory_confine_MEMREG,
        OPDMEMMEM : memory_confine_MEMMEM,
        OPDMEM    : memory_confine_MEM,
        OPDIMEREG : memory_confine_IMEREG,
        OPDLABLE  : jmpaddress_confine
    }

    # how to solve lea:ISA 
    for index,att in enumerate(att_list):
        att:ATT_Syntax
        if att.Itype == IINSTR and att.operand_size != 1:
            if att.DataType in [OPDREG , OPDREGREG , OPDIMEREG , OPDLABLE]:
                continue
            # ！！！
            # 
            #  special deal with leaq	.sfi_lable0(%rip),  %rax
            if "lea" in att.op and att.DataType is OPDMEMREG:
                continue
            
            att_list[index] = confin_fun[att.DataType](att)

    att_list =  expand_list(att_list)

    for index,att in enumerate(att_list):
        att:ATT_Syntax
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
    align = 32
    for att in att_list:
        att:ATT_Syntax
        if att.Itype == ILABEL:
            ret_att.append(make_struct(".align 32"))
            ret_att.append(att)
            align =  32
            continue
        c_size = att.get_opcode_size()
        align -= c_size
        if align < 0:
            align += c_size
            assert align >= 0
            ret_att.append(make_struct(".align 32"))
            align =  32 - c_size
            ret_att.append(att)
        else:
            ret_att.append(att)
        
    return ret_att

