import sys
# import folder paths to tensorflow utils
sys.path.append("/home/dlinano/nvdli-nano/models/research/object_detection/")
sys.path.append("/home/dlinano/nvdli-nano/models/research/")

import numpy as np
from PIL import Image

# prevent annoying info thrown from PIL
import logging
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)

# must import opencv before tensorflow to avoid issues, common library problem
import cv2
def getCapture(cameraID=0):
    return cv2.VideoCapture(cameraID)
cap = getCapture()

# sets tracking resolution
CAP_HEIGHT = 400
CAP_WIDTH = 300

import tensorflow.compat.v1 as tf
from utils import label_map_util
from utils import visualization_utils as vis_util

# network tables for robot comms
import networktablesclient as nt
commClient = nt.NetworkTablesClient()
import cameraOffsetToAngle

# setup HTTP mjpeg server for live viewing of image detections
from threading import Thread
from time import sleep
import mjpegserver
img_to_server = None

def startImageServer():
    mjpegserver.start()
    while True:
        mjpegserver.stream.update(img_to_server)
        sleep(0.1)
Thread(target=startImageServer, args=()).start()
  
# Frozen detection graph is used as model
PATH_TO_CKPT = "/home/dlinano/nvdli-nano/models/powercell_graph/frozen_inference_graph.pb"
 
# pbtxt file that contains list of classes
LABEL_PATH = "/home/dlinano/nvdli-nano/models/training/object-detection.pbtxt"

NUM_TOTAL_CLASSES = 1

# sets minimum threshold for valid object detection
MIN_SCORE_THRESH = 0.7

def getTensor(name):
    tensor = detectionGraph.get_tensor_by_name(name)
    return tensor

# setup graph & model checkpoint for inference detection
detectionGraph = tf.Graph()
with detectionGraph.as_default():
    graphDef = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, "rb") as fid:
        serialized_graph = fid.read()
        graphDef.ParseFromString(serialized_graph)
        tf.import_graph_def(graphDef, name='')
 
label_map = label_map_util.load_labelmap(LABEL_PATH)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_TOTAL_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# create a new box from a list of 4 points
class PointBox:                                                                                                                                   
    def __init__(self, pts):
        self.x_min = pts[1]
        self.y_min = pts[0]
        self.x_max = pts[3]
        self.y_max = pts[2]

    def getPts(self):
        return self.x_min, self.y_min, self.x_max, self.y_max

# gives center coordinates of box in entire frame -> to be used for targetting
class BoxCentralCoordsGenerator:
    def get(self, boxes):
        pts = []
        boxCenters = []
        for boxListIndexer in range(len(boxes)):
            score = np.squeeze(scores)
            if score[boxListIndexer] > MIN_SCORE_THRESH:
                box = np.squeeze(boxes)
                # there are 4 points in each square
                for boxNum in range(4):
                    scaledCoord = self.__scaleCoordsToFrameSize(box, boxNum, boxListIndexer)
                    pts.append(scaledCoord)
                trackingBox = PointBox(pts)
                center = self.__getTrueBoxCenter(trackingBox)
                boxCenters.append(center)
            else:
                # cannot be negative due to target finding algorithm
                noOffset = (9999, 9999)
                boxCenters.append(noOffset)
        return self.__getCentermostBoxCoords(boxCenters)

    def __scaleCoordsToFrameSize(self, box, boxNum, indexer):
        multiplier = None
        if (boxNum % 2 == 0):
            multiplier = CAP_WIDTH
        else:
            multiplier = CAP_HEIGHT
        coord = int(box[indexer,boxNum]*multiplier)
        return coord

    # returns the center of the box as coordinates on the entire plane
    def __getTrueBoxCenter(self, boxPts):
        x_min, y_min, x_max, y_max = boxPts.getPts()
        x = (x_min + x_max) / 2
        y = (y_min + y_max) / 2
        return (x, y)

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
        
        # find closest powercell to robot
        if (y_smallestOffsetIndex < 5) and (x_smallestOffsetIndex < 15):
          closestTarget = y_smallestOffsetIndex
        else:
          closestTarget = x_smallestOffsetIndex
     
        return boxCenters[closestTarget]   

    
with detectionGraph.as_default():
    with tf.Session(graph=detectionGraph) as sess:
        while True:
            ret, image_np = cap.read()

            # model expects images to be in this format: [1, None, None, 3]
            numpyImg = np.expand_dims(image_np, axis=0)
            image_tensor = getTensor("image_tensor:0")

            boxes = getTensor("detection_boxes:0")

            scores = getTensor("detection_scores:0")
            classes = getTensor("detection_classes:0")
            num_detections = getTensor("num_detections:0")

            # detect for items in predefined classes
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: numpyImg})

            # show results
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8,
                min_score_thresh=MIN_SCORE_THRESH)
            # cv2.imshow("detection feed", cv2.resize(image_np, (CAP_HEIGHT, CAP_WIDTH)))
            # streamUpdateThread = Thread(target=updateStream, args=(image_np,))
            # streamUpdateThread.start()
            img_to_server = image_np
                            
            # get (x, y) from center of detected targets
            coords = BoxCentralCoordsGenerator()
            x_offset, y_offset = coords.get(boxes)
            x_offset_ang, y_offset_ang = cameraOffsetToAngle.FromPixels(x_offset, y_offset)
            
            Offsets = [x_offset_ang, y_offset_ang]
            
            # send whether there are valid targets to robot
            if Offsets[0] or Offsets[1] != 0:
              commClient.SendValuePair("valid target:", 1)
            else:
              commClient.SendValuePair("valid target:", 0)

            # send camera offset angle to robot - angle=0 if no valid targets
            commClient.SendValueArray("PC Offset in AI Cam: ", Offsets)
            print("({}, {})".format(x_offset, y_offset))
            print("Angle Offset (X) in Cam: {}".format(x_offset_ang))
