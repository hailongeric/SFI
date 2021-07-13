# python
from keystone import *
from define import *
from utilities import log


class OPD:
    """
    op_data Dtype 
    op_data -> 'Segment-Overwrite:': S_offset: (base: index: scale)
    Dtype   ->        0x        1      1        1      1     1 

    """
    def __init__(self, segment_override = "", s_offset = "",  base = "", index = "", scale = ""):
        self.segment_override = segment_override
        self.s_offset = s_offset
        self.base = base
        self.index = index
        self.scale = scale

        # if or not access memory
        self.accesss_memory = False
    
        self.Dtype = self.__data_type__() # don't suggest use this attribute

    
    def __str__(self):
        # !!! must be access memory instruction
        s = ""
        if len(self.segment_override.strip()) != 0:
            s += self.segment_override + ":"
        s += self.s_offset + "("
        s += self.base 
        if len(self.index.strip()) != 0:
            s += ", " + self.index
        if len(self.scale.strip()) != 0:
            s += ", " + self.scale
        s += ")"
        return s

    def __data_type__(self):
        Dtype = 0
        if len(self.segment_override) != 0:
            Dtype = Dtype | 0x10000
        if len(self.s_offset) != 0:
            Dtype = Dtype | 0x01000
        if len(self.base) != 0:
            Dtype = Dtype | 0x00100
        if len(self.index) != 0:
            Dtype = Dtype | 0x00010
        if len(self.scale) != 0:
            Dtype = Dtype | 0x00001
        return Dtype

    def get_Dtype(self):
        self.Dtype = self.__data_type__()
        return self.Dtype

class ATTASM:
    """
    Itype value:
        #      lable  type 1
        # annotation  type 2
        # instruction type 3
    DataType  # weather or not add access memory flag type
        # 0 not init
        # 1 src dst --> register
        # 2 src -->  register , dst --> memory 
        # 3 src --> memory, dst --> register
        # 4 src --> memory, dst --> memory
    """
    def __init__(self,assem_str="", Itype = 0, operand_size = 0 , DataType = 0, op = "" , source = OPD(), destination = OPD()):
        self.assem_str = assem_str
        self.Itype = Itype 
        self.operand_size = operand_size
        self.op = op
        self.DataType = DataType
        self.jmp_lable= ""
        self.src_opd = source
        self.dst_opd = destination
        
        # TODO add some attach information to inform add SFI information
        self.orignal_str = ""
        self.sfi_stack =  True  #!! default true and must modify and if it 's false no need modify

        self.opcode_size = self.__opcode_size__()  # don't suggest use this attribute

    def __opcode_size__(self):
        global IINSTR
        ks = Ks(KS_ARCH_X86, KS_MODE_64)
        ks.syntax = KS_OPT_SYNTAX_ATT

        # !!! in special 
        # endbr64 and endbr32 
        # lea lable(%rip), %reg

        if self.Itype != IINSTR:
            return 0
        if "endbr" in self.op:  # endbr64 / endbr32 not recongnition by ks.asm
            return 4
        if "lea" in self.op and self.DataType == OPDMEMREG:
            return 7
        try:
            # print(self.assem_str)
            hard_code,count = ks.asm(self.assem_str)  # ks.asm return truple such as.([90,90],1L)
        except keystone.KsError as err:
            log(err)
            print("[+]: "+self.assem_str+"  --> asm error amd I default using jmp lable: 5 byte code")
            hard_code = [90]*5
            count = 1 
        assert count == 1
        return len(hard_code)

    def get_opcode_size(self):
        self.opcode_size = self.__opcode_size__()
        return self.opcode_size 
    def __str__(self):  # use debug
        return str([self.Itype,self.assem_str,self.operand_size,self.DataType,str(self.src_opd),str(self.dst_opd)])
    
    def update_str(self):
        if self.Itype != IINSTR or self.operand_size == 1 or self.DataType == OPDIMEREG:
            return

        if self.DataType == OPDLABLE:
            return 
        s = self.op
        s += '\t'

        strr = {OPDREGREG: lambda x,y:x.base +', '+ y.base,
                OPDREGMEM: lambda x,y:x.base +', '+ str(y),
                OPDMEMREG: lambda x,y:str(x) +', '+ y.base,
                OPDMEMMEM: lambda x,y:str(x) +', '+ str(y)
                }
        if self.operand_size == 2:
            if self.DataType == OPDREG:
                s += self.src_opd.base
            else:
                s += str(self.src_opd)
        else:
            s += strr[self.DataType](self.src_opd,self.dst_opd)
            
        self.assem_str = s
        return
            
        

 