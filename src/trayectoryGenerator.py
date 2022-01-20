

#from machine import machine
from wingPanelLayout import wingPanelLayout
import numpy as np
import math

class trayectoryGenerator:
    def __init__(self):
        #self.machine = machine()
        self.wpl = wingPanelLayout()

        self.numStationsUpperSurface = 100
        self.numStationsLowerSurface = 100

        self.trayectoryXPlus = np.zeros(1)
        self.trayectoryYPlus = np.zeros(1)
        self.trayectoryFPlus = np.zeros(1)  # velocity
        self.trayectoryXMinus = np.zeros(1)
        self.trayectoryYMinus = np.zeros(1)
        self.trayectoryFMinus = np.zeros(1)
    
    def generateTrayectory(self):
        
        # profiles should have upper and lower surfaces
        #    easiest: profileSectionY > < 0 + points with x=xMin ( no x = xMax, profiles always have +- Y trailing edge points)
        # ¿WHY? I could consider just one curve -> NOP, the wire should get to the leading edge at the same time at both ends

        #print(self.wpl.sectionMinusLayout.computeLengthOfUpperSurface())
        #print(self.wpl.sectionPlusLayout.computeLengthOfUpperSurface())
        #print(self.wpl.sectionMinusLayout.computeLengthOfLowerSurface())
        #print(self.wpl.sectionPlusLayout.computeLengthOfLowerSurface())

        self.wpl.sectionMinusLayout.resampledSectionCoordinatesX,  \
            self.wpl.sectionMinusLayout.resampledSectionCoordinatesY = self.resampleSectionPoints(self.wpl.sectionMinusLayout, self.numStationsUpperSurface, self.numStationsLowerSurface)

        self.wpl.sectionPlusLayout.resampledSectionCoordinatesX,  \
            self.wpl.sectionPlusLayout.resampledSectionCoordinatesY = self.resampleSectionPoints(self.wpl.sectionPlusLayout, self.numStationsUpperSurface, self.numStationsLowerSurface)

        #self.wpl.sectionMinusLayout.sectionCoordinatesX
        #self.wpl.sectionMinusLayout.sectionCoordinatesY


        # for each surface
            # calculate length of curve
            # interpolate numPoints
            # compute velocities at each side
            # compute wire-surface distance compensation = f(wireDiameter, velocity ?)
            # compute compensated points
        
        # add entry and exit points 

        # translate points to wire planes along the lines connecting Zplus and zMinus surfaces

    def resampleSectionPoints(self, section, numStationsUpperSurface, numStationsLowerSurface):
        newIndexes = np.linspace(min(section.indUpperSurface), max(section.indUpperSurface), numStationsUpperSurface)
        resampledSectionCoordinatesXUpperSurf = np.interp(newIndexes, section.indUpperSurface, section.sectionCoordinatesX[section.indUpperSurface])
        resampledSectionCoordinatesYUpperSurf = np.interp(newIndexes, section.indUpperSurface, section.sectionCoordinatesY[section.indUpperSurface])

        newIndexes = np.linspace(min(section.indLowerSurface), max(section.indLowerSurface), numStationsLowerSurface)
        resampledSectionCoordinatesXLowerSurf = np.interp(newIndexes, section.indLowerSurface, section.sectionCoordinatesX[section.indLowerSurface])
        resampledSectionCoordinatesYLowerSurf = np.interp(newIndexes, section.indLowerSurface, section.sectionCoordinatesY[section.indLowerSurface])
 
        resampledSectionCoordinatesX = np.hstack([resampledSectionCoordinatesXUpperSurf, resampledSectionCoordinatesXLowerSurf])
        resampledSectionCoordinatesY = np.hstack([resampledSectionCoordinatesYUpperSurf, resampledSectionCoordinatesYLowerSurf])

        return resampledSectionCoordinatesX, resampledSectionCoordinatesY
        

