import pickle

class READER:
    pickleIn = open("gesture3.p", "rb")
    gestureData = pickle.load(pickleIn)

    print(gestureData)
