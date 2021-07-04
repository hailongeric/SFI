/*
 * loader.c
 * Copyright (C) 2021 eric <hailongeric@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */


#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/mman.h>

extern void  mymain();

static inline void set_r15(unsigned long value){
    asm volatile("mov %0, %%r15"::"r"(value):);
}
int main(){
    char * stack_memory =(char*) mmap(0xbf000000,40960, PROT_READ|PROT_WRITE, MAP_ANON|MAP_SHARED, -1, 0);
    unsigned long stack =(unsigned long) stack_memory + 20480;
    stack &= 0xfffffffffffffff8;

    *((unsigned long*)stack) = (unsigned long)&&con;
    set_r15(stack);
    mymain();
con:
    return 0;
}