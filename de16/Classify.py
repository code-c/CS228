import numpy as np
import pickle
from knn import KNN


### IMPORTING DATA ###

trainList = []
testList = []

def flipHand(dataSet):
    allZCoordinates = dataSet[:,:,5,:]
    allFlippedZCoordinates = 0 - allZCoordinates
    dataSet[:,:,5,:] = allFlippedZCoordinates
    return dataSet

train0In = open("userData/Clark_train0.p", "rb")
train0 = pickle.load(train0In)
trainList.append(train0) #trainList.update({0 : train0})
#trainList.update({0 : flipHand(train0)})
test0In = open("userData/Clark_test0.p", "rb")
test0 = pickle.load(test0In)
testList.append(test0) #testList.update({0 : test0})
#trainList.update({0 : flipHand(test0)})

train1In = open("userData/Clark_train1.p", "rb")
train1 = pickle.load(train1In)
#trainList.update({1 : train1})
trainList.append(train1)
test1In = open("userData/Clark_test1.p", "rb")
test1 = pickle.load(test1In)
#testList.update({1 : test1})
testList.append(test1)

train2In = open("userData/Apple_train2.p", "rb")
train2 = pickle.load(train2In)
#trainList.update({2 : train2})
trainList.append(train2)
test2In = open("userData/Apple_test2.p", "rb")
test2 = pickle.load(test2In)
#testList.update({2 : test2})
testList.append(test2)

train3In = open("userData/Apple_train3.p", "rb")
train3 = pickle.load(train3In)
#trainList.update({3 : train3})
trainList.append(train3)
test3In = open("userData/Apple_test3.p", "rb")
test3 = pickle.load(test3In)
#testList.update({3 : test3})
testList.append(test3)

train4In = open("userData/Ward_train4.p", "rb")
train4 = pickle.load(train4In)
#trainList.update({4 : train4})
trainList.append(train4)
test4In = open("userData/Ward_test4.p", "rb")
test4 = pickle.load(test4In)
#testList.update({4 : test4})
testList.append(test4)

train5In = open("userData/Peck_train5.p", "rb")
train5 = pickle.load(train5In)
#trainList.update({5 : train5})
trainList.append(train5)
test5In = open("userData/Peck_test5.p", "rb")
test5 = pickle.load(test5In)
#testList.update({5 : test5})
testList.append(test5)

train6In = open("userData/Peck_train6.p", "rb")
train6 = pickle.load(train6In)
#trainList.update({6 : train6})
trainList.append(train6)
test6In = open("userData/Peck_test6.p", "rb")
test6 = pickle.load(test6In)
#testList.update({6 : test6})
testList.append(test6)

train7In = open("userData/MacMaster_train7.p", "rb")
train7 = pickle.load(train7In)
#trainList.update({7 : train7})
trainList.append(train7)
test7In = open("userData/MacMaster_test7.p", "rb")
test7 = pickle.load(test7In)
#testList.update({7 : test7})
testList.append(test7)

train8In = open("userData/Erickson_train8.p", "rb")
train8 = pickle.load(train8In)
#trainList.update({8 : train8})
trainList.append(train8)
test8In = open("userData/Erickson_test8.p", "rb")
test8 = pickle.load(test8In)
#testList.update({8 : test8})
testList.append(test8)

train9In = open("userData/train9.p", "rb")
train9 = pickle.load(train9In)
#trainList.update({9 : train9})
trainList.append(train9)
test9In = open("userData/test9.p", "rb")
test9 = pickle.load(test9In)
#testList.update({9 : test9})
testList.append(test9)


# def ReshapeData(dataList):
#     X = np.zeros((10000, 5*2*3), dtype='f')
#     y = np.zeros(10000)
#     rowEx = 0
#     for setX in dataList:
#         for row in range(1000):
#             y[row + rowEx] = setX
#             col = 0
#             for finger in range(0,5):
#                 for bone in range(0,2):
#                     for tip in range(0,3):
#                         X[row+rowEx,col] = dataList[setX][finger,bone,tip,row]
#                         col = col + 1
#         rowEx = rowEx + 1000
#     return X, y


def ReshapeData(dataList):
    length = len(dataList)*1000
    X = np.zeros((length, 5*2*3), dtype='f')
    y = np.zeros(length)
    for row in range(0,1000):
        for i in range(len(dataList)):
            y[row + i*1000] = i
        col = 0
        for finger in range(0,5):
            for bone in range(0,2):
                for tip in range(0,3):
                    for i in range(len(dataList)):
                        X[row + i*1000,col] = dataList[i][finger,bone,tip,row]
                    col = col + 1
    return X, y


def ReduceData(X):
    X = np.delete(X,1,1) #second instance second dimension
    X = np.delete(X,1,1)
    X = np.delete(X,0,2) #first instance third dimension
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    return X


def CenterData(X):
    allXCoordinates = X[:,:,0,:]
    meanXValue = allXCoordinates.mean()
    X[:,:,0,:] = allXCoordinates - meanXValue

    allYCoordinates = X[:,:,1,:]
    meanYValue = allYCoordinates.mean()
    X[:,:,1,:] = allYCoordinates - meanYValue

    allZCoordinates = X[:,:,2,:]
    meanZValue = allZCoordinates.mean()
    X[:,:,2,:] = allZCoordinates - meanZValue

    return X


for trainX in trainList:
    ReduceData(trainX)
    CenterData(trainX)


for testX in testList:
    ReduceData(testX)
    CenterData(testX)


trainX, trainy = ReshapeData(testList)
testX, testy = ReshapeData(trainList)


### TRAINING KNN ###
knn = KNN()
knn.Use_K_Of(15)
knn.Fit(trainX, trainy)
correct = 0

for row in range(0, 10000):
    prediction = knn.Predict(testX[row])
    if float(prediction) == float(testy[row]):
        correct = correct + 1
        print('correct         ' + str(correct))
    print("wrong " + str(row))

print((correct/10000)*100)

pickle.dump(knn, open('userData/classifier.p', 'wb'))
