
from sectionLayout import sectionLayout

class wingPanelLayout:
    def __init__(self):
        self.spSection = sectionLayout()
        self.spZposition = 0
        self.spleadingEdgeX = 0

        self.smSection = sectionLayout()
        self.smZposition = 0
        self.smleadingEdgeX = 0
        
        self.leadInDistance = 10
        self.leadOutDistance = 20

        self.skinThickness = 0
        self.wireThickness = 0.2
        self.foamThickness = 0

    def methodTemplate(self):
        a = 77