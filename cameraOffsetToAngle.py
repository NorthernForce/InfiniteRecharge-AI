import realsenseUtils

FOV = 70
FOVoffset = FOV/2

width = realsenseUtils.RGB_CAP_WIDTH
height = realsenseUtils.RGB_CAP_HEIGHT

width_thresh = (width/2)+1
height_thresh = (height/2)+1

def FromPixels(x, y):
    max = (width/2)/FOVoffset
    angleX = 0
    angleY = 0

    # 9999 is a placeholder for no offset given
    if (x == 9999) and (y == 9999):
        angleX = 0
        angleY = 0

    elif (x < width_thresh) and (y < height_thresh):
        offsetX = -x
        offsetY = -y

        angleX = -FOVoffset + -(offsetX/max)
        angleY = -FOVoffset + -(offsetY/max)

    elif (x < width_thresh) and (y >= height_thresh):
        offsetX = -x
        offsetY = y-(height/2)
        
        angleX = -FOVoffset + -(offsetX/max)
        angleY = offsetY/-max

    elif (x >= width_thresh) and (y < height_thresh):
        offsetX = x-(width/2)
        offsetY = -y
        
        angleX = offsetX/max
        angleY = -FOVoffset + -(offsetY/max)

    elif (x >= (width/2)+1) and (y >= height_thresh):
        offsetX = x-(width/2)
        offsetY = y-(height/2)

        angleX = offsetX/max
        angleY = offsetY/-max

    return (angleX, angleY)
