
from trayectoryGenerator import trayectoryGenerator
import serial
import time
import os

class trayectoryExecutor:
    def __init__(self):
        self.GRBL_RX_BUFFER_SIZE = 127
        self.sleepTimeAtFirstPoint = 5
        self.portPlus="/dev/ttyUSB0"
        self.portMinus="/dev/ttyUSB1"
        self.flagUsePlus = True
        self.flagUseMinus = True
        #self.sPlus = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.5, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)
        #self.sMinus = serial.Serial(port="/dev/ttyUSB1", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.5, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)

    def connectToServos(self):
        if self.flagUsePlus:
            self.sPlus = serial.Serial(port=self.portPlus, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.5, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)
            self.sPlus.write(('\r\n\r\n').encode())
            time.sleep(2)
            while self.sPlus.inWaiting():
                print(self.sPlus.readline())
            self.sPlus.flushInput()
        if self.flagUseMinus:
            self.sMinus = serial.Serial(port=self.portMinus, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.5, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)
            self.sMinus.write(('\r\n\r\n').encode())
            time.sleep(2)
            while self.sMinus.inWaiting():
                print([self.sMinus.readline() + '\n'])
            self.sMinus.flushInput()

    def goToFirstPoint(self, tr):
        if self.flagUsePlus:
            linePlus = ('G1X{x:.3f}Y{y:.3f}F{z:.1f}\n').format(x=tr.wirePlusTrayectoryX[0], y=tr.wirePlusTrayectoryY[0], z=tr.wirePlusTrayectoryF[0])
            self.sPlus.write(linePlus.encode())
            print("                                    " + linePlus)
            self.sPlus.flushInput()
        if self.flagUseMinus:
            lineMinus = ('G1X{x:.3f}Y{y:.3f}F{z:.1f}\n').format(x=tr.wireMinusTrayectoryX[0], y=tr.wireMinusTrayectoryY[0], z=tr.wireMinusTrayectoryF[0])
            self.sMinus.write(lineMinus.encode())
            print(lineMinus)
            self.sMinus.flushInput()

    def waitAtFirstPoint(self):
        time.sleep(self.sleepTimeAtFirstPoint)

    def followTrayectoryFromSecondPoint(self, tr):
#log    f = open(os.path.join('data','debugLogs','executorLog.txt'), 'w+')
        numPoints = len(tr.wirePlusTrayectoryX)
        self.sPlus.flushInput()
        nextPoint = 1
        charCount = []
        linePlus = []
        while nextPoint < numPoints:
            logLine = ('nextPoint {} sum(charCount) {} len(linePlus) {} inWaiting() {} linePlus: {}\n').format(nextPoint, sum(charCount), len(linePlus), self.sPlus.inWaiting(), linePlus)
            print(logLine)
#log        f.write(logLine)
            if self.sPlus.inWaiting():
                responseLine = self.sPlus.readline().strip().decode()
                if (responseLine.find('ok') > -1) | (responseLine.find('error') > -1):
                    del charCount[0]
            linePlus = ('G1X{x:.3f}Y{y:.3f}F{z:.1f}\n').format(x=tr.wirePlusTrayectoryX[nextPoint], y=tr.wirePlusTrayectoryY[nextPoint], z=tr.wirePlusTrayectoryF[nextPoint])
            if sum(charCount) + len(linePlus) < self.GRBL_RX_BUFFER_SIZE - 2:
                self.sPlus.write(linePlus.encode())
                nextPoint = nextPoint + 1 
                charCount.append(len(linePlus))
            #time.sleep(0.1)
#log    f.close()




        #for ii in range(1,numPoints):
        #    if self.flagUsePlus:
        #        linePlus = ('G1X{x:.3f}Y{y:.3f}F{z:.1f}\n').format(x=tr.wirePlusTrayectoryX[ii], y=tr.wirePlusTrayectoryY[ii], z=tr.wirePlusTrayectoryF[ii])
        #        self.sPlus.write(linePlus.encode())
        #        print("                                    " + linePlus)
        #    if self.flagUseMinus:
        #        lineMinus = ('G1X{x:.3f}Y{y:.3f}F{z:.1f}\n').format(x=tr.wireMinusTrayectoryX[ii], y=tr.wireMinusTrayectoryY[ii], z=tr.wireMinusTrayectoryF[ii])
        #        self.sMinus.write(lineMinus.encode())
        #        print(lineMinus)
        #    time.sleep(0.2)

