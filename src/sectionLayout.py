import numpy as np
import math
from sectionProfile import sectionProfile

class sectionLayout(sectionProfile):
    def __init__(self):
        self.templateHeight = 10
        self.chord = 100
        self.washoutAngle_deg = 0
        self.flagInvertProfile = False # Y = -Y

        #self.thickness = 0
        #self.camber = 0
        #self.LEbalsa = 0

        self.sectionCoordinatesX = np.zeros(1)
        self.sectionCoordinatesY = np.zeros(1)

        self.indUpperSurface = np.zeros(1)
        self.indLowerSurface = np.zeros(1)

    def computeSectionCoordinates(self):
        profileChord = self.computeProfileChord()
        scale = self.chord / profileChord
        angle = self.washoutAngle_deg * math.pi / 180
        if self.flagInvertProfile:
            self.profileCoordinatesX = np.flip(self.profileCoordinatesX)
            self.profileCoordinatesY = -np.flip(self.profileCoordinatesY)
            angle = -angle
        rotationMatrix = np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
        pointsProfileDefinition = np.array([self.profileCoordinatesX, self.profileCoordinatesY])
        pointsLayout = np.matmul(scale * rotationMatrix, pointsProfileDefinition)

        self.sectionCoordinatesX = pointsLayout[0,:]                           # shape ?? 1xN   Nx1
        self.sectionCoordinatesY = pointsLayout[1,:] + self.templateHeight

    def computeProfileChord(self):
        return np.abs( np.max(self.profileCoordinatesX) - np.min(self.profileCoordinatesX) )

    def splitUpperLowerSurfaces(self):
        ind = np.argmin(self.profileCoordinatesX)
        self.indUpperSurface = range(0,ind)
        self.indLowerSurface = range(ind, len(self.profileCoordinatesX))

#    def computeLengthOfUpperSurface(self):
#        dx = np.diff(self.sectionCoordinatesX[self.indUpperSurface])
#        dy = np.diff(self.sectionCoordinatesY[self.indUpperSurface])
#        dsSq = np.multiply(dx, dx) + np.multiply(dy,dy)
#        ds = np.sqrt(dsSq)
#        S = sum(ds)
#        return S
#    def computeLengthOfLowerSurface(self):
#        dx = np.diff(self.sectionCoordinatesX[self.indLowerSurface])
#        dy = np.diff(self.sectionCoordinatesY[self.indLowerSurface])
#        dsSq = np.multiply(dx, dx) + np.multiply(dy,dy)
#        ds = np.sqrt(dsSq)
#        S = sum(ds)
#        return S

    #def interpolateProperlySpacedNPoints(self, numPoints):
        #np.interp(newIndex, index, vector)

    
