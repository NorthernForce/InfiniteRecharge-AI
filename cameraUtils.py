import cv2
import networktablesclient as nt
commClient = nt.commClient

# sets tracking resolution
CAP_HEIGHT = 288
CAP_WIDTH = 352
CAM_ID = 0

isChangingCamera = False
commClient.SendValuePair("AI Cam", CAM_ID);
cap = None

def switchCamera(cameraID):
    global cap
    if (cap is not None):
        cap.release()
    cv2.destroyAllWindows()
    cap = cv2.VideoCapture(cameraID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAP_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_HEIGHT)

def updateFeedToDesiredCamera():
    global CAM_ID
    isChangingCamera = True
    desiredCamID = int(commClient.GetValueFrom("AI Cam"))
    if (desiredCamID != CAM_ID):
        if (desiredCamID == 0):
            switchCamera(0)
        elif (desiredCamID == 1):
            switchCamera(1)
        CAM_ID = desiredCamID
    isChangingCamera = False

def increaseYellow(image_np):
    hsv = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)
    yellowMask = cv2.inRange(hsv, (51, 40, 70), (60, 100, 100))
    image_np[yellowMask == 255] = (0, 255, 0)
    return image_np

switchCamera(CAM_ID)