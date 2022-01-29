
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


# Tengo problemas de precision numerica en el empalme de los tramos:
#   puntos de entrada salida
#   (0,0) empalme superficie superior e inferior

flagMoveMachine = 1

if __name__ == "__main__":

    sectionLayoutZplus = sectionLayout()
    sectionLayoutZplus.loadFromFile(os.path.join('data','profiles','sipkill1710b.dat')) 
    sectionLayoutZplus.chord = 215 #8.5*25.4
    sectionLayoutZplus.washoutAngle_deg = 0
    sectionLayoutZplus.templateHeight = 0   

    sectionLayoutZminus = sectionLayout()
    sectionLayoutZminus.loadFromFile(os.path.join('data','profiles','ag25.dat'))
    sectionLayoutZminus.chord = 115 #4.5*25.4
    sectionLayoutZminus.washoutAngle_deg = 3
    sectionLayoutZminus.templateHeight = 0

    wpl = wingPanelLayout()
    wpl.sectionPlusLayout = sectionLayoutZplus
    wpl.sectionPlusZposition = 500
    wpl.sectionPlusLeadingEdgeX = 0
    wpl.sectionMinusLayout = sectionLayoutZminus
    wpl.sectionMinusZposition = 75
    wpl.sectionMinusLeadingEdgeX = 257
    wpl.leadInDistance = 20
    wpl.leadOutDistance = 20
    wpl.skinThickness = 0
    wpl.wireThickness = 0.7
    wpl.foamThickness = 0

    mch = machine()
    mch.wirePlusZpositon = 640
    mch.wireMinusZpositon = -30

    tr = trayectoryGenerator()

    tr.machine = mch
    tr.wpl = wpl
    tr.numStationsUpperSurface = 100
    tr.numStationsLowerSurface = 100
    tr.velocity = 125*5
    tr.generateTrayectory()
    tr.wirePlusTrayectoryX = tr.wirePlusTrayectoryX - tr.wirePlusTrayectoryX[0]
    tr.wirePlusTrayectoryY = tr.wirePlusTrayectoryY - tr.wirePlusTrayectoryY[0]
    tr.wireMinusTrayectoryX = tr.wireMinusTrayectoryX - tr.wireMinusTrayectoryX[0]
    tr.wireMinusTrayectoryY = tr.wireMinusTrayectoryY - tr.wireMinusTrayectoryY[0]
    tr.generateVelocityVectors()

    fig, axs = plt.subplots(2,2, sharex=False)
    axs[0,0].plot(tr.sectionMinusTrayectoryX, tr.sectionMinusTrayectoryY)
    axs[1,0].plot(tr.wireMinusTrayectoryX, tr.wireMinusTrayectoryY,'blue')
    axs[0,1].plot(tr.sectionPlusTrayectoryX, tr.sectionPlusTrayectoryY)
    axs[1,1].plot(tr.wirePlusTrayectoryX, tr.wirePlusTrayectoryY,'blue')

    fig, axs2 = plt.subplots(2,2, sharex=False)
    axs2[0,0].plot(tr.wireMinusTrayectoryX)
    axs2[1,0].plot(tr.wireMinusTrayectoryY)
    axs2[0,1].plot(tr.wirePlusTrayectoryX)
    axs2[1,1].plot(tr.wirePlusTrayectoryY)

    #tr.compensateWireThickness()

    axs[1,0].plot(tr.wireMinusTrayectoryX, tr.wireMinusTrayectoryY,'red')
    axs[1,1].plot(tr.wirePlusTrayectoryX, tr.wirePlusTrayectoryY,'red')
    plt.show()

    print('\n')
    print(('plus  initial Y (mm): {:.1f}').format(tr.wirePlusTrayectoryY[0]))
    print((  'minus initial Y (mm): {:.1f}').format(tr.wireMinusTrayectoryY[0]))
    print((  '(plus-minus) initial Y (mm): {:.1f}').format(tr.wirePlusTrayectoryY[0] - tr.wireMinusTrayectoryY[0]))
    print('\n')
    print(('plus   X travel (mm): {:.1f}').format( max(tr.wirePlusTrayectoryX) - min(tr.wirePlusTrayectoryX) ))
    print(('minus  X travel (mm): {:.1f}').format( max(tr.wireMinusTrayectoryX) - min(tr.wireMinusTrayectoryX) ))
    print('\n')
    print(('plus   Y travel (mm): {:.1f}').format( max(tr.wirePlusTrayectoryY) - min(tr.wirePlusTrayectoryY) ))
    print(('minus  Y travel (mm): {:.1f}').format( max(tr.wireMinusTrayectoryY) - min(tr.wireMinusTrayectoryY) ))
    print('\n')
    
    fig = plt.figure()    
    ax = fig.gca(projection='3d')
    ax.plot(tr.sectionPlusResampledCoordinatesX, tr.sectionPlusResampledCoordinatesY,  tr.wpl.sectionPlusZposition)
    #plt.hold(True)
    ax.plot(tr.sectionMinusResampledCoordinatesX, tr.sectionMinusResampledCoordinatesY, tr.wpl.sectionMinusZposition)
    ax.plot(tr.wirePlusTrayectoryX, tr.wirePlusTrayectoryY, tr.machine.wirePlusZpositon)
    ax.plot(tr.wireMinusTrayectoryX, tr.wireMinusTrayectoryY, tr.machine.wireMinusZpositon)
    ax.axis('equal')
    plt.xlabel('X')
    plt.ylabel('Y')
    #plt.zlabel('Z')
    plt.show(block=False)

    

    #print('ax.azim {}'.format(ax.azim)) # -89
    #print('ax.elev {}'.format(ax.elev)) # 114
    #print('ax.roll {}'.format(ax.roll))

    if flagMoveMachine:

        input('press a button to start moving')

        ex = trayectoryExecutor()
        ex.portPlus="/dev/ttyUSB1"
        ex.portMinus="/dev/ttyUSB0"
        ex.flagUsePlus = True
        ex.flagUseMinus = True
        ex.connectToServos()
        ex.sleepTimeAtFirstPoint = 1 # use 'ok' reply
        #tr.wirePlusTrayectoryX = tr.wirePlusTrayectoryX - tr.wirePlusTrayectoryX[0]
        #tr.wirePlusTrayectoryY = tr.wirePlusTrayectoryY - tr.wirePlusTrayectoryY[0]
        #tr.wireMinusTrayectoryX = tr.wireMinusTrayectoryX - tr.wireMinusTrayectoryX[0]
        #tr.wireMinusTrayectoryY = tr.wireMinusTrayectoryY - tr.wireMinusTrayectoryY[0]
        
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

    plt.show()
    