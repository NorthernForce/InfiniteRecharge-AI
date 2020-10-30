import cv2
import numpy as np

kernelOpen = np.ones((5,5))
kernelClose = np.ones((20,20))

def _getCoordsFromStartAndOffset(startCoords, offsets):
    x_bottom = (startCoords[0] + (0.5 * offsets[0]))
    y_bottom = (startCoords[1] + (0.5 * offsets[1]))
    return (x_bottom, y_bottom)

def _createImageMask(image_np, lowerBound=np.array([20, 100, 100]), upperBound=np.array([30, 255, 255])):
    imgHSV = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    return maskClose

def getCentralCoordsOfYellowFromImage(image_np):
    x_center, y_center = None, None

    maskedImage = _createImageMask(image_np)
    contours, height = cv2.findContours(maskedImage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for i in range(len(contours)):
        x_bottom, y_bottom, width, height = cv2.boundingRect(contours[i])
        cv2.rectangle(image_np, (x_bottom, y_bottom), (x_bottom + width, y_bottom + height), (252, 11, 0), 2)
        x_center, y_center = _getCoordsFromStartAndOffset((x_bottom, y_bottom), (width, height))
    return (x_center, y_center)