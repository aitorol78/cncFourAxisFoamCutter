

from machine import machine
from wingPanelLayout import wingPanelLayout
from geom3d import line3d, plane3d, geom3d
import numpy as np
import math

class trayectoryGenerator:
    def __init__(self):
        self.machine = machine()
        self.wpl = wingPanelLayout()

        self.numStationsUpperSurface = 100
        self.numStationsLowerSurface = 100

        self.sectionPlusResampledCoordinatesX = np.zeros(1)
        self.sectionPlusResampledCoordinatesY = np.zeros(1)
        self.sectionMinusResampledCoordinatesX = np.zeros(1)
        self.sectionMinusResampledCoordinatesY = np.zeros(1)

        self.sectionPlusEntryPointX = 0
        self.sectionPlusEntryPointY = 0
        self.sectionPlusExitPointX  = 0
        self.sectionPlusExitPointY  = 0
        self.sectionMinusEntryPoint = 0
        self.sectionMinusEntryPoint = 0
        self.sectionMinusExitPointX = 0
        self.sectionMinusExitPointY = 0

        self.sectionPlusTrayectoryX =  np.zeros(1)
        self.sectionPlusTrayectoryY =  np.zeros(1)
        self.sectionMinusTrayectoryX = np.zeros(1)
        self.sectionMinusTrayectoryY = np.zeros(1)

        self.wirePlusTrayectoryX = np.zeros(1)
        self.wirePlusTrayectoryY = np.zeros(1)
        self.wirePlusTrayectoryF = np.zeros(1)  # velocity
        self.wireMinusTrayectoryX = np.zeros(1)
        self.wireMinusTrayectoryY = np.zeros(1)
        self.wireMinusTrayectoryF = np.zeros(1)
    
    def generateTrayectory(self):

        self.wpl.sectionPlusLayout.computeSectionCoordinates()        
        self.wpl.sectionMinusLayout.computeSectionCoordinates()        

        # (done) profiles should have upper and lower surfaces
        #    easiest: profileSectionY > < 0 + points with x=xMin ( no x = xMax, profiles always have +- Y trailing edge points)
        # ¿WHY? I could consider just one curve -> NOP, the wire should get to the leading edge at the same time at both ends

        self.wpl.sectionPlusLayout.splitUpperLowerSurfaces()
        self.wpl.sectionMinusLayout.splitUpperLowerSurfaces()

        self.sectionPlusResampledCoordinatesX, self.sectionPlusResampledCoordinatesY = \
            self.resampleSectionPoints(self.wpl.sectionPlusLayout)

        self.sectionMinusResampledCoordinatesX, self.sectionMinusResampledCoordinatesY = \
            self.resampleSectionPoints(self.wpl.sectionMinusLayout)

        # for each surface
            # (done) calculate length of curve
            # (done) interpolate numPoints
            # (after xy in each end is calculated) compute velocities at each side
            # compute wire-surface distance compensation = f(wireDiameter, velocity ?)
            # compute compensated points
        
        # move points along X coordinate as defined in the wing layout
        self.sectionPlusResampledCoordinatesX = self.sectionPlusResampledCoordinatesX + self.wpl.sectionPlusLeadingEdgeX
        self.sectionMinusResampledCoordinatesX = self.sectionMinusResampledCoordinatesX + self.wpl.sectionMinusLeadingEdgeX
        
        # add entry and exit points 
        self.sectionPlusEntryPointX, self.sectionPlusEntryPointY = \
            self.computeEntryPoint(self.sectionPlusResampledCoordinatesX, self.sectionPlusResampledCoordinatesY, self.wpl.leadInDistance)
        self.sectionPlusExitPointX, self.sectionPlusExitPointY = \
            self.computeExitPoint(self.sectionPlusResampledCoordinatesX, self.sectionPlusResampledCoordinatesY, self.wpl.leadOutDistance)
        self.sectionMinusEntryPointX, self.sectionMinusEntryPointY = \
            self.computeEntryPoint(self.sectionMinusResampledCoordinatesX, self.sectionMinusResampledCoordinatesY, self.wpl.leadInDistance)
        self.sectionMinusExitPointX, self.sectionMinusExitPointY = \
            self.computeExitPoint(self.sectionMinusResampledCoordinatesX, self.sectionMinusResampledCoordinatesY, self.wpl.leadOutDistance)

        # compose the whole trayectory at panel sections
        self.sectionPlusTrayectoryX = np.hstack([self.sectionPlusEntryPointX,self.sectionPlusResampledCoordinatesX,self.sectionPlusExitPointX])
        self.sectionPlusTrayectoryY = np.hstack([self.sectionPlusEntryPointY,self.sectionPlusResampledCoordinatesY,self.sectionPlusExitPointY])
        self.sectionMinusTrayectoryX = np.hstack([self.sectionMinusEntryPointX,self.sectionMinusResampledCoordinatesX,self.sectionMinusExitPointX])
        self.sectionMinusTrayectoryY = np.hstack([self.sectionMinusEntryPointY,self.sectionMinusResampledCoordinatesY,self.sectionMinusExitPointY])

        # translate points to wire planes along the lines connecting Zplus and zPlus surfaces
        self.wirePlusTrayectoryX, self.wirePlusTrayectoryY = self.traslateTrayectoryToWirePlane( self.machine.wirePlusZpositon)
        self.wireMinusTrayectoryX, self.wireMinusTrayectoryY = self.traslateTrayectoryToWirePlane( self.machine.wireMinusZpositon)


    def resampleSectionPoints(self, section):
        newIndexes = np.linspace(min(section.indUpperSurface), max(section.indUpperSurface), self.numStationsUpperSurface)
        resampledSectionCoordinatesXUpperSurf = np.interp(newIndexes, section.indUpperSurface, section.sectionCoordinatesX[section.indUpperSurface])
        resampledSectionCoordinatesYUpperSurf = np.interp(newIndexes, section.indUpperSurface, section.sectionCoordinatesY[section.indUpperSurface])

        newIndexes = np.linspace(min(section.indLowerSurface), max(section.indLowerSurface), self.numStationsLowerSurface)
        resampledSectionCoordinatesXLowerSurf = np.interp(newIndexes, section.indLowerSurface, section.sectionCoordinatesX[section.indLowerSurface])
        resampledSectionCoordinatesYLowerSurf = np.interp(newIndexes, section.indLowerSurface, section.sectionCoordinatesY[section.indLowerSurface])
 
        resampledSectionCoordinatesX = np.hstack([resampledSectionCoordinatesXUpperSurf, resampledSectionCoordinatesXLowerSurf])
        resampledSectionCoordinatesY = np.hstack([resampledSectionCoordinatesYUpperSurf, resampledSectionCoordinatesYLowerSurf])

        return resampledSectionCoordinatesX, resampledSectionCoordinatesY
        
    def computeEntryPoint(self, profileX, profileY, distance):

        pointIn = np.array([[profileX[3]], [profileY[3]]])
        pointEdge = np.array([[profileX[0]], [profileY[0]]])
        direction = pointEdge - pointIn
        newPoint = pointEdge + direction * distance / np.linalg.norm(direction)

        return newPoint[0], newPoint[1]

    def computeExitPoint(self, profileX, profileY, distance):

        pointIn = np.array([[profileX[len(profileX)-4]], [profileY[len(profileY)-4]]])
        pointEdge = np.array([[profileX[len(profileX)-1]], [profileY[len(profileY)-1]]])
        direction = pointEdge - pointIn
        newPoint = pointEdge + direction * distance / np.linalg.norm(direction)

        return newPoint[0], newPoint[1]

    def traslateTrayectoryToWirePlane(self, wireZposition):
        numPoints = len(self.sectionPlusTrayectoryX)
        
        sectionPlusPoints3d = np.vstack([self.sectionPlusTrayectoryX, self.sectionPlusTrayectoryY, np.ones([1,numPoints])*self.wpl.sectionPlusZposition])
        sectionMinusPoints3d = np.vstack([self.sectionMinusTrayectoryX, self.sectionMinusTrayectoryY, np.ones([1,numPoints])*self.wpl.sectionMinusZposition])
        
        wirePlane = plane3d()
        wirePlane.point = np.array([[0],[0],[wireZposition]])
        wirePlane.normal = np.array([[0],[0],[1]])

        line = line3d()
        pointsXYZ = np.zeros([3,numPoints])
        for ii in range(numPoints):
            line.point = np.array([[sectionPlusPoints3d[0,ii]], [sectionPlusPoints3d[1,ii]], [sectionPlusPoints3d[2,ii]]])
            pointAux = np.array([[sectionMinusPoints3d[0,ii]], [sectionMinusPoints3d[1,ii]], [sectionMinusPoints3d[2,ii]]])
            line.direction = line.point -pointAux
            pointWire = geom3d.linePlaneToPoint(line, wirePlane)
            pointsXYZ[0,ii] = pointWire[0]
            pointsXYZ[1,ii] = pointWire[1]

        return pointsXYZ[0,:], pointsXYZ[1,:]