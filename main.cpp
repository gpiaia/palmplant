#include "mbed.h"
 
Serial pc(PB_6, PC_5, 115200); // tx, rx

AnalogIn   ain(A1);

AnalogOut  aout(A2);
 
char stringOverSerialBuffer[10];    // buffer to store received string over pc
int bytesRecieved = 0;
uint16_t AnalogOutValue;


volatile bool newCommandFlag = false;    

void serialDataCallback() { 
 
    while (pc.readable()) { // read all available data
        if ((bytesRecieved  == 9) || newCommandFlag){  // avoid buffer overflow
            pc.getc();
        }
        else {
            stringOverSerialBuffer[bytesRecieved] = pc.getc();   // get waiting data
            bytesRecieved++;
            if ((bytesRecieved == 8) || (stringOverSerialBuffer[bytesRecieved-1] == '\n')) {   // buffer full or a new line
                stringOverSerialBuffer[bytesRecieved] = 0;                                                              // append a null
                newCommandFlag  = true;
            }
        }
    }
}

int main(){
    pc.attach(&serialDataCallback);  // attach pc ISR
    
    while(1){
        if(newCommandFlag){
            
            sscanf(stringOverSerialBuffer, "%u", &AnalogOutValue);
            aout.write_u16(AnalogOutValue);
            
            pc.printf("%s\n", stringOverSerialBuffer);
            
            memset(stringOverSerialBuffer, 0, 10);
            bytesRecieved = 0; 
            newCommandFlag = false;
        }
    }
}           