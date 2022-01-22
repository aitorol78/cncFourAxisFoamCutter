

import numpy as np
import serial
import time

s1 = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.5, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)
s2 = serial.Serial(port="/dev/ttyUSB1", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.5, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)

time.sleep(5)

pointsXY = np.array([[10,30,10,0],[0,30,30,0]])
F = 2500
repetitions = 2

for rep in range(repetitions):
    for iPoint in range(4):
        line = "G1X{}Y{}F{}\n".format(pointsXY[0,iPoint],pointsXY[1,iPoint],F)
        print(line)
        s1.write(line.encode())
        s2.write(line.encode())
        time.sleep(0.01)
        
s1.close();
s2.close();

