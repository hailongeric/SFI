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
        flag == True
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
    
    if "syscall" in s:
        return False
        
    return True

def write_file(data_list, sfi_filename):
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

    if "（" not in s:
        base = s
    else:
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

def trans_str(att_list):
    pass

    

