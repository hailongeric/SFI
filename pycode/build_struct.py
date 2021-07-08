# python 

from ins_struct import *
from utilities import *
from define import *


def struct_lable(ins_str,att_s):
    att_s.ori_str = ins_str
    att_s.Itype = ILABEL
    att_s.operand_size =  1
    att_s.op = ins_str
    return att_s

def struct_annotation(ins_str,att_s):
    att_s.ori_str = ins_str
    att_s.Itype = IANNOT
    att_s.operand_size =  1
    att_s.op = ins_str
    return att_s

def struct_instruction_1(ins_str,att_s):  # single operand 
    att_s.ori_str = ins_str
    att_s.Itype = IINSTR
    att_s.operand_size =  1
    att_s.op = ins_str
    return att_s

def struct_instruction_2(ins_str,att_s:OP_DATA): #  multi operand
    # TODO add some it is 2 op_size
    """
    op_data Dtype 
    op_data -> 'Segment-Overwrite:': S_offset: (base: index: scale)
    Dtype   ->        0x        1      1        1      1     1 

    """
    op = ins_str.split("\t")[0]
    op_data = ins_str.split("\t")[1]

    att_s.ori_str = ins_str
    att_s.Itype = IINSTR
    att_s.op = op

    # TODO deal with jmp lable
    if "%" not in op_data:
        att_s.jmp_lable = op_data
        att_s.operand_size = 2
        att_s.DataType = OPDLABLE
        return att_s

    op_data = split_op_data(op_data)
    assert len(op_data) == 2

    if len(op_data[1]) == 0:
        att_s.operand_size = 2
        op_data = op_data[:1]
    else:
        att_s.operand_size = 3
    
    op_data_struct = []
    access_memory = []
    for data in op_data:
        single_data = split_single_op_data(data)  # debug this function error
        print(single_data)
        assert len(single_data) == 6
        temp = OP_DATA(single_data[0],single_data[1],single_data[2],single_data[3],single_data[4])
        access_memory.append(single_data[5])
        op_data_struct.append(temp)

    att_s.source = op_data_struct[0]
    if att_s.operand_size == 2:
        if True not in access_memory:
            att_s.DataType = OPDREG
        else:
            att_s.DataType = OPDMEM
    else:
        att_s.destination = op_data_struct[1]
        if True not in access_memory:
            att_s.DataType = OPDREGREG
        elif False not in access_memory:
            att_s.DataType = OPDMEMMEM
        elif access_memory[0] == True:
            att_s.DataType = OPDMEMREG
        else:
            att_s.DataType = OPDREGMEM
    return att_s

def make_struct(ins_str):
    #self.count += 1
    att_s =  ATT_Syntax()
    ins_str = ins_str.strip()
    ins_list = ins_str.split('\t')
    ins_len = len(ins_list)

    if len(ins_str) == 0:
        return None
    if ins_str[0] == "." and ins_str[-1] != ":":
            return struct_annotation(ins_str, att_s) # annotation type 2

    if ins_len == 1:
        if ins_str[-1] == ":" and ins_str[0] != "#":
            return struct_lable(ins_str, att_s) # lable type 1
        else:
            return struct_instruction_1(ins_str, att_s) # instruction type 3

    if ins_len == 2:
        if ins_list[0][0] != "." and ins_list[0][0] != "#":
            log(ins_list)
            return struct_instruction_2(ins_str,att_s)
        else:
            print("[+]: unknow instruction : "+ ins_str)
    else:
        print("[+]: unknow instruction : "+ ins_str)
    return None

def trans_str(att_list):
    s = []
    for att in att_list:
        att:ATT_Syntax
        if att == None:
            continue
        if att.Itype != ILABEL:
            s.append("\t" + att.ori_str)
        else:
            s.append(att.ori_str)
    return '\n'.join(s)

