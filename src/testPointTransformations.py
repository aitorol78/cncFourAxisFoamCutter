
import numpy as np
import math

a = np.array([[0,0,1,1],[0,1,0,1]])
angle = 3.141592 / 4.0

R = np.array([[math.cos(angle),math.sin(angle)],[-math.sin(angle),math.cos(angle)]])

b = np.matmul(R,a)
print(b)

e = a
e[0,:] = e[0,:] + 5
e[1,:] = e[1,:] + 100
print(e)
print(a)

e = e + np.array([[1000],[10000]])
print(e)
print(a)

