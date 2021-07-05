# python 
from keystone import *

from ins_struct import *
from utilities import *

ks = Ks(KS_ARCH_X86, KS_MODE_64)
ks.syntax = KS_OPT_SYNTAX_ATT

def struct_lable(ins_str,att_s):
    att_s.Itype = 1
    att_s.operand_size =  1
    att_s.op = ins_str
    return att_s

def struct_annotation(ins_str,att_s):
    att_s.Itype = 2
    att_s.operand_size =  1
    att_s.op = ins_str
    return att_s

def struct_instruction_1(ins_str,att_s):  # single operand 
    att_s.Itype = 3
    att_s.operand_size =  1
    att_s.op = ins_str
    return att_s

def struct_instruction_2(ins_str,att_s): #  multi operand
    """
    op_data Dtype 
    op_data -> 'Segment-Overwrite:': S_offset: (base: index: scale)
    Dtype   ->        0x        1      1        1      1     1 

    """
    op = ins_str.split("\t")[0]
    op_data = ins_str.split("\t")[1]
    att_s.Itype = 3
    att_s.operand_size =  3
    att_s.op = op
    per = ""
    access_memory =  False
    if_base = False
    if_index = False
    finish_src = False
    dst_start = False
    Dtype = 0
    for i, c in enumerate(op_data):
        if "(" != c or "," != c or ":" != c or ")" != c:
            per += c
            if i == len(op_data) -1:
                op_dst = OP_DATA()
                op_dst.segment_override = segment_override
                op_dst.s_offset = s_offset
                op_dst.base = base
                op_dst.index = index
                op_dst.scale = scale
                op_dst.Dtype = Dtype
        elif c == ":":
            segment_override = per
            Dtype = 0x10000 | Dtype
            per = ""
        elif c == "(":
            access_memory = True
            s_offset  = per
            Dtype = 0x01000 | Dtype
            per = ""
        elif c == "," and access_memory == True:
            if_base = True
            base = per
            Dtype = 0x00100 | Dtype
            per  =""
        elif c == "," and if_base == True:
            assert access_memory == True
            if_index = True
            if_base = False
            index = per 
            Dtype = 0x00010 | Dtype
            per = ""
        elif c == ")" and if_index == True:
            assert access_memory == True
            scale =  per
            Dtype = 0x00001 | Dtype
            per = ""
            access_memory == False
            if_index = False
            finish_src = True
            if i == len(op_data) -1 :
                op_dst = OP_DATA()
                op_dst.segment_override = segment_override
                op_dst.s_offset = s_offset
                op_dst.base = base
                op_dst.index = index
                op_dst.scale = scale
                op_dst.Dtype = Dtype
        elif (c == "," and finish_src == True and dst_start == False) or ( c == "," and  dst_start == False) :
            op_src = OP_DATA()
            op_src.segment_override = segment_override
            op_src.s_offset = s_offset
            op_src.base = base
            op_src.index = index
            op_src.scale = scale
            op_src.Dtype = Dtype
            Dtype = 0
            per = ""
            dst_start == True
        elif c == "," and finish_src == True and dst_start == True:
            op_dst = OP_DATA()
            op_dst.segment_override = segment_override
            op_dst.s_offset = s_offset
            op_dst.base = base
            op_dst.index = index
            op_dst.scale = scale
            op_dst.Dtype = Dtype
    att_s.source = op_src
    att_s.destination = op_dst
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
            # TODO
        else:
            print("[+]: unknow instruction : "+ ins_str)
    else:
        print("[+]: unknow instruction : "+ ins_str)


def add_align(as_data):
    global ks
    ret = []
    align = 32
    for data in as_data:
        s_line = data.strip()
        if len(s_line) == 0:
            ret.append(data)
            continue
        if s_line[0] == '.': # annotation
            if ".align" in data:
                continue
            ret.append(data)
            continue
        if s_line[-1] == ':': # lable
            ret.append("\t.align 32")
            ret.append(data)
            align = 32
            continue
        else:
            log("add_align --> " + data)
            if "endbr" in data[:6]:  # deal with endbra64 and endbra32 keystone can't solve
                hard_code = [90]*4
                count = 1
            else:
                try:
                    hard_code,count = ks.asm(data)  # ks.asm return truple such as.([90,90],1L)
                except keystone.KsError as err:
                    log(err)
                    print "[+]: "+data+"--> asm error amd I default using jmp lable: 7 byte code"
                    hard_code = [90]*7
                    count = 1 
            assert count == 1
            align -= len(hard_code)
            if align < 0:
                align += len(hard_code)
                assert align >= 0
                ret.append("\t.align 32")
                align =  32-len(hard_code)
                ret.append(data)
            else:
                ret.append(data)
        
    return ret