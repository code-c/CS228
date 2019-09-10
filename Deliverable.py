import sys
sys.path.insert(0, '..')
import Leap
import random
from constants import *
from pygameWindow_Del03 import PYGAME_WINDOW
pygameWindow = PYGAME_WINDOW()

class DELIVERABLE:
    def __init__(self):
        self.controller = Leap.Controller()
        self.xMin = -200.0
        self.xMax = 200.0
        self.yMin = -200.0
        self.yMax = 200.0

    def Scale_XY(self, num, minimum, maximum, scalingMin, scalingMax):
        if (self.xMax == self.xMin) or (self.yMax == self.yMin):
            return 250
        else:
            return int(scalingMin + (num - minimum) * ((scalingMax - scalingMin) / (maximum - minimum)))

    def Handle_Vector_From_Leap(self, v):
        x = v.x
        y = v.z
        pygameX = self.Scale_XY(x, self.xMin, self.xMax, 0, pygameWindowWidth)
        pygameY = self.Scale_XY(y, self.yMax, self.yMin, pygameWindowDepth, 0)
        return pygameX, pygameY

    def Handle_Bone(self, bone, b):
        base = bone.prev_joint
        tip = bone.next_joint
        baseX, baseY = self.Handle_Vector_From_Leap(base)
        tipX, tipY = self.Handle_Vector_From_Leap(tip)
        pygameWindow.Draw_Black_Line(baseX, baseY, tipX, tipY, b)

    def Handle_Finger(self, finger):
        for b in range(0,4):
            self.Handle_Bone(finger.bone(b), b)

    def Handle_Frame(self, frame):
        self.numberOfHands
        hand = frame.hands[0]
        fingers = hand.fingers
        for finger in fingers:
            self.Handle_Finger(finger)

    def Run_Forever(self):
        while True:
           self.Run_Once()
    def Run_Once(self):
        frame = self.controller.frame()
        pygameWindow.Prepare()
        if not frame.hands.is_empty:
            self.Handle_Frame(frame)
        pygameWindow.Reveal()

