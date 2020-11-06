import cv2, cameraUtils
import numpy as np
from math import sqrt
from more_itertools import sort_together

class CoordinateBox:
	def __init__(self, mins, maxes):
		"""init"""
		self.x_min = mins[0]
		self.y_min = mins[1]
		self.x_max = maxes[0]
		self.y_max = maxes[1]
		self.x_center, self.y_center = self.getAbsoluteBoxCenter()
		self.ratio_of_image = self._getRatioOfImage()
	
	def _getRatioOfImage(self):
		self.width, self.height = self.getWidthAndHeightFromMinsAndMaxes((self.x_min, self.y_min), (self.x_max, self.y_max))
		box_area = self.height * self.width
		total_area = cameraUtils.CAP_HEIGHT * cameraUtils.CAP_WIDTH
		return (box_area / total_area)

	def setDistances(self, distances):
		self.distances = distances
		self.avgOfDistances = sum(distances) / len(distances)

	def getAbsoluteBoxCenter(self):
		x = (self.x_min + self.x_max) / 2
		y = (self.y_min + self.y_max) / 2
		return (x, y)

	@staticmethod
	def getEndCoordsFromStartAndDist(mins, dists):
		maxes = []
		maxes.insert(0, (mins[0] + dists[0]))
		maxes.insert(1, (mins[1] + dists[1]))
		return maxes

	@staticmethod
	def getWidthAndHeightFromMinsAndMaxes(mins, maxes):
		width = maxes[0] - mins[0]
		height = maxes[1] - mins[1]
		return (width, height)

def _sortBoxesByArea(boxes):
	ratios = []
	boxesByArea = []
	for box in boxes:
		ratios.append(box.ratio_of_image)

	boxesByAreaSmToLg = sort_together([ratios, boxes])[1]

	boxesByAreaLgToSm = list(reversed(boxesByAreaSmToLg))
	return boxesByAreaLgToSm

def _getDistanceFromBoxToAllOthers(boxNum, boxes):
	distances = []
	for box2 in boxes:
		distances.append(sqrt((box2.x_center - boxes[boxNum].x_center)**2 + (box2.y_center - boxes[boxNum].y_center)**2))
	return distances

def _removeOutlyingBoxes(boxes):
	numOfBoxes = len(boxes)
	avgDistsForBoxes = []
	boxesToRemove = []
	for box in boxes:
		avgDistsForBoxes.append(box.avgOfDistances)
	avgDistBetweenAllBoxes = sum(avgDistsForBoxes) / len(avgDistsForBoxes)

	for i in range(len(boxes)):
		areaBias = 1 / (1+boxes[i].ratio_of_image)
		if (avgDistsForBoxes[i] * areaBias) > avgDistBetweenAllBoxes:
			boxesToRemove.append(i)
	for index in boxesToRemove:
		try:
			boxes.pop(index)
		except:
			pass

	return boxes

def calculateDistanceOfEachBoxToAllOthers(boxes):
	boxesByArea = _sortBoxesByArea(boxes)
	# distances to each point are correspond to the same box indexes as in boxesByArea
	for i in range(len(boxesByArea)):
		distances = _getDistanceFromBoxToAllOthers(i, boxesByArea)
		boxesByArea[i].setDistances(distances)
	
def getClusterBoxFromCloseBoxes(boxes):
		x_mins, y_mins, x_maxes, y_maxes = [], [], [], []
		if len(boxes) > 1:
			boxes = _removeOutlyingBoxes(boxes)
		for box in boxes:
			x_mins.append(box.x_min)
			y_mins.append(box.y_min)
			x_maxes.append(box.x_max)
			y_maxes.append(box.y_max)
		return CoordinateBox((min(x_mins), min(y_mins)), (max(x_maxes), max(y_maxes)))

kernelOpen = np.ones((5,5))
kernelClose = np.ones((20,20))

def _createImageMask(image_np, lowerBound=np.array([20, 100, 100]), upperBound=np.array([50, 255, 255])):
	imgHSV = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)
	imgHSV[...,2] = imgHSV[...,2] * 0.9
	yellow_mask = cv2.inRange(imgHSV, lowerBound, upperBound)
	maskOpen = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernelOpen)
	maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

	return maskClose

def getCentralCoordsOfYellowFromImage(image_np):
	detectionBoxes = []

	maskedImage = _createImageMask(image_np)
	contours, h = cv2.findContours(maskedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	for i in range(len(contours)):
		x_min, y_min, width, height = cv2.boundingRect(contours[i])
		cv2.rectangle(image_np, (x_min, y_min), (x_min + width, y_min + height), (230, 11, 0), 2)
		x_max, y_max = CoordinateBox.getEndCoordsFromStartAndDist((x_min, y_min), (width, height))
		detectionBoxes.append(CoordinateBox((x_min, y_min), (x_max, y_max)))

	if not contours:
		return (9999, 9999)
	else:
		calculateDistanceOfEachBoxToAllOthers(detectionBoxes)
		clusterBox = getClusterBoxFromCloseBoxes(detectionBoxes)
		cv2.rectangle(image_np, (clusterBox.x_min, clusterBox.y_min), (clusterBox.x_max, clusterBox.y_max), (11, 252, 0), 2)
		return clusterBox.getAbsoluteBoxCenter()