import sys

sys.path.insert(0, '..')

import Leap
import random
from constants import *
from pygameWindow import PYGAME_WINDOW
pygameWindow = PYGAME_WINDOW()
global x, y, xMin, xMax, yMin, yMax
xMin = -200.0
xMax = 200.0
yMin = -200.0
yMax = 200.0

def Perturb_Circle_Position():
    x = random.randint(100, 400)
    y = random.randint(100, 400)
    fourSidedDieRoll = random.randint(1,4)

    if fourSidedDieRoll == 1:
        y = y - 1
    elif fourSidedDieRoll == 2:
        y = y + 1
    elif fourSidedDieRoll == 3:
        x = x - 1
    elif fourSidedDieRoll == 4:
        x = x + 1

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

controller = Leap.Controller()

x = 250
y = 250

while True:
    frame = controller.frame()
    pygameWindow.Prepare()
    if not frame.hands.is_empty:
        Handle_Frame(frame)
    #pygameWindow.Draw_Black_Circle(pygameX, pygameY)
    pygameWindow.Reveal()


