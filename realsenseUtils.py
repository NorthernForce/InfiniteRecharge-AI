import pyrealsense2 as rs
import numpy as np

# settings
RGB_CAP_HEIGHT = 540
RGB_CAP_WIDTH = 960
RGB_CAP_FPS = 60
DEPTH_CAP_HEIGHT = 480
DEPTH_CAP_WIDTH = 848
DEPTH_CAP_FPS = 90
#

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, DEPTH_CAP_WIDTH, DEPTH_CAP_HEIGHT, rs.format.z16, DEP)
config.enable_stream(rs.stream.color, RGB_CAP_WIDTH, RGB_CAP_HEIGHT, rs.format.bgr8, RGB_CAP_FPS)
profile = pipeline.start(config)

inchesPerMeter = 39.37

def readRGBImage():
    frames = pipeline.wait_for_frames()
	colorFrame = frames.get_colorFrame()
	return np.asanyarray(colorFrame.get_data())

def readDepthAtPointInRGB(x, y):
    x_scaled = int((x / RGB_CAP_WIDTH) * DEPTH_CAP_WIDTH)
	y_scaled = int((y / RGB_CAP_HEIGHT) * DEPTH_CAP_HEIGHT)

	frames = pipeline.wait_for_frames()
	depthFrame = frames.get_depthFrame()
	return (depthFrame.get_distance(x_scaled, y_scaled) * inchesPerMeter)