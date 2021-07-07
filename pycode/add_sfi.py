# python 

from utilities import expand_list
from ins_struct import *
from build_struct import make_struct

DEBUG = False

op_list = ["push", "mov", "add", "cmp", "jmp", "sub", "mul", "div", "rcp", "sqrt", "rsqrt", "lea", "call", "load", ""]

def reg_swtich_low(reg):
    reg_low_table = {"%rax":"%eax","%rbx":"%ebx","%rcx":"%ecx","%rdx":"%edx","%rsi":"%esi","%rdi":"%edi","%rbp":"%ebp","%rsp":"%esp","%r8":"%r8d","%r9":"%r9d","%r10":"%r10d","%r11":"%r11d","%r12":"%r12d","%r13":"%r13d","%r14":"%r14d","%r15":"%r15d"}
    reg = reg.strip()
    return reg_low_table[reg]

def if_in(op_list,op):
    for i_op in op_list:
        if i_op in op:
            return True
    
    return False

def add_memory_confine(ins_data):
    ret = []
    split_data = ins_data.strip()
    split_data = split_data.split("\t")
    op = split_data[0]
    assert len(split_data) > 1
    op_data = split_data[1]
    op_data = op_data.split(',')  # TODO can't solve op (%rax, %rax, 1), %eax
    op_src = op_data[0]
    op_dst = op_data[1]
    src_mem = re.findall(r"\d*\(.*\)",op_src)
    if src_mem != None:
        if re.findall(r"\d+\(",op_src) != None:  # is disp32 offset ?
            offset = re.findall(r"\d+\(",op_src)[0][:-1]
        else:
            offset = "0"
        reg = re.findall(r"\(\%.*\)",op_src)[0][1:-1]
        # TODO reg_list = reg.split(',')  support  (%rax, %rax, 1)
        if "r" in reg:  # is 64-bit reg ?
            add_ins_0 = "mov\t"+ reg +", " + reg_swtich_low(reg)
            add_ins_1 = op+"\t"+offset+"(%r13, " + reg +", 1)"
            return [add_ins_0, add_ins_1]
        else:
            return ins_data

    dst_mem = re.findall(r"\d*\(.*\)",op_dst)
    # the same as above
    if dst_mem != None:
        if re.findall(r"\d+\(",op_dst) != None:  # is disp32 offset ?
            offset = re.findall(r"\d+\(",op_dst)[0][:-1]
        else:
            offset = "0"
        reg = re.findall(r"\(\%.*\)",op_dst)[0][1:-1]
        # TODO reg_list = reg.split(',')  support  (%rax, %rax, 1)
        if "r" in reg:  # is 64-bit reg ?
            add_ins_0 = "mov\t"+ reg +", " + reg_swtich_low(reg)
            add_ins_1 = op+"\t"+offset+"(%r13, " + reg +", 1)"
            return [add_ins_0, add_ins_1]
        else:
            return ins_data

def add_address_confinement(ins_data):
    # TODO
    split_data = ins_data.strip()
    split_data = split_data.split("\t" )
    if "%" in split_data[1]:
        add_ins = "and\t0xffffffe0, "+split_data[1]
        return 

def add_confinement(instruction_data):
    ret = []
    for data in instruction_data:
        split_data = data.strip()
        split_data = split_data.split("\t")
        op = split_data[0]
        if op in [".file", ".text", ".type", ".size", ".ident", ".section", ".data", ".align", ".long"]:
            ret.append(data)
        elif op in ["endbr64","endbr32"]:
            ret.append(data)
        elif "mov" in op:
            ret.append(add_memory_confine(data))
        elif "add" in op:
            ret.append(add_memory_confine(data))
        elif "jmp" in op:
            ret.append(add_address_confinement(data))

    return ret

# def memory_confine_base(op_data:OP_DATA):
def memory_confine_base(op_data):
    dst_dtype =  op_data.get_Dtype()
    if dst_dtype == 0x00100 or dst_dtype == 0x01100:   # also solve 0x01000
        base = op_data.base
        s = "mov\t" + reg_swtich_low(base) + ", " + reg_swtich_low(base)
        op_data.base = "%r13"
        op_data.index = base
        return [ s, op_data ]
    else:
        base = op_data.base
        s = "lea\t" + str(op_data) +", " + base
        s2 = "mov\t" + reg_swtich_low(base) + ", " + reg_swtich_low(base)
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
    return memory_confine_MEMREG(att)

def memory_confine_IMEREG(att:ATT_Syntax):
    return att

def add_sfi_main(att_list):
    confin_fun = {
        OPDREGMEM : memory_confine_REGMEM,
        OPDMEMREG : memory_confine_MEMREG,
        OPDMEMMEM : memory_confine_MEMMEM,
        OPDMEM    : memory_confine_MEM,
        OPDIMEREG : memory_confine_IMEREG
    }
    for index,att in enumerate(att_list):
        att:ATT_Syntax
        if att.Itype == 3:
            if att.DataType == OPDREG or att.DataType == OPDREGREG or att.DataType == OPDIMEREG:
                continue
            att_list[index] = confin_fun[att.DataType](att)
        if att.Itype == 2:
            if "jmp" in att.opp:
                
    return expand_list(att_list)
