import sys
sys.path.insert(0, '..')
import Leap
import random
import pickle
import numpy as np
from constants import *
from pygameWindow_Del03 import PYGAME_WINDOW
pygameWindow = PYGAME_WINDOW()

class DELIVERABLE:
    def __init__(self):
        self.saves = 0
        self.controller = Leap.Controller()
        self.xMin = -200.0
        self.xMax = 200.0
        self.yMin = -200.0
        self.yMax = 200.0
        previousNumberOfHands = 0
        currentNumberOfHands = 0
        self.gestureData = np.zeros((5,4,6), dtype='f')

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

    def Handle_Bone(self, bone, b, fingerID):
        base = bone.prev_joint
        tip = bone.next_joint
        baseX, baseY = self.Handle_Vector_From_Leap(base)
        tipX, tipY = self.Handle_Vector_From_Leap(tip)
        pygameWindow.Draw_Line(baseX, baseY, tipX, tipY, b, self.currentNumberOfHands)
        if self.Recording_Is_Ending:
            self.gestureData[fingerID, b, 0] = base.x
            self.gestureData[fingerID, b, 1] = base.z
            self.gestureData[fingerID, b, 2] = base.y
            self.gestureData[fingerID, b, 3] = tip.x
            self.gestureData[fingerID, b, 4] = tip.z
            self.gestureData[fingerID, b, 5] = tip.y

    def Handle_Finger(self, finger, fingerID):
        for b in range(0,4):
            self.Handle_Bone(finger.bone(b), b, fingerID)

    def Handle_Frame(self, frame):
        hand = frame.hands[0]
        fingers = hand.fingers
        fingerID = 0
        for finger in fingers:
            self.Handle_Finger(finger, fingerID)
            fingerID += 1

        if self.Recording_Is_Ending():
            print(self.gestureData)
            self.Save_Gesture()

    def Run_Forever(self):
        while True:
           self.Run_Once()

    def Run_Once(self):
        frame = self.controller.frame()
        self.currentNumberOfHands = 0
        for hand in frame.hands:
            self.currentNumberOfHands += 1
        pygameWindow.Prepare()
        if not frame.hands.is_empty:
            self.Handle_Frame(frame)
        pygameWindow.Reveal()
        self.previousNumberOfHands = self.currentNumberOfHands

    def Recording_Is_Ending(self):
        if self.currentNumberOfHands == 1 and self.previousNumberOfHands == 2:
            return True
        else:
            return False

    def Save_Gesture(self):
        pickleOut = open("userData/gesture"+str(self.saves)+".p", "wb")
        pickle.dump(self.gestureData, pickleOut)
        pickleOut.close()
        self.saves += 1 

