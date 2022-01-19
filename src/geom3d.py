
import numpy as np

class line3d:
    def __init__(self):
        point = np.array([[0],[0],[0]])
        direction = np.array([[0],[0],[0]])

class plane3d:
    def __init__(self):
        point = np.array([[0],[0],[0]])
        normal = np.array([[0],[0],[0]])

class geom3d:
    def twoPointsToLine(pointA, pointB):
        line = line3d()
        line.point = pointA
        line.direction = pointB - pointA
        return line

    def linePlaneToPoint(line, plane):
        denominator = np.matmul(np.transpose(line.direction), plane.normal)
        numerator = np.matmul(np.transpose(line.point - plane.point), plane.normal)
        point = line.point - line.direction * numerator / denominator
        return  point

        