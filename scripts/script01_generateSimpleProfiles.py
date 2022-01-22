

import os
import numpy as np

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


