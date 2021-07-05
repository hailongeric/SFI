# python 

from keystone import *
import re
import sys

DEBUG = False

ks = Ks(KS_ARCH_X86, KS_MODE_64)
ks.syntax = KS_OPT_SYNTAX_ATT

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

def log(s):
    if DEBUG:
        print s
    return 

def ch_rg(s):
    # rbp --> r14
    # rsp --> r15
    # arg s: string --> read input file convert string
    # return string --> string after solve ch_rg 
    s = s.replace("%rsp","%r15")
    s = s.replace("%rbp","%r14")
    s = s.replace("%spl","%r15b")
    s = s.replace("%bpl","%r14b")
    s = s.replace("%sp","%r15w")
    s = s.replace("%bp","%r14w")
    s = s.replace("%esp","%r15d")
    s = s.replace("%ebp","%r14d")
    return s

def ch_push(s):
    # modify push instruction
    # arg s: a line string --> need to modify
    # return ins: string list --> after add some sfi
    s_add = "subq\t$8, %r15"
    s = s.replace('push','mov')
    s += ", 0(%r15)"
    return ['\t'+s_add, '\t'+s]

def ch_pop(s):
    # modify pop instruction
    # arg s: a line string --> need to modify
    # return ins: string list --> after add some sfi
    s = s.replace('pop','mov')
    s = s.split('\t')
    s[1]  = "0(%r15), "+s[1]
    s = "\t".join(s)
    s_add = "addq\t$8, %r15"
    return ['\t'+s, '\t'+s_add]

def ch_ret(s):
    # modify ret instruction
    # arg string : "ret"
    # return ins: string list --> after add some sfi
    s_add = "addq\t$8, %r15"
    s = "jmp\t*-8(%r15)"
    return ['\t'+s_add, '\t'+s]

def ch_call(s):
    # modify call instruction
    # arg string : a line str --> call instrcution string
    # return ins: string list --> after add some sfi
    s_add ="subq\t$8, %r15"
    # s_add_1 ="movq    %rip, (%r15)"
    s_add_1 ="lea\t0(%rip), %rax"
    s_add_2 = "addq\t$12, %rax"
    s_add_3 ="movq\t%rax, (%r15)"
    s = s.replace("call","jmp *")
    return ['\t'+s_add,'\t'+s_add_1,'\t'+s_add_2,'\t'+s_add_3,'\t'+s]

def ch_leave(s):
    # modify leave instruction
    # arg string : a line str --> "leave" instrcution string
    # return ins: string list --> after add some sfi
    assert s == "leave"
    s_add = "movq\t%r14, %r15"
    s_add_1 = "movq\t(%r15), %r14"
    s_add_2 = "addq\t$8, %r15"
    return ['\t'+s_add, '\t'+s_add_1, '\t'+s_add_2]

def create_output_file(data_list, sfi_filename):
    try:
        f = open(sfi_filename,'w+')
    except OSError as err:
        print("Open file error: {0}".format(err))
    for data in data_list:
        if type(data) == str:
            f.write(data+'\n')
        else:
            assert type(data) == list
            for subdata in data:
                if type(subdata) == str:
                    f.write(subdata+'\n')
                else:
                    assert type(subdata) == list
                    for subsubdata in subdata:
                        assert  type(subsubdata) == str
                        f.write(subsubdata+'\n')
    f.close()
    return

def expand_data_list(data_list):
    # expand some multi list element
    ret = []
    for data in data_list:
        if type(data) == str:
            ret.append(data)
        else:
            assert type(data) == list
            for subdata in data:
                if type(subdata) == str:
                    ret.append(subdata)
                else:
                    assert type(subdata) == list
                    for subsubdata in subdata:
                        assert  type(subsubdata) == str
                        ret.append(subsubdata)
    return ret

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

def add_sfi(filename):
    try:
        f = open(filename,'r')
        as_data = f.read()
        f.close()
    except OSError as err:
        print("Open read file error: {0}".format(err))
    as_data = ch_rg(as_data)  # replace rsp rbp using r15 r14
    as_data = as_data.split('\n')
    index = 0
    as_data_len = len(as_data)
    while index < as_data_len:
        s_line =  as_data[index]
        s_line = s_line.strip()
        if len(s_line) == 0:
            index += 1
            continue
        if s_line[0] == '.': # annotation
            index += 1
            continue
        if s_line[-1] == ':': # lable
            index += 1
            continue
        else:
            ins =  s_line.split("\t")
            op = ins[0]
            if "push" in  op:
                as_data[index] = ch_push(s_line)
            elif "pop" in op:
                as_data[index] = ch_pop(s_line)
            elif "ret" in op:
                as_data[index] = ch_ret(s_line)
            elif "call" in op:
                as_data[index] = ch_call(s_line)
            elif "leave" in op:
                as_data[index] = ch_leave(s_line)
        index += 1

    as_data = expand_data_list(as_data)
    as_data = add_confinement(as_data)
    as_data = add_align(as_data)
    create_output_file(as_data,sfi_filename="sfi_"+filename)
    return

def main(argv):
    filename = "test.s"
    if len(argv) < 2:
        print("no specify file (default test.s) ")
    else:
        filename = argv[1]
        print("add SFI in {0}".format(filename))
    add_sfi(filename)
        
if __name__ == "__main__":
    main(sys.argv)
# TODO 
# modify .L0: lable in ch_register : add_sfi

