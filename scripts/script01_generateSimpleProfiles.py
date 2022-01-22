

import os
import numpy as np
import math

# rectangle, 10% 
x = np.array([  1, 0.01,    0, 0.01, 1])
y = np.array([0.1, 0.10, 0.05,    0, 0])
xy = np.vstack([x,y])

f = open(os.path.join('data','simpleProfiles','rectangle.dat'), 'w+')
f.write("rectangle, 10%\n")
for ii in range(len(x)):
    line = ('    {x:.4f}    {y:.4f}\n').format(x=xy[0,ii], y=xy[1,ii])
    f.write(line)
f.close()


# circle, 10% 
radius = 0.5
xOffset = radius
angle = np.linspace(0,2*math.pi,100)
x = radius*np.cos(angle) + xOffset
y = radius*np.sin(angle)
xy = np.vstack([x,y])

f = open(os.path.join('data','simpleProfiles','circle.dat'), 'w+')
f.write("circle, 100%\n")
for ii in range(len(x)):
    line = ('    {x:.4f}    {y:.4f}\n').format(x=xy[0,ii], y=xy[1,ii])
    f.write(line)
f.close()