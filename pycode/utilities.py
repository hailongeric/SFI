# python 

DEBUG = True

def log(s):
    if DEBUG:
        print(s)
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

def write_file_line(data_str, sfi_filename):
    f = open(sfi_filename,'w+')
    f.write(data_str+"\n")
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
        print(s)
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
    return [segement_overwrite,s_offset,base,index,scale, access]

def split_op_data(s):
    bracket = False
    for i,c in enumerate(s):
        if c == "," and bracket == False:
            return [s[:i], s[i+1:]]
        if c == '(':
            bracket = True
        if c == ')':
            bracket = False
    return [s,""]

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
def split_file_data(s):
    s = s.split('\n')
    ret = []
    RET_FLAG = False
    for i in s:
        if len(i.strip()) == 0:
            continue
        if ".globl" in i:
            RET_FLAG = True
        if RET_FLAG and 'ret' in i:
            # replace ret using .???
            ret.append(i.replace('ret','.???'))
            RET_FLAG = False
            continue
        ret.append(i)
    return ret

def if_in(op_list,op):
    for i_op in op_list:
        if i_op in op:
            return True
    
    return False
