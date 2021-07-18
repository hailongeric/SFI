# python 

from assem_struct import *
from utilities import *
from define import *


def struct_lable(ins_str,att_s:ATTASM):
    att_s.assem_str = ins_str
    att_s.Itype = ILABEL
    att_s.operand_size =  1
    att_s.op = ins_str
    return att_s

def struct_annotation(ins_str,att_s:ATTASM):
    att_s.assem_str = ins_str
    att_s.Itype = IANNOT
    att_s.operand_size =  1
    att_s.op = ins_str
    return att_s

def struct_instruction_no_operand(ins_str,att_s:ATTASM):  # single operand 
    att_s.assem_str = ins_str
    att_s.Itype = IINSTR
    att_s.operand_size =  1
    att_s.op = ins_str
    return att_s

def struct_instruction_operand(ins_str,att_s:ATTASM): #  multi operand
    # TODO add some it is 2 op_size
    """
    op_data Dtype 
    op_data -> 'Segment-Overwrite:': S_offset: (base: index: scale)
    Dtype   ->        0x        1      1        1      1     1 

    """
    # op = ins_str.split("\t")[0]
    # op_data = ins_str.split("\t")[1]
    op,op_data = split_op_opdata(ins_str)
    # log("error+ op " + op + " opdata --> " +op_data)

    att_s.assem_str = ins_str
    att_s.Itype = IINSTR
    att_s.op = op

    # TODO deal with jmp lable
    if "%" not in op_data:
        att_s.jmp_lable = op_data
        att_s.operand_size = 2
        att_s.DataType = OPDLABLE
        return att_s

    op_data = split_op_data(op_data)
    # log("opdata list --> "+str(op_data))
    #assert len(op_data) == 2
    op_data_struct = []
    access_memory = []
    if len(op_data) == 1:
        att_s.operand_size = 2
        single_data = split_single_op_data(op_data[0])  # debug this function error
        assert len(single_data) == 6
        opd = OPD(single_data[0],single_data[1],single_data[2],single_data[3],single_data[4])
        opd.accesss_memory = single_data[5]
        att_s.src_opd = opd
        if opd.accesss_memory:
            att_s.DataType = OPDMEM
        else:
            att_s.DataType = OPDREG

    elif len(op_data) == 2:
        att_s.operand_size = 3
        for data in op_data:
            single_data = split_single_op_data(data)  # debug this function error
            # print(single_data)
            assert len(single_data) == 6
            opd = OPD(single_data[0],single_data[1],single_data[2],single_data[3],single_data[4])
            opd.accesss_memory = single_data[5]
            access_memory.append(single_data[5])
            op_data_struct.append(opd)
        att_s.src_opd = op_data_struct[0]
        att_s.dst_opd = op_data_struct[1]
        if True not in access_memory:
            if "%" not in op_data[0]:
                att_s.DataType = OPDIMEREG
            else:
                att_s.DataType = OPDREGREG
        elif False not in access_memory:
            att_s.DataType = OPDMEMMEM
        elif access_memory[0] == True:
            att_s.DataType = OPDMEMREG
        else:
            att_s.DataType = OPDREGMEM

    elif len(op_data) == 3:
        att_s.operand_size = 4
        for data in op_data:
            single_data = split_single_op_data(data)  # debug this function error
            # print(single_data)
            assert len(single_data) == 6
            opd = OPD(single_data[0],single_data[1],single_data[2],single_data[3],single_data[4])
            opd.accesss_memory = single_data[5]
            access_memory.append(single_data[5])
            op_data_struct.append(opd)

        att_s.src_opd = op_data_struct[0]
        att_s.dst_opd = op_data_struct[1]
        att_s.third_opd = op_data_struct[2]
        if True not in access_memory:
            if "%" not in op_data[0]:
                att_s.DataType = OPDIMEREGREG
            elif "%" not in op_data[1]:
                att_s.DataType = OPDREGIMEREG
            else:
                att_s.DataType = OPDREGREGREG
                # print("[!!!] error three operand variant and the first variant isn't ime")
        elif access_memory[1] == True :
            att_s.DataType = OPDIMEMEMREG
        else:
            print("[!!!] error three operand variant and the first variant isn't ime")
    # print("[DEBUG]:  struct_instruction_operand " + ins_str)
    return att_s

def make_struct(ins_str):
    #self.count += 1
    att_s =  ATTASM()
    ins_str = ins_str.strip()

    if len(ins_str) == 0:
        return None

    if ins_str[0] == "." and ins_str[-1] != ":":
            return struct_annotation(ins_str, att_s) # annotation type 2
    if ins_str[0] == "#":
            return struct_annotation(ins_str, att_s) # annotation type 2
    if ins_str[-1] == ":" and ins_str[0] != "#":
            return struct_lable(ins_str, att_s) # lable type 1

    # TODO split need myfunction :  no compatibility
    ins_list = ins_str.split('\t')
    ins_len = len(ins_list)
    if ins_len == 1:
        #!!! no tab as separative sign
        if "%" not in ins_str:
            return struct_instruction_no_operand(ins_str, att_s) # instruction type 3
        else:
            return struct_instruction_operand(ins_str,att_s)

    if ins_len == 2:
        if ins_list[0][0] != "." and ins_list[0][0] != "#":
            # log(ins_list)
            return struct_instruction_operand(ins_str,att_s)
        else:
            print("[+]: unknow instruction : "+ ins_str)
    else:
        print("[+]: unknow instruction : "+ ins_str)
    return None

def trans_str(att_list):
    s = []
    for att in att_list:
        att:ATTASM
        if att == None:
            continue
        if att.Itype == IANNOT and att.op[0] == '#':
            s.append(att.assem_str)
        elif att.Itype != ILABEL:
            s.append("\t" + att.assem_str)
        else:
            s.append(att.assem_str)
    return '\n'.join(s)


def init_asm(s_list:list):
    att_list = []
    asm_att:ATTASM
    for ins in s_list:
        asm_att = make_struct(ins)
        if asm_att is None:
            continue
        asm_att.orignal_str = ins
        att_list.append(asm_att)
    return att_list