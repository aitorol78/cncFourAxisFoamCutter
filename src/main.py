
import numpy as np
import math
from sectionProfile import sectionProfile
from geom3d import geom3d, plane3d, line3d

if __name__ == "__main__":

    fileName = 'profiles/ag25.dat'
    #sectionZplus = sectionProfile()
    #sectionZplus.loadFromFile(fileName)

    sectionLayoutZplus = sectionLayout()
    sectionLayoutZplus.loadFromFile(fileName)

    a = 3
