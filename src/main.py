
from operator import truediv
import os

from numpy import transpose
from sectionLayout import sectionLayout
from trayectoryGenerator import trayectoryGenerator
from trayectoryExecutor import trayectoryExecutor
from wingPanelLayout import wingPanelLayout
from geom3d import geom3d, plane3d, line3d
from machine import machine
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":

    sectionLayoutZplus = sectionLayout()
    sectionLayoutZplus.loadFromFile(os.path.join('data','profiles','ag25.dat')) 
    sectionLayoutZplus.chord = 50
    sectionLayoutZplus.washoutAngle_deg = 0
    sectionLayoutZplus.templateHeight = 0   

    sectionLayoutZminus = sectionLayout()
    sectionLayoutZminus.loadFromFile(os.path.join('data','profiles','ag25.dat'))
    sectionLayoutZminus.chord = 50
    sectionLayoutZminus.washoutAngle_deg = 0
    sectionLayoutZminus.templateHeight = 0

    wpl = wingPanelLayout()
    wpl.sectionPlusLayout = sectionLayoutZplus
    wpl.sectionPlusZposition = 600
    wpl.sectionPlusLeadingEdgeX = 0
    wpl.sectionMinusLayout = sectionLayoutZminus
    wpl.sectionMinusZposition = 100
    wpl.sectionMinusLeadingEdgeX = 0
    wpl.leadInDistance = 0
    wpl.leadOutDistance = 20
    wpl.skinThickness = 0
    wpl.wireThickness = 0.2
    wpl.foamThickness = 0

    mch = machine()
    mch.wirePlusZpositon = 700
    mch.wireMinusZpositon = 0

    tr = trayectoryGenerator()

    tr.machine = mch
    tr.wpl = wpl
    tr.numStationsUpperSurface = 100
    tr.numStationsLowerSurface = 100
    tr.velocity = 1000
    tr.generateTrayectory()
    tr.generateVelocityVectors()

    ex = trayectoryExecutor()
    ex.portPlus="/dev/ttyUSB1"
    ex.portMinus="/dev/ttyUSB0"
    ex.flagUsePlus = True
    ex.flagUseMinus = True
    ex.connectToServos()
    ex.sleepTimeAtFirstPoint = 5
    tr.wirePlusTrayectoryX = tr.wirePlusTrayectoryX - tr.wirePlusTrayectoryX[0]
    tr.wirePlusTrayectoryY = tr.wirePlusTrayectoryY - tr.wirePlusTrayectoryY[0]
    tr.wireMinusTrayectoryX = tr.wireMinusTrayectoryX - tr.wireMinusTrayectoryX[0]
    tr.wireMinusTrayectoryY = tr.wireMinusTrayectoryY - tr.wireMinusTrayectoryY[0]
    ex.goToFirstPoint(tr)
    ex.waitAtFirstPoint()
    ex.followTrayectoryFromSecondPoint(tr)

    #fig, axs = plt.subplots(4, 1, sharex=True, sharey=False)
    #fig.suptitle('section profile')
    #axs[0].plot(sectionLayoutZplus.sectionCoordinatesX, sectionLayoutZplus.sectionCoordinatesY, marker='o')
    #axs[0].grid()
    #axs[0].axis('equal')
    #axs[0].set_xlabel("X (mm)")
    #axs[0].set_ylabel("Y (mm)")
#
    #axs[1].plot(tr.sectionPlusResampledCoordinatesX, tr.sectionPlusResampledCoordinatesY, marker='o')
    #axs[1].grid()
    #axs[1].axis('equal')
    #axs[1].set_xlabel("X (mm)")
    #axs[1].set_ylabel("Y (mm)")
#
    #axs[2].plot(sectionLayoutZminus.sectionCoordinatesX, sectionLayoutZminus.sectionCoordinatesY, marker='o')
    #axs[2].grid()
    #axs[2].axis('equal')
    #axs[2].set_xlabel("X (mm)")
    #axs[2].set_ylabel("Y (mm)")
#
    #axs[3].plot(tr.sectionMinusResampledCoordinatesX, tr.sectionMinusResampledCoordinatesY, marker='o')
    #axs[3].grid()
    #axs[3].axis('equal')
    #axs[3].set_xlabel("X (mm)")
    #axs[3].set_ylabel("Y (mm)")
    #plt.show()

    
    fig = plt.figure()    
    ax = fig.gca(projection='3d')
    ax.plot(tr.sectionPlusResampledCoordinatesX, tr.sectionPlusResampledCoordinatesY,  tr.wpl.sectionPlusZposition)
    plt.hold(True)
    ax.plot(tr.sectionMinusResampledCoordinatesX, tr.sectionMinusResampledCoordinatesY, tr.wpl.sectionMinusZposition)
    ax.plot(tr.wirePlusTrayectoryX, tr.wirePlusTrayectoryY, tr.machine.wirePlusZpositon)
    ax.plot(tr.wireMinusTrayectoryX, tr.wireMinusTrayectoryY, tr.machine.wireMinusZpositon)
    ax.axis('equal')
    plt.xlabel('X')
    plt.ylabel('Y')
    #plt.zlabel('Z')
    plt.show()
    print('ax.azim {}'.format(ax.azim)) # -89
    print('ax.elev {}'.format(ax.elev)) # 114
    #print('ax.roll {}'.format(ax.roll))