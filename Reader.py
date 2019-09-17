import os
import time
import pickle
from constants import *
from pygameWindow import PYGAME_WINDOW


class READER:
    def __init__(self):
        self.pygameWindow = PYGAME_WINDOW()
        self.Get_Number_Of_Gestures()
        self.xMin = -200.0
        self.xMax = 200.0
        self.yMin = -200.0
        self.yMax = 200.0


    def Print_Gestures(self):
        for fileNum in range(0, self.numGestures):
            pickleIn = open("userData/gesture"+str(fileNum)+".p", "rb")
            self.gestureData = pickle.load(pickleIn)
            print(self.gestureData)


    def Get_Number_Of_Gestures(self):
        paths, dirs, files = next(os.walk('userData'))
        self.numGestures = len(files)
        self.numGestures


    def Scale_XY(self, num, minimum, maximum, scalingMin, scalingMax):
        if (self.xMax == self.xMin) or (self.yMax == self.yMin):
            return 250
        else:
            return int(scalingMin + (num - minimum) * ((scalingMax - scalingMin) / (maximum - minimum)))


    def Draw_Gesture(self, gestureNum):
        for finger in range (0, 5):
            for bone in range(0, 4):
                currentBone = self.gestureData[finger, bone, :]

                ##storing data to variables##
                xBaseNotYetScaled = currentBone[0]
                yBaseNotYetScaled = currentBone[1]
                xTipNotYetScaled = currentBone[3]
                yTipNotYetScaled = currentBone[4]

                ##scaled base and tips ##
                xBase = self.Scale_XY(xBaseNotYetScaled, self.xMin, self.xMax, 0, pygameWindowWidth)
                yBase = self.Scale_XY(yBaseNotYetScaled , self.yMax, self.yMin, pygameWindowDepth, 0)
                xTip = self.Scale_XY(xTipNotYetScaled, self.yMax, self.yMin, pygameWindowDepth, 0)
                yTip = self.Scale_XY(yTipNotYetScaled, self.yMax, self.yMin, pygameWindowDepth, 0)
                self.pygameWindow.Draw_Line(xBase, yBase, xTip, yTip)

    def Draw_Gestures(self):
        while True:
           self.Draw_Each_Gestures_Once()


    def Draw_Each_Gestures_Once(self):
        for fileNum in range(0, self.numGestures):
            pickleIn = open("userData/gesture"+str(fileNum)+".p", "rb")
            self.gestureData = pickle.load(pickleIn)
            self.pygameWindow.Prepare()
            self.Draw_Gesture(fileNum)
            self.pygameWindow.Reveal()
            time.sleep(1)

