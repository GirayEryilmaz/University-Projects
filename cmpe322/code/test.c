#include <lib.h>    // provides _syscall and message
#include <stdio.h>

int main(void) {
    message m;
    m.m1_i1 = 11;
    
    _syscall(PM_PROC_NR, PRINTINTEGER, &m);

}
