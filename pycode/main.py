
from add_sfi import *
import sys
from assem_struct import *
from utilities import * 
from ch_reg_function import *
from build_struct import *

def main_main(s_list):
    log("\tparse assemble code...")
    att_list = init_asm(s_list)
    log("\tsolve jump instrcution")
    att_list = solve_jump_ins_main(att_list)
    log("\tadd_sfi_main")
    att_list = add_sfi_main(att_list)
    log("\talign 32")
    att_list = add_align(att_list)
    s_list = trans_str(att_list)
    return s_list

def main(argv):
    
    filename = "test.s"
    out_filename="sfi_"+filename
    if len(argv) < 2:
        print("no specify file (default test.s) ")
    else:
        filename = argv[1]
        if len(argv) == 3:
            out_filename = argv[2]

    log("start to read file {0}".format(filename))
    s = read_file(filename)
    log("read file finish, and start to judge condition")
    assert assert_condition(s) == True
    log("pass condition, and start to change stack reg")
    s = replace_stack_reg(s)
    log("enter main logic... ")
    s_list =  in_format_patch(s)
    s = main_main(s_list)
    log("finish add sfi, and ouptut file {0} ".format(out_filename))

    s = out_format_patch(s)
    write_file(s,out_filename)
    log("Done !!!")
    return
    
if __name__ == "__main__":
    main(sys.argv)