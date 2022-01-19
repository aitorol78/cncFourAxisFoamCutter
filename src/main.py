
import os
from sectionLayout import sectionLayout
from geom3d import geom3d, plane3d, line3d
import matplotlib.pyplot as plt

if __name__ == "__main__":

    fileName = os.path.join('data','profiles','ag25.dat')
    #sectionZplus = sectionProfile()
    #sectionZplus.loadFromFile(fileName)

    sectionLayoutZplus = sectionLayout()
    sectionLayoutZplus.loadFromFile(fileName)
    sectionLayoutZplus.chord = 230
    sectionLayoutZplus.washoutAngle_deg = 3
    sectionLayoutZplus.templateHeight = 10
    sectionLayoutZplus.computeCoordinates()

    fig, axs = plt.subplots(2, 1, sharex=True, sharey=False)
    fig.suptitle('section profile')
    axs[0].plot(sectionLayoutZplus.sectionCoordinatesX, sectionLayoutZplus.sectionCoordinatesY)
    axs[0].grid()
    axs[0].axis('equal')
    axs[0].set_xlabel("X (mm)")
    axs[0].set_ylabel("Y (mm)")
    plt.show()


    a = 3
