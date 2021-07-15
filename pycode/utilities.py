# python 

LOG = True
DEBUG = False
def log(s):
    if LOG:
        print("[+]: " + str(s))
    return 

def Fdebug(s):
    if DEBUG:
        print("[DEBUB]: " + s)
    return

def warning(s):
    print("[W]: " + s)
    return

def error(s):
    print("[E]: " + s)
    return

def expand_list(s):
    ret = s
    flag = False
    while flag == False:
        flag = True
        s =  ret
        ret = []
        for i in s:

            
            if type(i) == list:
                flag = False
                for j in i:
                    ret.append(j)
            else:
                ret.append(i)
    return ret

def read_file(filename):
    f = open(filename,"r")
    s = f.read()
    return s

def assert_condition(s):
    
    if "r15" in s or "r14" in s or "r13" in s:
        return False

    # !!! in special syscall communitcate    
    # if "syscall" in s:
    #     return False
    
    # !!! in special %rip can't place destination in opdata
    s = s.split("\n")
    for c in s:
        if "rip" in c:
            t = c.split(',')[-1]
            if "rip" in t and "(" not in t:
                return False

    return True

def write_file(data_str, sfi_filename):
    f = open(sfi_filename,'w+')
    f.write(data_str)
    f.close()
    return

def split_single_op_data(s):
    segement_overwrite = ""
    s_offset = ""
    base = ""
    index = ""
    scale = ""
    access = False
    if "(" in s:
        assert ")" in s
        access = True

    if ":"  in s:
        segement_overwrite = s.split(":")[0]
        s = s.split(":")[1]
    if "(" not in s:
        base = s
    else:
        # print(s)
        s_offset = s.split("(")[0]
        s = s.split("(")[1]
        assert s[-1] == ")"
        s = s[:-1]
        s = s.split(",")
        base = s[0]
        if len(s)> 1:
            index = s[1]
        if len(s) > 2:
            scale = s[2]
    return [segement_overwrite.strip(),s_offset.strip(),base.strip(),index.strip(),scale.strip(), access]

# support three-operand variant
def split_op_data(s):
    bracket = False
    ret = []
    last = 0
    for i,c in enumerate(s):
        if c == "," and bracket == False:
            ret.append(s[last:i])
            last = i+1
        if c == '(':
            bracket = True
        if c == ')':
            bracket = False
    ret.append(s[last:])
    return ret

def split_op_opdata(ins_str):
    op = ""
    op_data = ""
    if "\t" in ins_str:
        op = ins_str.split("\t")[0]
        op_data = ins_str.split("\t")[1]
    else:
        for i,c in enumerate(ins_str):
            if c == ' ':
                op = ins_str[:i]
                op_data = ins_str[i+1:]
                break
    assert len(op) > 0
    assert len(op_data) > 0
    return op, op_data

# orginal code 
# def split_file_data(s):
#     s = s.split('\n')
#     ret = []
#     for i in s:
#         if len(i.strip()) == 0:
#             continue
#         ret.append(i)
#     return ret
# above orignal code 
# !!! in special add ret in global 
def in_format_patch(s:str):
    s = s.split('\n')
    ret = []
    RET_FLAG = False
    RET_FUN = ""

    for i in s:
        if len(i.strip()) == 0:
            continue
        if ".globl" in i:
            RET_FLAG = True
            RET_FUN = i.split(" ")[-1].strip()
            
        if RET_FLAG and 'ret' in i:
            # replace ret using .???
            if i.strip() != "ret":
                print("[!] {} differ default(ret)".format(i))

            ret.append(i.replace('ret','.???'))
            continue
        if ".size" in i and RET_FUN in i and RET_FLAG:
            RET_FLAG = False
        ret.append(i)
    return ret

def if_in(op_list,op):
    for i_op in op_list:
        if i_op in op:
            return True
    
    return False

def out_format_patch(s:str):
    # !!! in special    jmp * don't using in static shared object
    s = s.replace('*',' ')
    # !!! in special ret recover using .???
    s = s.replace('.???','movq\t%rax, %rdi\n\tmovl\t$0x1000, %eax\n\tret')
    # !!! in special last line  must be '\n'
    s += "\n"
    return s