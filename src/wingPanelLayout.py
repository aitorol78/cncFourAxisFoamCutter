
from sectionLayout import sectionLayout

class wingPanelLayout:
    def __init__(self):
        self.sectionPlusLayout = sectionLayout()
        self.sectionPlusZposition = 0
        self.sectionPlusLeadingEdgeX = 0

        self.sectionMinusLayout = sectionLayout()
        self.sectionMinusZposition = 0
        self.sectionMinusLeadingEdgeX = 0
        
        self.leadInDistance = 20
        self.leadOutDistance = 20

        self.skinThickness = 0
        self.wireThickness = 0.2
        self.foamThickness = 0

    def methodTemplate(self):
        a = 77