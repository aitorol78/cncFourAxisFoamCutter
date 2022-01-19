
from wingPanelLayout import wingPanelLayout
from geom3d import geom3d, line3d, plane3d

class machine:
    def __init__(self):
        self.wirePlusZpositon = 700
        self.wireMinusZpositon = 0

        self.wirePlusPlane = plane3d()
        self.wireMinusPlane = plane3d()

        self.sectionPlusPlane = plane3d()
        self.sectionMinusPlane = plane3d()

        wingPanel = wingPanelLayout()

    def computeWireCoordinates(self):





