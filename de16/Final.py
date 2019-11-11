## Imports of everything needed
import sys
sys.path.insert(0, '../..')
import Leap
import random
import pickle
import time
import numpy as np
from constants import *
from collections import Counter
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
countedFrame = 0
number = -1
correctNum = 0

## load the data
clf = pickle.load(open('userData/classifier.p','rb'))
testData = np.zeros((1,30), dtype='f')
database = pickle.load(open('userData/database.p', 'rb'))


###### ----- Functions --------- #########

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

def getScores():
    global database
    ratioDict = {}
    for user in database:
        usrRatio = database[user]['TotalRatio']
        #'{:.3f}'.format(usrRatio)
        ratioDict.update({user: usrRatio})
    k = Counter(ratioDict)
    highScores = k.most_common(3)
    return highScores



def initializeDict():
    global database, userName
    userRecord =  database[userName]
    if userRecord['logins'] > 1:
        userRecord['prevFails'] = userRecord['fails']
        userRecord['prevSuccess'] = userRecord['success']
        if float(userRecord['prevSuccess'])/float(userRecord['success']) > float(userRecord['success'])/float(userRecord['fails']):
            userRecord['TotalRatio'] =float(userRecord['prevSuccess'])/float(userRecord['success'])
        else:
            userRecord['TotalRatio'] = float(userRecord['success'])/float(userRecord['fails'])
    else:
        for i in range(0,10):
            userRecord['digit'+str(i)+'attempted'] = 0
            userRecord['digit'+str(i)+'correct'] = 0
            userRecord['prevFails'] = 0
            userRecord['prevSuccess'] = 0
        userRecord['TotalRatio'] = 0
    userRecord['fails'] = 0
    userRecord['success'] = 0

def UpdateNumOfAttempts(num):
    global database, userName
    userRecord =  database[userName]
    userRecord['fails'] += 1
    if num == 0:
        if userRecord['digit0attempted'] == 1:
            userRecord['digit0attempted'] += 1
        else:
            userRecord['digit0attempted'] = 1
    elif num == 1:
        if userRecord['digit1attempted'] == 1:
            userRecord['digit1attempted'] += 1
        else:
            userRecord['digit1attempted'] = 1
    elif num == 2:
        if userRecord['digit2attempted'] == 1:
            userRecord['digit2attempted'] += 1
        else:
            userRecord['digit2attempted'] = 1
    elif num == 3:
        if userRecord['digit3attempted'] == 1:
            userRecord['digit3attempted'] += 1
        else:
            userRecord['digit3attempted'] = 1
    elif num == 4:
        if userRecord['digit4attempted'] == 1:
            userRecord['digit4attempted'] += 1
        else:
            userRecord['digit4attempted'] = 1
    elif num == 5:
        if userRecord['digit5attempted'] == 1:
            userRecord['digit5attempted'] += 1
        else:
            userRecord['digit5attempted'] = 1
    elif num == 6:
        if userRecord['digit6attempted'] == 1:
            userRecord['digit6attempted'] += 1
        else:
            userRecord['digit6attempted'] = 1
    elif num == 7:
        if userRecord['digit7attempted'] == 1:
            userRecord['digit7attempted'] += 1
        else:
            userRecord['digit7attempted'] = 1
    elif num == 8:
        if userRecord['digit8attempted'] == 1:
            userRecord['digit8attempted'] += 1
        else:
            userRecord['digit8attempted'] = 1
    elif num == 9:
        if userRecord['digit9attempted'] == 1:
            userRecord['digit9attempted'] += 1
        else:
            userRecord['digit9attempted'] = 1

def UpdateCorrect(num):
    global database, userName
    userRecord =  database[userName]
    userRecord['success'] += 1
    if num == 0:
        if userRecord['digit0correct'] == 1:
            userRecord['digit0correct'] += 1
        else:
            userRecord['digit0correct'] = 1
    elif num == 1:
        if userRecord['digit1correct'] == 1:
            userRecord['digit1correct'] += 1
        else:
            userRecord['digit1correct'] = 1
    elif num == 2:
        if userRecord['digit2correct'] == 1:
            userRecord['digit2correct'] += 1
        else:
            userRecord['digit2correct'] = 1
    elif num == 3:
        if userRecord['digit3correct'] == 1:
            userRecord['digit3correct'] += 1
        else:
            userRecord['digit3correct'] = 1
    elif num == 4:
        if userRecord['digit4correct'] == 1:
            userRecord['digit4correct'] += 1
        else:
            userRecord['digit4correct'] = 1
    elif num == 5:
        if userRecord['digit5correct'] == 1:
            userRecord['digit5correct'] += 1
        else:
            userRecord['digit5correct'] = 1
    elif num == 6:
        if userRecord['digit6correct'] == 1:
            userRecord['digit6correct'] += 1
        else:
            userRecord['digit6correct'] = 1
    elif num == 7:
        if userRecord['digit7correct'] == 1:
            userRecord['digit7correct'] += 1
        else:
            userRecord['digit7correct'] = 1
    elif num == 8:
        if userRecord['digit8correct'] == 1:
            userRecord['digit8correct'] += 1
        else:
            userRecord['digit8correct'] = 1
    elif num == 9:
        if userRecord['digit9correct'] == 1:
            userRecord['digit9correct'] += 1
        else:
            userRecord['digit9correct'] = 1

def DetermineNum():
    global database, userName
    userRecord =  database[userName]
    numbers = range(0,10)
    i = 0
    succRate = {}

    for num in numbers:
        succRate[num] = float(userRecord['digit'+str(num)+'correct']+1)/float(userRecord['digit'+str(num)+'attempted']+1)

    while i != 9:
        if succRate[i]/100 <= .75 and number != i:
            return i
        else:
            i += 1

    return 0

def DetermineHelp(number):
    global database, userName
    userRecord =  database[userName]
    numbers = range(0,10)
    succRate = {}

    for num in numbers:
        succRate[num] = float(userRecord['digit'+str(num)+'correct'])/float(userRecord['digit'+str(num)+'attempted'])

    if succRate[number] < .30:
        pygameWindow.RandomNumber(number)
        pygameWindow.Numbers()
    elif .30 <= succRate[number] <= .75:
        pygameWindow.RandomNumber(number)
        pygameWindow.Numbers() #take it away hopefully
    elif .75< succRate[number]:
        pygameWindow.RandomNumber(number)
    return 0

# zero state where there is no hand on the screen
def HandleState0(frame):
    global programState
    pygameWindow.Image()
    if not frame.hands.is_empty:
        programState = 1

# when there is a hand over the device it displays which way to move your hand
def HandleState1(frame):
    global programState, center, numCenterFrames
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
            numCenterFrames = numCenterFrames + 1
            if numCenterFrames  == 10:
                center = True
                programState = 2
    if frame.hands.is_empty:
        programState = 0

# when there is a centered hand over the frame we start our program
def HandleState2(frame):
    global testData, countedFrame, number, correctNum
    guess = -1
    if ((countedFrame == 0) or (countedFrame == 30)):
        number = DetermineNum() #replaces random numbers and goes in order just about
        if (countedFrame == 30):
            countedFrame = 0
            correctNum = 0
    pygameWindow.RandomNumber(number)
    Handle_Frame(frame)
    # DetermineHelp(number) #replaces the two lines below
    #pygameWindow.RandomNumber(number)
    pygameWindow.Numbers()

    #first time seeing this number again
    if countedFrame == 0:
        UpdateNumOfAttempts(number)

    if (len(frame.hands)>0):
        countedFrame += 1
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

        # if we got it right then udate db and set counter to 0
        if guess == number:
            correctNum +=1
            pygameWindow.warm()
            if correctNum == 10:
                UpdateCorrect(number)
                countedFrame = 0
                correctNum = 0
        else:
            pygameWindow.cold()
    # guessed the number right so we go back and dump our data in
    pickle.dump(database, open('userData/database.p', 'wb'))
    if frame.hands.is_empty:
        programState = 0



controller = Leap.Controller()

x = 250
y = 250

############## ------------- START --------------- ################

userName = raw_input('Please enter your name: ')
if userName in database:
    print('Welcome back ' + userName + '.')
    userRecord =  database[userName]
    database[userName]['logins'] += 1
    initializeDict()
else:
    database[userName] = {}
    database[userName].update({'logins' : 1})
    userRecord =  database[userName]
    initializeDict()
    print('Welcome ' + userName + '.')

preF = userRecord['prevFails']
preS = userRecord['prevSuccess']
highScores = getScores()

while True:
    frame = controller.frame()
    pygameWindow.Prepare()
    curS = userRecord['success']
    curF = userRecord['fails']
    pygameWindow.showProgress(curS,curF,preS,preF)
    pygameWindow.showScores(highScores)
    if programState == 0:
        HandleState0(frame)
    elif programState == 1:
        HandleState1(frame)
    elif programState == 2:
        HandleState2(frame)
    pygameWindow.Reveal()
