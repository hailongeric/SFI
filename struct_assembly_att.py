# python 
import re
import sys

DEBUG = True

def log(s):
    if DEBUG:
        print(s)
    return 

def deal_instrcution(ins_list):
    log("enter deal_instrcution")
    tpy = 0x2
    op = ins_list[0]
    ins_op_data =  ins_list[1]
    ins_op_data = ins_op_data.strip()
   
    if "(" in ins_op_data:   # access momery
        # if ins_op_data.count('(') == 2:
        #     tpy = tpy | 0x200
        #     st = ""
        #     access_flag = False
        #     dst_flag = False
        #     ins_op_data_src = []
        #     for c in ins_op_data:
        #         if c != "(" and c != "," and c != " ":
        #             st += c
        #         elif c == "," and access_flag ==False and dst_flag = False:
        #             dst_flag = True
        #             ins_op_data_src.append(st)
        #             st = ""
        #         elif c == "(" and dst_flag == False:
        #             ins_op_data_src.append(st)
        #             st = ""
        #             access_flag = True
        #         elif c== ")" and dst_flag == False:
        #             assert access_flag == True
        #             ins_op_data_src.append(st)
        #             st = ""
        op_data = ins_op_data.split(',')
        
        op_data = [i.strip() for i in op_data]
        if "(" not in op_data[0]:
            return tpy,op,op_data[0],op_data[1:]
        else:   
            for i in range(0,len(op_data)):
                if ")" in op_data[i]:
                    return tpy,op,op_data[0:i+1],op_data[i+1:]


        # else:
        #     tpy = tpy | 0x100
    else:
        ins_op_data = ins_op_data.split(', ')
        ins_op_data_src = ins_op_data[0]
        if len(ins_op_data) > 1:
            tpy = tpy | 0x20
            ins_op_data_dst = ins_op_data[1]
        else:
            tpy = tpy | 0x10
            ins_op_data_dst = None
        return tpy,op,ins_op_data_src,ins_op_data_dst


class ASSEM_ATT():
    def __init__(self):
        self.count = 0

    class INS_Struct():
        def __init__(self,Itype, ins_op, ins_op_data_src=None, ins_op_data_dst=None):
            self.Itype = Itype
            self.op=ins_op
            self.ins_op_data_src = ins_op_data_src
            self.ins_op_data_dst = ins_op_data_dst
        # def __str__():
        #     pass

    def make_struct(self,ins_str):
        self.count += 1
        ins_str = ins_str.strip()
        ins_list = ins_str.split('\t')
        ins_len = len(ins_list)

        if len(ins_str) == 0:
            return None
        if ins_len == 1:

            if ins_str[-1] == ":" and ins_str[0] != "#":
                return self.INS_Struct(0x10,ins_str) # lable type 0
            if ins_str[0] == "." and ins_str[-1] != ":":
                return self.INS_Struct(0x11,ins_str) # annotation type 1
            else:
                return self.INS_Struct(0x12,ins_str) # instruction type 2
        if ins_len == 2:
            if ins_list[0][0]==".":
                return self.INS_Struct(0x21,ins_list[0],ins_list[1]) # annotation type 0
            elif ins_list[0][0] != "." and ins_list[0][0] != "#":
                log(ins_list)
                tpy,op,ins_data_src,ins_data_dst = deal_instrcution(ins_list)
                # t = deal_instrcution(ins_list)
                # log(tpy,op,ins_data_src,ins_data_dst)
                return self.INS_Struct(tpy,op,ins_data_src,ins_data_dst)# TODO instruction deal with
            else:
                print("[+]: unknow instruction : "+ ins_str)
        else:
            print("[+]: unknow instruction : "+ ins_str)

def read_file(filename):
    f = open(filename,"r")
    s = f.read()
    return s.split('\n')

def form(s_list):
    ATT =  ASSEM_ATT()
    att_list = []
    for ins in s_list:
        att_list.append(ATT.make_struct(ins))
    print(att_list)
    return


def main(argv):
    filename = "test.s"
    if len(argv) < 2:
        print("no specify file (default test.s) ")
    else:
        filename = argv[1]
        log("add SFI in {0}".format(filename))
    s = read_file(filename)
    form(s)
    

if __name__ == "__main__":
    main(sys.argv)