from assem_struct import *
from define import *
# test xor orl
SET_FLAG_OP = ["add","and","cmp","div","imu","mul", "neg","sca","sub","clc","rol","ror","tes","xor","orl"]
USE_FLAG_OP = ["set","cmo"]

def init_cfg(att_list):
    for att in att_list:
        att:ATTASM
        if att.Itype != IINSTR:
            continue 
        op = att.op
        op = op.strip()
        # jmp jle gl
        if op[0] == 'j': 
            if op == "jmp":
                att.fdm.flag_use = FUNUSE
            else:
                att.fdm.flag_use = FUSE  
        elif op[0:3] in SET_FLAG_OP:
            att.fdm.flag_use = FSET
        elif op[0:3] in USE_FLAG_OP:
            att.fdm.flag_use = FUSE
        else:
            att.fdm.flag_use = FUNUSE
    return att_list

def add_cfg_info(att_list):
    size = len(att_list)
    att_list = att_list[::-1]
    flag_block = False
    for index,att in enumerate(att_list):
        att:ATTASM
        if att.fdm.flag_use == FUSE:
            flag_block = True
            att_list[index].fdm.flag_block = 3
        elif flag_block and att.fdm.flag_use != FSET:
            att_list[index].fdm.flag_block = 2
        elif flag_block and att.fdm.flag_use == FSET:
            att_list[index].fdm.flag_block = 3  # may be 
            flag_block = False
        else:
            att_list[index].fdm.flag_block = 0
    att_list = att_list[::-1]
    assert size == len(att_list)
    return att_list

def cfg_main(att_list):
    '''
    reconginze every function and get   cfg logic
    '''
    att_list = init_cfg(att_list)
    fun_start = 0
    fun_end = 0
    cur_fun = ""
    for index, att in enumerate(att_list):
        att:ATTASM
        if "@function" in att.orignal_str and ".type" in att.orignal_str:
            cur_fun = att.orignal_str.split(',')[0].strip().split('\t')[1].strip()
            fun_start = index + 1
            fun_end =  -1
        elif ".size" in att.orignal_str and len(cur_fun) != 0 and cur_fun in att.orignal_str:
            fun_end = index
            att_list[fun_start:fun_end] = add_cfg_info(att_list[fun_start:fun_end])
            cur_fun = ""

    return att_list



                