#include "mbed.h"
 
Serial pc(PB_6, PC_5, 115200); // tx, rx

int main()
{
    int i = 0;
    while(1) {
        pc.printf("%d", i++);
    }
}