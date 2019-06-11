#!/usr/bin/env python
import time
import serial
import struct

ser = serial.Serial(
	port='/dev/ttyS0',
	baudrate = 115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
 	timeout=1
)

i=0

while 1:
	i = i + 1100
	if(i>=65535):
 		i = 0

	time_send = time.time()
	ser.write((str(i)+'\n').encode('utf-8'))
	
	x=ser.readline()

	while (ser.readline() == '\n') :
		x=ser.readline()

	print('cycle time = ' + str(time.time()-time_send) + '  sent = ' + str(i) + '  received = ' +  x.decode('utf-8'))

