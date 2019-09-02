import sys

sys.path.insert(0, '..')

import Leap


#from pygameWindow import PYGAME_WINDOW
#
#pygameWindow = PYGAME_WINDOW()
#
#def Perturb_Circle_Position():
#    global x, y
#    x = random.randint(100, 400)
#    y = random.randint(100, 400)
#    fourSidedDieRoll = random.randint(1,4)
#
#    if fourSidedDieRoll == 1:
#        y = y - 1
#    elif fourSidedDieRoll == 2:
#        y = y + 1
#    elif fourSidedDieRoll == 3:
#        x = x - 1
#    elif fourSidedDieRoll == 4:
#        x = x + 1

controller = Leap.Controller()

while True:
    frame = controller.frame()
    if not frame.hands.is_empty:
        print ("Hand Detected")
#    pygameWindow.Prepare()
#    Perturb_Circle_Position()
#    pygameWindow.Draw_Black_Circle(x,y)
#    pygameWindow.Reveal()

