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

# must import camera libraries (opencv) before tensorflow to avoid issues, common library problem
import cameraUtils, cv2

import tensorflow.compat.v1 as tf
from utils import label_map_util
from utils import visualization_utils as vis_util

# network tables for robot comms
import networktablesclient as nt
commClient = nt.commClient
import cameraOffsetToAngle

# setup HTTP mjpeg server for live viewing of image detections
from threading import Thread
from time import sleep
import mjpegserver

img_to_server = None
server_update_interval = 0.1

import coordUtils

def startImageServer():
    mjpegserver.start()
    while True:
        mjpegserver.stream.update(img_to_server)
        sleep(server_update_interval)
Thread(target=startImageServer, args=()).start()
  
# Frozen detection graph is used as model
PATH_TO_CKPT = "/home/dlinano/nvdli-nano/models/powercell_graph/frozen_inference_graph.pb"
 
# pbtxt file that contains list of classes
LABEL_PATH = "/home/dlinano/nvdli-nano/models/training/object-detection.pbtxt"

NUM_TOTAL_CLASSES = 1

# sets minimum threshold for valid object detection
MIN_SCORE_THRESH = 0.7
coordUtils.MIN_SCORE_THRESH = MIN_SCORE_THRESH

detectionGraph = None
def getTensor(name):
    tensor = detectionGraph.get_tensor_by_name(name)
    return tensor

def setupGraphAndModelCheckpoint():
    global detectionGraph
    detectionGraph = tf.Graph()
    with detectionGraph.as_default():
        graphDef = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, "rb") as fid:
            serialized_graph = fid.read()
            graphDef.ParseFromString(serialized_graph)
            tf.import_graph_def(graphDef, name='')

setupGraphAndModelCheckpoint()
label_map = label_map_util.load_labelmap(LABEL_PATH)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_TOTAL_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def RunAI(image_np):
    global img_to_server
    global server_update_interval
    server_update_interval = 0.1

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
    img_to_server = image_np
                    
    # get (x, y) from center of detected targets
    coords = coordUtils.BoxCentralCoordsGenerator()
    x_offset, y_offset = coords.get(boxes, scores)

    # Calculate angle offsets for tracking, and to validate targets
    x_offset_ang, y_offset_ang = cameraOffsetToAngle.FromPixels(x_offset, y_offset)
    Offsets = [x_offset_ang, y_offset_ang]

    # send whether there are valid targets to robot
    if (Offsets[0] != 0 or Offsets[1] != 0):
        commClient.SendValuePair("valid target:", 1)
    else:
        commClient.SendValuePair("valid target:", 0)

    # send camera offset angle to robot - angle=0 if no valid targets
    commClient.SendValueArray("PC Offset in AI Cam: ", Offsets)
    print("({}, {})".format(x_offset, y_offset))
    print("Angle Offset (X) in Cam: {}".format(x_offset_ang))

    commClient.SendValuePair("target area", coords.targetBoxArea)

    if (cameraUtils.CAM_ID != 0):
        commClient.SendValuePair("AI: IntakeOffsetX", x_offset)
    else:
        commClient.SendValuePair("AI: IntakeOffsetX", 9999)

with detectionGraph.as_default():
    with tf.Session(graph=detectionGraph) as sess:
        while True:
            ret, image_np = cameraUtils.cap.read()
            
            if (cameraUtils.CAM_ID == 1):
                image_np = cameraUtils.increaseYellow(image_np)

            if ((not cameraUtils.isChangingCamera) and ret):
                if (commClient.GetValueFrom("manualcam") == 1):
                    img_to_server = image_np
                    server_update_interval = 0.03
                else:
                    RunAI(image_np)
            cameraUtils.updateFeedToDesiredCamera()
