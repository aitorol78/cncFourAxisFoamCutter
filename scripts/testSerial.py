
import serial

s1 = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)

print(s1.readline())
print(s1.readline())
print(s1.readline())
print(s1.readline())
s1.write("G1X-10F500\n".encode())
print(s1.readline())
s1.write("$$".encode())
print(s1.readline())
print(s1.readline())
print(s1.readline())
print(s1.readline())
print(s1.readline())
print(s1.readline())
print(s1.readline())

s1.close();
