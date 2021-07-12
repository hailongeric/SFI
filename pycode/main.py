
from add_sfi import *
import sys
from assem_struct import *
from utilities import * 
from ch_reg_function import *
from build_struct import *

def main_main(s_list):
    att_list = []
    log("   [+]: parse assemble code...")
    for ins in s_list:
        att_list.append(make_struct(ins))
    log("   [+]: solve jump instrcution")
    att_list = solve_jump_ins_main(att_list)
    log("   [+]: add_sfi_main")
    att_list = add_sfi_main(att_list)
    log("   [+]: align 32")
    att_list = add_align(att_list)
    s_list = trans_str(att_list)
    log("   [+]: Done")
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

    log("[+]: start to read file {0}".format(filename))
    s = read_file(filename)
    log("[+]: read file finish, and start to judge condition")
    assert assert_condition(s) == True
    log("[+]: pass condition, and start to change stack reg")
    s = replace_stack_reg(s)
    log("[+]: enter main logic... ")
    s_list =  split_file_data(s)
    s = main_main(s_list)
    log("[+]: finish add sfi, and ouptut file {0} ".format(out_filename))

    # ！！！ in special    jmp * don't using in static shared object
    s = s.replace('*',' ')
    # !!! in special ret recover using .???
    s = s.replace('.???','movq\t%rax, %rdi\n\tmovl\t$0x1000, %eax\n\tret')
  
    write_file_line(s,out_filename)
    log("[+]: Done !!!")
    return
    
if __name__ == "__main__":
    main(sys.argv)