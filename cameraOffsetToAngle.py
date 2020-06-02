FOV = 60
FOVoffset = FOV/2

def FromPixels(x, y):
    max = 112/FOVoffset
    angleX = 0
    angleY = 0

    # -1 is a placeholder for no offset given
    if (x == -1) and (y == -1):
        angleX = 0
        angleY = 0

    elif (x < 113) and (y < 113):
        offsetX = -x
        offsetY = -y

        angleX = -FOVoffset + -(offsetX/max)
        angleY = -FOVoffset + -(offsetY/max)

    elif (x < 113) and (y >= 113):
        offsetX = -x
        offsetY = y-112
        
        angleX = -FOVoffset + -(offsetX/max)
        angleY = offsetY/-max

    elif (x >= 113) and (y < 113):
        offsetX = x-112
        offsetY = -y
        
        angleX = offsetX/max
        angleY = -FOVoffset + -(offsetY/max)

    elif (x >= 113) and (y >= 113):
        offsetX = x-112
        offsetY = y-112

        angleX = offsetX/max
        angleY = offsetY/-max

    return (angleX, angleY)
