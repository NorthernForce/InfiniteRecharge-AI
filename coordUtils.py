# gives center coordinates of box in entire frame -> to be used for targetting
import cameraOffsetToAngle, cameraUtils
import numpy as np

MIN_SCORE_THRESH = 0

class BoxCentralCoordsGenerator:
    targetBoxArea = 0

    def get(self, boxes, scores):
        pts = []
        boxCenters = []
        for boxListIndexer in range(len(boxes)):
            score = np.squeeze(scores)
            if score[boxListIndexer] > MIN_SCORE_THRESH:
                if 
                box = np.squeeze(boxes)
                # there are 4 points in each rectangle target
                for boxNum in range(4):
                    scaledCoord = self.__scaleCoordsToFrameSize(box, boxNum, boxListIndexer)
                    pts.append(scaledCoord)
                trackingBox = PointBox(pts)
                self.targetBoxArea = trackingBox.getArea()

                # if target box is not too big, use it
                if (self.targetBoxArea < (0.5*(cameraUtils.CAP_WIDTH * cameraUtils.CAP_HEIGHT))):
                    center = trackingBox.getAbsoluteBoxCenter()
                    boxCenters.append(center)
            else:
                # default coords cannot be negative or None due to target finding algorithm
                noOffset = (9999, 9999)
                boxCenters.append(noOffset)
        return self.__getCentermostBoxCoords(boxCenters)

    def __scaleCoordsToFrameSize(self, box, boxNum, indexer):
        multiplier = None
        if (boxNum % 2 == 0):
            multiplier = cameraUtils.CAP_WIDTH
        else:
            multiplier = cameraUtils.CAP_HEIGHT
        coord = int(box[indexer,boxNum]*multiplier)
        return coord

    def getCoordsArea(self):
        return self.targetBoxArea

    def __getCentermostBoxCoords(self, boxCenters):
        x_offsets = []
        y_offsets = []
        closestTarget = None
        for point in boxCenters:
            offsetX, offsetY = cameraOffsetToAngle.FromPixels(point[0], point[1])
            # x_offsets is always positive because we want it to be close to the center (0)
            x_offsets.append(abs(offsetX))
            # y_offsets can be negative because smaller numbers = a closer target
            y_offsets.append(offsetY)
        x_smallestOffsetIndex = x_offsets.index(min(x_offsets))
        y_smallestOffsetIndex = y_offsets.index(min(y_offsets))
        
        # if multiple powercells, find the closest one to the robot
        if (y_smallestOffsetIndex < 5) and (x_smallestOffsetIndex < 15):
          closestTarget = y_smallestOffsetIndex
        else:
          closestTarget = x_smallestOffsetIndex
     
        return boxCenters[closestTarget]   

# creates a new abstract box from a list of 4 points
class PointBox:                                                                                                                                   
    def __init__(self, pts):
        self.x_min = pts[1]
        self.y_min = pts[0]
        self.x_max = pts[3]
        self.y_max = pts[2]

    def getArea(self):
        x_len = self.x_max - self.x_min
        y_len = self.y_max - self.y_min
        return (x_len * y_len)

    def getAbsoluteBoxCenter(self):
        x = (self.x_min + self.x_max) / 2
        y = (self.y_min + self.y_max) / 2
        return (x, y)

    def getPts(self):
        return self.x_min, self.y_min, self.x_max, self.y_max
