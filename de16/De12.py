import sys

sys.path.insert(0, '../..')

import Leap
import random
import pickle
import numpy as np
from constants import *
from pygameWindow import PYGAME_WINDOW
pygameWindow = PYGAME_WINDOW()
global x, y, xMin, xMax, yMin, yMax
xMin = -200.0
xMax = 200.0
yMin = -200.0
yMax = 200.0
clf = pickle.load( open('userData/classifier.p','rb'))
testData = np.zeros((1,30), dtype='f')


def Scale_XY(num, minimum, maximum, scalingMin, scalingMax):
    if (xMax == xMin) or (yMax == yMin):
        return 250
    else:
        return int(scalingMin + (num - minimum) * ((scalingMax - scalingMin) / (maximum - minimum)))

def Handle_Vector_From_Leap(v):
    x = v.x
    y = v.z
    pygameX = Scale_XY(x, xMin, xMax, 0, pygameWindowWidth)
    pygameY = Scale_XY(y, yMax, yMin, pygameWindowDepth, 0)
    return pygameX, pygameY

def Handle_Bone(bone, b):
    base = bone.prev_joint
    tip = bone.next_joint
    baseX, baseY = Handle_Vector_From_Leap(base)
    tipX, tipY = Handle_Vector_From_Leap(tip)
    pygameWindow.Draw_Black_Line(baseX, baseY, tipX, tipY, b)
    
def Handle_Finger(finger):
    for b in range(0,4):
        Handle_Bone(finger.bone(b), b)

def Handle_Frame(frame):
    global x, y, xMin, xMax, yMin, yMax
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        Handle_Finger(finger)

    indexFingerList = fingers.finger_type(fingers[0].TYPE_INDEX)
    indexFinger = indexFingerList[0]
    distalPhalanx = indexFinger.bone(2)
    tip = distalPhalanx.next_joint
    x = int(tip.x)
    y = int(tip.y)
    if (x < xMin):
        xMin = x
    if (x > xMax):
        xMax = x
    if (y < yMin):
        yMin = y
    if (y > yMax):
        yMax = y


def centerData(data):
    allXCoordinates = data[0,::3]
    meanXValue = allXCoordinates.mean()
    data[0,::3] = allXCoordinates - meanXValue
   
    allYCoordinates = data[0,1::3]
    meanYValue = allYCoordinates.mean()
    data[0,1::3] = allYCoordinates - meanYValue
   
    allZCoordinates = data[0,2::3]
    meanZValue = allZCoordinates.mean()
    data[0,2::3] = allZCoordinates - meanZValue
  
    return data


controller = Leap.Controller()

x = 250
y = 250


while True:
    frame = controller.frame()
    if (len(frame.hands)>0):
        k = 0
        fingers = frame.hands[0].fingers
        for finger in fingers:
            for b in range(0, 4):
                bone = finger.bone(b)
                tip = bone.next_joint
                xTip = tip.x
                yTip = tip.z
                zTip = tip.y

                if ((b==0) or (b==3)):
                    testData[0,k] = xTip
                    testData[0, k+1] = yTip
                    testData[0, k+2] = zTip
                    k = k + 3
        testData = centerData(testData)
        predictClass = clf.Predict(testData)
        print(predictClass)
    pygameWindow.Prepare()
    if not frame.hands.is_empty:
        Handle_Frame(frame)
    #pygameWindow.Draw_Black_Circle(pygameX, pygameY)
    pygameWindow.Reveal()


