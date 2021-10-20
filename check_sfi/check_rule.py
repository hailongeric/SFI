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
from capstone.x86 import *
import sys

LOG = True

def log(s):
    if LOG:
        print("[+] " + s)
    return
        
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

def reg_swtich_low_2(reg):
    reg_low_table = {"rax":"eax","rbx":"ebx","rcx":"ecx","rdx":"edx","rsi":"esi","rdi":"edi","rbp":"ebp","rsp":"esp","r8":"r8d","r9":"r9d","r10":"r10d","r11":"r11d","r12":"r12d","r13":"r13d","r14":"r14d","r15":"r15d"}
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
    
    def disasm_code(self,code):
        '''
        disasm binary : 
        input: binary code 
        output: capstone's assembly format structure
        '''
        disam = self.cs.disasm(code,0)
        ret = []
        for ins in disam:
            ret.append(ins)
        ret = ret[::-1]
        return ret

    def assert_data(self, ASM:list):
        # TODO no include rsp esp rbp rsp rip syscall call
        s = [i.mnemonic + "\t" + i.op_str for i in ASM]
        s = ''.join(s)
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

    def check_rules(self):
        # if "%rsp"
        # TODO need to increase the information of details
        for i in range(6,len(self.check_data)):
            ASM = self.disasm_code(self.check_data[i])
            assert self.assert_data(ASM) == True
            assert self.check_memory(ASM) == True
            assert self.check_jmp(ASM) == True
            assert self.check_RZP(ASM) == True
        
        return 

    def check_memory(self,ASM:list):
        '''
        check every mem access base index if bundle 

        '''
        Track = []
        track_base = []
        assert_need =  False
        track_index = []
        # Capstone assmemble data structure
        '''
        struct x86_op_mem {
            x86_reg segment;
            x86_reg base;
            x86_reg index;
            int scale;
            long disp;
        }
        '''
        # TODO function return retq instruction
        for insn in ASM:

            if  "nop" in insn.mnemonic:
                continue
            
            if "ret" in insn.mnemonic:
                return True
            if assert_need and len(insn.operands) ==2 :
                if insn.operands[1].type == X86_OP_REG:
                    for reg in Track:
                        if reg_swtich_low_2(reg) == insn.reg_name(i.value.reg) and ("mov" in insn.mnemonic or "lea" in insn.mnemonic):
                            Track.remove(reg)
                if len(Track) == 0:
                    assert_need = False

            if "lea" in insn.mnemonic:
                continue
            
            # TODO solve rep check validify
            # if "rep" in insn.mnemonic:
            #     continue

                
            if len(insn.operands) > 0:
                log("Number of operands: %u" %len(insn.operands))
                ins = []
                for i in insn.operands:
                    if i.type == X86_OP_REG:
                        ins.append(insn.reg_name(i.value.reg))
                    elif i.type == X86_OP_IMM:
                        ins.append(i.value.imm)
                    elif i.type == X86_OP_MEM:
                        ins.append(i.value.mem)
                        if i.value.mem.base !=0:
                            if insn.reg_name(i.value.mem.base) not in ["r14","r15","r13"]:
                                track_base.append(insn.reg_name(i.value.mem.base))

                        if i.value.mem.index !=0:
                            track_index.append(insn.reg_name(i.value.mem.index))
                    else:
                        print("[+] don't reconginze code assemble, YOU MUST BE CHECK AGAIN!!!")
                print("ins:->"+str(ins))
            if len(track_base) != 0 or len(track_index) != 0:
                assert_need = True
                Track = track_index + track_base
                track_base = []
                track_index = []

            print("check_mem->"+ str(Track))

        if assert_need == True:
            return False      
        return True

    def check_RZP(self,ASM:list):
        '''
        check RZP can't modify 
        '''
        for insn in ASM:
            if "%r13" not in insn.op_str:
                continue

            # if r13 is in this insn, the number of operands must be greater than 0
            assert len(insn.operands) > 0

            for index,i in enumerate(insn.operands):
                if i.type == X86_OP_REG:
                   assert ("r13" not in insn.reg_name(i.value.reg) or index != 1)
                elif i.type == X86_OP_MEM:
                    if i.value.mem.base !=0:
                        assert "r13" in  insn.reg_name(i.value.mem.base)
                    if i.value.mem.index !=0:
                        assert "r13" not in insn.reg_name(i.value.mem.index)

        return True


    def check_jmp(self, ASM:list):
        '''
        check jmp address ： align 32
        check jmp register: track bundle and align 32
        '''
        Track_REG = ""
        # flag jmp destination is register
        Jmp_REG = False
        # flag jmp destination align 32
        Align = False
        Data_reg = ""

        for insn in ASM:
            if  "jmp" in insn.mnemonic:
                # jmp insn must have one operands
                assert len(insn.operands) > 0
                for index,i in enumerate(insn.operands):
                    if i.type == X86_OP_REG:
                        Track_REG = insn.reg_name(i.value.reg)
                        Jmp_REG = True
                    elif i.type == X86_OP_IMM:
                        assert i.value.imm % 32 == 0
                    else:
                        print("[+] check_jmp: operands exception, YOU MUST BE CHECK AGAIN!!!")
                    assert index < 1
            elif Jmp_REG:
                if Track_REG in insn.op_str:
                    if "r13" in insn.op_str:
                        for index,i in enumerate(insn.operands):
                            if i.type == X86_OP_REG:
                                assert Track_REG == insn.reg_name(i.value.reg) and index == 1
                            elif i.type == X86_OP_MEM:
                                if i.value.mem.base !=0:
                                    assert "r13" in  insn.reg_name(i.value.mem.base)
                                    assert i.value.mem.index !=0
                                    assert Track_REG in insn.reg_name(i.value.mem.index)
                                    Jmp_REG = False
                                    Align = True
            elif Align:
                if reg_swtich_low_2(Track_REG) in insn.op_str:
                    if "and" in insn.mnemonic:
                        for index,i in enumerate(insn.operands):
                            if i.type == X86_OP_REG:
                                assert reg_swtich_low_2(Track_REG) in insn.reg_name(i.value.reg) and index == 1
                                Align = False
                                Track_REG = ""
                            elif i.type == X86_OP_IMM:
                                assert i.value.imm % 32 == 0 and index == 0
                    if "sh" in insn.mnemonic:
                        try:
                            assert insn.operands[1].value.reg == insn.operands[2].value.reg
                            assert reg_swtich_low_2(Track_REG) in insn.reg_name(insn.operands[1].value.reg) 
                            Data_reg = insn.reg_name(insn.operands[0].value.reg)

                        except:
                                print("[+] check_jmp Align operands error: CHECK IT AGAIN")
                if "mov" in insn.mnemonic and len(Data_reg) != 0:
                    for index,i in enumerate(insn.operands):
                        if i.type == X86_OP_REG:
                            assert Data_reg == insn.reg_name(i.value.reg)
                            Data_reg = ""
                        elif i.type == X86_OP_IMM:
                            assert i.value.imm == 5
                    Align = False

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
