
import numpy as np

x = 77.1
y = 23.8
F = 200
point = np.array([[10,11],[20,21]])

line1 = "G1X{}Y{}F{}".format(point[0,0],point[1,0],F)
line2 = "G1X{}Y{}F{}".format(point[0,1],point[1,1],F)

print(line1)
print(line2)


