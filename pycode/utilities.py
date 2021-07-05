# python 

DEBUG = False

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
    return s.split('\n')