# python
from keystone import *
from utilities import log

ks = Ks(KS_ARCH_X86, KS_MODE_64)
ks.syntax = KS_OPT_SYNTAX_ATT

class OP_DATA:
    def __init__(self, Dtype = 0, segment_override = "", s_offset = "",  base = "", index = "", scale = ""):
        self.Dtype = Dtype  # 0 src dst --> register
                            # 1 src -->  register , dst --> memory 
                            # 2 src --> memory, dst --> register
                            # 3 src --> memory, d 
        self.segment_override = segment_override
        self.s_offset = s_offset
        self.base = base
        self.index = index
        self.scale = scale

class ATT_Syntax:
    def __init__(self,ori_str=None, Itype = 0, operand_size = 0 , op = None , source = OP_DATA, destination = OP_DATA):
        self.ori_str = ori_str
        self.Itype = Itype
        self.operand_size = operand_size
        self.op = op
        self.source = source
        self.destination = destination
        self.opcode_size = self.__get_opcode_size__()
    
    def __get_opcode_size__():
        global ks
        try:
            hard_code,count = ks.asm(data)  # ks.asm return truple such as.([90,90],1L)
        except keystone.KsError as err:
            log(err)
            print("[+]: "+data+"--> asm error amd I default using jmp lable: 7 byte code")
            hard_code = [90]*7
            count = 1 
        assert count == 1
        

 