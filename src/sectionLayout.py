
import numpy as np
import math
from sectionProfile import sectionProfile

class sectionLayout(sectionProfile):
    def __init__(self):
        self.templateHeight = 10
        self.chord = 100
        self.washoutAngle_deg = 0

        #self.thickness = 0
        #self.camber = 0
        #self.LEbalsa = 0

        self.sectionCoordinatesX = np.zeros(1)
        self.sectionCoordinatesY = np.zeros(1)

    def computeCoordinates(self):
        profileChord = self.computeProfileChord()
        scale = self.chord / profileChord
        angle = self.washoutAngle_deg * math.pi / 180
        rotationMatrix = np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
        
        pointsProfileDefinition = np.array([self.profileCoordinatesX, self.profileCoordinatesY])
        pointsLayout = np.matmul(scale * rotationMatrix, pointsProfileDefinition)

        self.sectionCoordinatesX = pointsLayout[0,:]                           # shape ?? 1xN   Nx1
        self.sectionCoordinatesY = pointsLayout[1,:] + self.templateHeight

    def computeProfileChord(self):
        return np.abs( np.max(self.profileCoordinatesX) - np.min(self.profileCoordinatesX) )