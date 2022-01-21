
from trayectoryGenerator import trayectoryGenerator
import serial
import time

class trayectoryExecutor:
    def __init__(self):
        self.sleepTimeAtFirstPoint = 5
        sPlus = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.5, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)
        sMinus = serial.Serial(port="/dev/ttyUSB1", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.5, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)

    def goToFirstPoint(self, tr):
        linePlus = ('X{}Y{}F{}').format(tr.wirePlusTrayectoryX[0], tr.wirePlusTrayectoryY[0], tr.wirePlusTrayectoryF[0])
        lineMinus = ('X{}Y{}F{}').format(tr.wireMinusTrayectoryX[0], tr.wireMinusTrayectoryY[0], tr.wireMinusTrayectoryF[0])
        self.sPlus.write(linePlus.encode())
        self.sMinus.write(lineMinus.encode())

    def waitAtFirstPoint(self):
        time.sleep(self.sleepTimeAtFirstPoint)

    def followTrayectoryFromSecondPoint(self, tr):
        numPoints = len(tr.wirePlusTrayectoryX)
        for ii in range(1,numPoints):
            linePlus = ('X{}Y{}F{}').format(tr.wirePlusTrayectoryX[ii], tr.wirePlusTrayectoryY[ii], tr.wirePlusTrayectoryF[ii])
            lineMinus = ('X{}Y{}F{}').format(tr.wireMinusTrayectoryX[ii], tr.wireMinusTrayectoryY[ii], tr.wireMinusTrayectoryF[ii])
            self.sPlus.write(linePlus.encode())
            self.sMinus.write(lineMinus.encode())
            time.sleep(0.2)

