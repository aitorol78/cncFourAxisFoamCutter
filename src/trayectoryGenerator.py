

from machine import machine
from wingPanelLayout import wingPanelLayout
import numpy as np

class trayectoryGenerator:
    def __init__(self):
        self.machine = machine()
        self.wingPanelLayout = wingPanelLayout()

        self.numPointUpperSurface = 100
        self.numPointsLowerSurface = 100

        self.trayectoryXPlus = np.zeros(1)
        self.trayectoryYPlus = np.zeros(1)
        self.trayectoryXMinus = np.zeros(1)
        self.trayectoryYMinus = np.zeros(1)
    
    def generateTrayectory(self):
        
        # profiles should have upper and lower surfaces
        #    easiest: profileSectionY > < 0 + points with x=xMin ( no x = xMax, profiles always have +- Y trailing edge points)

        # for each surface
            # calculate length of line
            # interpolate numPoints 
        
        # add entry and exit points 

        # translate points to wire planes along the lines connecting Zplus and zMinus surfaces

        



