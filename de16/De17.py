## Imports of everything needed
import sys
sys.path.insert(0, '../..')
import Leap
import random
import pickle
import time
import numpy as np
from constants import *
from pygameWindow import PYGAME_WINDOW

## setting constants that are needed in the program
pygameWindow = PYGAME_WINDOW()
global x, y, xMin, xMax, yMin, yMax, programState, position
xMin = -300.0
xMax = 300.0
yMin = -300.0
yMax = 300.0
programState = 0
Xposition = []
Yposition = []
center = False
numCenterFrames = 0

## load the data
clf = pickle.load( open('userData/classifier.p','rb'))
testData = np.zeros((1,30), dtype='f')


# scale the hand to the frame
def Scale_XY(num, minimum, maximum, scalingMin, scalingMax):
    if (xMax == xMin) or (yMax == yMin):
        return 125
    else:
        return int(scalingMin/2 + (num - minimum) * ((scalingMax/2 - scalingMin/2) / (maximum - minimum)))

# All below are the handlers for objects in the fram of the leap motion device
def Handle_Vector_From_Leap(v):
    x = v.x
    y = v.z
    pygameX = Scale_XY(x, xMin, xMax, 0, pygameWindowWidth)
    pygameY = Scale_XY(y, yMax, yMin, pygameWindowDepth, 0)
    return pygameX, pygameY

def Handle_Bone(bone, b):
    global Xposition, Yposition
    base = bone.prev_joint
    tip = bone.next_joint
    baseX, baseY = Handle_Vector_From_Leap(base)
    tipX, tipY = Handle_Vector_From_Leap(tip)
    pygameWindow.Draw_Black_Line(baseX, baseY, tipX, tipY, b)

    Xposition.append(tipX)
    Yposition.append(tipY)

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

#-------------------------------------------------------------------------------
# data camture and clean and comparision

# centering of the data
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

# zero state where there is no hand on the screen
def HandleState0(frame):
    global programState
    pygameWindow.Image()
    if not frame.hands.is_empty:
        programState = 1

# when there is a hand over the device it displays which way to move your hand
def HandleState1(frame):
    global programState, center
    Handle_Frame(frame)
    if not center:
        if 0 <= np.mean(Xposition) < ((pygameWindowWidth/4)-10): #the hand is left so move right
            pygameWindow.MoveRight()
            numCenterFrames = 0
        if ((pygameWindowWidth/4)+10) < np.mean(Xposition) <= pygameWindowWidth/2: #the hand is right so move left
            pygameWindow.MoveLeft()
            numCenterFrames = 0
        if 0 <= np.mean(Yposition) < ((pygameWindowDepth/4)-10): # the hand is high so move down
            pygameWindow.MoveDown()
            numCenterFrames = 0
        if ((pygameWindowDepth/4)+10) < np.mean(Yposition) <= (pygameWindowDepth/2): # the hand is low so move up
            pygameWindow.MoveUp()
            numCenterFrames = 0
        if (((pygameWindowDepth/4)-10) <= np.mean(Yposition) <= ((pygameWindowDepth/4)+10)) and (((pygameWindowWidth/4)-10) <= np.mean(Xposition) <= ((pygameWindowWidth/4)+10)):
            pygameWindow.Centered()
            numCenterFrames =+ 1
            if numCenterFrames  == 10:
                center = True
                programState = 2
    if frame.hands.is_empty:
        programState = 0

# when there is a centered hand over the frame we start our program
def HandleState2(frame):
    global testData
    guess = -1
    number = random.randrange(0,10,1)
    Handle_Frame(frame)
    pygameWindow.RandomNumber(number)
    pygameWindow.Numbers()
    while not guess == number:
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
            guess = clf.Predict(testData)



controller = Leap.Controller()

x = 250
y = 250


while True:
    frame = controller.frame()
    pygameWindow.Prepare()
    if programState == 0:
        HandleState0(frame)
    elif programState == 1:
        HandleState1(frame)
    elif programState == 2:
        HandleState2(frame)
    pygameWindow.Reveal()
