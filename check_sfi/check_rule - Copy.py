#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 eric <hailongeric@gmail.com>
#
# Distributed under terms of the MIT license.

"""
check the binary's  sfi rules

"""

import re
from pwn import *
import keystone as KS
import capstone as CS
import sys

class OPD:
    def __init__(self) -> None:
        pass

class ASM_ATT:
    def __init__(self,ins:str):
        self.ins_str = ins
        self.op = ins.split("\t")[0]
        


# read elf file from binary 
def readelf_bak(filename):
    f = open(filename,"rb")
    data = f.read()
    f.close()
    return data

def reg_swtich_low(reg):
    reg_low_table = {"%rax":"%eax","%rbx":"%ebx","%rcx":"%ecx","%rdx":"%edx","%rsi":"%esi","%rdi":"%edi","%rbp":"%ebp","%rsp":"%esp","%r8":"%r8d","%r9":"%r9d","%r10":"%r10d","%r11":"%r11d","%r12":"%r12d","%r13":"%r13d","%r14":"%r14d","%r15":"%r15d"}
    reg = reg.strip()
    return reg_low_table[reg]

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

class check_sfi:
    def __init__(self,filename) -> None:
        self.base_addr = 0
        self.filename = filename
        self.symbols = []
        self.elf = None
        self.sym_addr = []
        self.syms_str = [] 
        self.check_data = None
        self.cs = CS.Cs(CS.CS_ARCH_X86, CS.CS_MODE_64)
        self.cs.syntax = CS.CS_OPT_SYNTAX_ATT
        self.cs.detail = True

    def readelf(self):
        self.elf = ELF(self.filename)
        self.symbols = self.elf.symbols

    def set_baseaddr(self):
        self.base_addr = self.symbols["frame_dummy"]+16
        for i in self.symbols:
            self.syms_str.append(i)
        for j in self.syms_str:
            self.sym_addr.append(self.symbols[j])
            
    def read_data(self):
        self.check_data = self.elf.section(".text")

    def split_data(self):
        data = []
        for i in range(0,len(self.check_data),32):
            data.append(self.check_data[i:i+32])
        size  = len(self.check_data)
        data.append(self.check_data[size-size%32:])
        self.check_data = data
    # !!! check_data is list data

    def nop_code(self):
        pass

    def disasm_code(self,code):
        disam = self.cs.disasm(code,0)
        return disam
        ret = []

        for i in disam:
            if len(i.operands) > 0:
                print("\tNumber of operands: %u" %len(i.operands))
                for opr in i.operands:
                    print(opr.type)
            ret.append(i.mnemonic + "\t" + i.op_str)
        return ret

    def assert_data(self, ASM:list):
        # TODO no include rsp esp rbp rsp rip syscall call
        s = ''.join(ASM)
        if "%rsp" in s:
            return False
        if "%spl" in s:
            return False
        if "%bpl" in s:
            return False
        if "%sp" in s:
            return False
        if "%bp" in s:
            return False
        if "%esp" in s:
            return False
        if "%ebp" in s:
            return False
        if "%eip" in s:
            return False
        if "syscall" in s:
            return False
        if "call" in s:
            return False
        if "leave" in s:
            return False
        return True

        # def assert_data(self, ASM:list):
        # # TODO no include rsp esp rbp rsp rip syscall call
        # s = ''.join(ASM)
        # if "%rbp" in s:
        #     return False
        # if "%rsp" in s:
        #     return False
        # if "%spl" in s:
        #     return False
        # if "%bpl" in s:
        #     return False
        # if "%sp" in s:
        #     return False
        # if "%bp" in s:
        #     return False
        # if "%esp" in s:
        #     return False
        # if "%ebp" in s:
        #     return False
        # # if "%rip" in s:
        # #     return False
        # if "%eip" in s:
        #     return False
        # if "syscall" in s:
        #     return False
        # if "call" in s:
        #     return False
        # if "leave" in s:
        #     return False
        # return True
    
    def check_rules(self):
        # if "%rsp"
        for i in range(6,len(self.check_data)):
            ASM = self.disasm_code(self.check_data[i])
            print(ASM)
            assert self.assert_data(ASM) == True
            assert self.check_memory(ASM) == True
            assert self.check_jmp(ASM) == True
            # assert self.check_RZP(ASM) == True
        
        return 

    def check_memory(self,ASM:list):
        # 'leaq\t-8(%r15), %r15', 
        # 'movq\t%r14, 0(%r15)', 
        # 'movq\t%r15, %r14', 
        # 'movq\t%rdi, -0x28(%r14)', 
        # 'movq\t%rsi, -0x30(%r14)', 
        # 'movl\t%edx, -0x34(%r14)', 
        # 'movq\t-0x30(%r14), %rax', 
        # 'movq\t%rax, -0x10(%r14)', 
        # 'nop\t'
        return True
        pass
        for i_str in ASM:
            if i_str.count("(") == 0:
                continue
            if i_str.count("(") == 1:
                split_data = i_str.strip()
                split_data = split_data.split("\t")
                if len(split_data) == 2:
                    op = split_data[0]
                    op_data = split_data[1]
                    op_src = 1
                    op_data = op_data.split(',')
                    op_src = op_data[0]
                    op_dst = op_data[1]

        return True

    def check_RZP(ASM:list):
        for i_str in ASM:
            if "%r13" in i_str:
                split_data = i_str.strip()
                split_data = split_data.split("\t")
                op_data = split_data[1]
                assert "%r13" in op_data
                assert "%r13" in op_data.split(",")[0]
                op_data = op_data.split(",")
                op_data = op_data[1:]
                op_data = "".join(op_data)
                assert "%r13" not in op_data
        return True


    def check_jmp(self, ASM:list):
        for i_str in ASM:
            if "jmp" in i_str:
                if "%" not in i_str:
                    offset = int(i_str.split("\t")[1].strip(),16)
                    assert offset%0x20 == 0
                else:
                    index = ASM.index(i_str)
                    reg = re.findall("\%\w+",i_str)
                    index -= 1
                    assert index >= 0
                    last_str = ASM[index]
                    # TODO  prove this write module
                    assert "lea" in last_str
                    assert "%r13" in last_str
                    assert reg in last_str 
                    l_reg = reg_swtich_low(reg)
                    index -= 1
                    assert index >= 0
                    last_str = ASM[index]
                    assert l_reg in last_str
        return True

    

    def check_main(self):
        self.readelf() 
        self.set_baseaddr()
        self.read_data()
        self.split_data()
        self.check_rules()


def main(argv):
    filename = "sfi_test.so"
    if len(argv) < 2:
        print("no specify checking file (default sfi_test.so) ")
    else:
        filename = argv[1]
    
    CSFI = check_sfi(filename)
    CSFI.check_main()
    return


if __name__ == "__main__":
    main(sys.argv)
