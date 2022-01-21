
from operator import truediv
import os

from numpy import transpose
from sectionLayout import sectionLayout
from trayectoryGenerator import trayectoryGenerator
from wingPanelLayout import wingPanelLayout
from geom3d import geom3d, plane3d, line3d
from machine import machine
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":

    sectionLayoutZplus = sectionLayout()
    sectionLayoutZplus.loadFromFile(os.path.join('data','profiles','sipkill1710b.dat'))
    sectionLayoutZplus.chord = 8.5*25.4
    sectionLayoutZplus.washoutAngle_deg = 0
    sectionLayoutZplus.templateHeight = 10

    sectionLayoutZminus = sectionLayout()
    sectionLayoutZminus.loadFromFile(os.path.join('data','profiles','MH60.dat'))
    sectionLayoutZminus.chord = 4.5*25.4
    sectionLayoutZminus.washoutAngle_deg = 3
    sectionLayoutZminus.templateHeight = 10

    wpl = wingPanelLayout()
    wpl.sectionPlusLayout = sectionLayoutZplus
    wpl.sectionPlusZposition = 600
    wpl.sectionPlusLeadingEdgeX = 0
    wpl.sectionMinusLayout = sectionLayoutZminus
    wpl.sectionMinusZposition = 100
    wpl.sectionMinusLeadingEdgeX = 350
    wpl.leadInDistance = 10
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
    tr.numPointsLowerSurface = 100
    tr.numPointUpperSurface = 100
    tr.generateTrayectory()

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