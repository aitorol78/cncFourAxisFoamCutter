
import numpy as np
import pandas as pd

class sectionProfile:
    def __init__(self):
        self.fileName = ''
        self.name = ''
        self.profileCoordinatesX = np.zeros(1)
        self.profileCoordinatesY = np.zeros(1)
    
    def loadFromFile(self, fileName):
        self.fileName = fileName
        self.name = 'ToDo rename profile'
        #data = pd.read_csv(self.fileName, sep=' ', delimiter=None, header='infer', names=None, index_col=None)
        data = pd.read_csv(self.fileName, sep=r'\s+', header=0)
        self.profileCoordinatesX = data.values[:,0].tolist()
        self.profileCoordinatesY = data.values[:,1].tolist()

