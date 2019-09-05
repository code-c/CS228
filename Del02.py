import sys

sys.path.insert(0, '..')

import Leap
import random
from constants import *
from pygameWindow import PYGAME_WINDOW
pygameWindow = PYGAME_WINDOW()
global x, y, xMin, xMax, yMin, yMax
xMin = 1000.0
xMax = -1000.0
yMin = 1000.0
yMax = -1000.0

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


def Handle_Frame(frame):
    global x, y, xMin, xMax, yMin, yMax
    hand = frame.hands[0]
    fingers = hand.fingers
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
    pygameX = Scale_XY(x, xMin, xMax, 0, pygameWindowWidth)
    pygameY = Scale_XY(y, yMin, yMax, pygameWindowDepth, 0)
    pygameWindow.Draw_Black_Circle(pygameX, pygameY)
    pygameWindow.Reveal()


