import numpy as np
import pickle
from knn import KNN


### IMPORTING DATA ###

trainList = []
testList = []

train0In = open("userData/Soccorsi_train0.p", "rb")
train0 = pickle.load(train0In)
trainList.append(train0)
test0In = open("userData/Soccorsi_test0.p", "rb")
test0 = pickle.load(test0In)
testList.append(test0)

train1In = open("userData/train1.p", "rb")
train1 = pickle.load(train1In)
trainList.append(train1)
train2In = open("userData/train2.p", "rb")
train2 = pickle.load(train2In)
trainList.append(train2)

test1In = open("userData/test1.p", "rb")
test1 = pickle.load(test1In)
testList.append(test1)
test2In = open("userData/test2.p", "rb")
test2 = pickle.load(test2In)
testList.append(test2)

train3In = open("userData/Gordon_train3.p", "rb")
train3 = pickle.load(train3In)
trainList.append(train3)
test3In = open("userData/Gordon_test3.p", "rb")
test3 = pickle.load(test3In)
testList.append(test3)

train4In = open("userData/Livingston_train4.p", "rb")
train4 = pickle.load(train4In)
trainList.append(train4)
test4In = open("userData/Livingston_test4.p", "rb")
test4 = pickle.load(test4In)
testList.append(test4)

train5In = open("userData/Livingston_train5.p", "rb")
train5 = pickle.load(train5In)
trainList.append(train5)
test5In = open("userData/Livingston_test5.p", "rb")
test5 = pickle.load(test5In)
testList.append(test5)

train6In = open("userData/Wu_train6.p", "rb")
train6 = pickle.load(train6In)
trainList.append(train6)
test6In = open("userData/Wu_test6.p", "rb")
test6 = pickle.load(test6In)
testList.append(test6)

train7In = open("userData/Rubin_train7.p", "rb")
train7 = pickle.load(train7In)
trainList.append(train7)
test7In = open("userData/Rubin_test7.p", "rb")
test7 = pickle.load(test7In)
testList.append(test7)

train8In = open("userData/Rubin_train8.p", "rb")
train8 = pickle.load(train8In)
trainList.append(train8)
test8In = open("userData/Rubin_test8.p", "rb")
test8 = pickle.load(test8In)
testList.append(test8)

train9In = open("userData/Zonay_train9.p", "rb")
train9 = pickle.load(train9In)
trainList.append(train9)
test9In = open("userData/Zonay_test9.p", "rb")
test9 = pickle.load(test9In)
testList.append(test9)


def ReshapeData(dataList):
    X = np.zeros((10000, 5*2*3), dtype='f')
    y = np.zeros(10000)
    i = 0
    rowEx = 0
    for setX in dataList:
        for row in range(0,1000):
            y[row + rowEx] = i
            col = 0
            for finger in range(0,5):
                for bone in range(0,2):
                    for tip in range(0,3):
                        X[row+rowEx,col] = setX[finger,bone,tip,row]
                        col = col + 1
        i = i + 1
        rowEx = rowEx + 1000
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


trainX, trainy = ReshapeData(trainList)
testX, testy = ReshapeData(testList)


### TRAINING KNN ###

knn = KNN()
knn.Use_K_Of(15)
knn.Fit(trainX, trainy)

correct = 0
for row in range(0, 3000):
    prediction = knn.Predict(testX[row])
    if float(prediction) == float(testy[row]):
        correct = correct + 1

print((correct/3000.0)*100)

pickle.dump(knn, open('userData/classifier.p', 'wb'))
