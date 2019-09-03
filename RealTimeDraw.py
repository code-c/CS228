from pygameWindow import PYGAME_WINDOW
import random

pygameWindow = PYGAME_WINDOW()

def Perturb_Circle_Position():
    global x, y
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

while True:
    pygameWindow.Prepare()
    Perturb_Circle_Position()
    pygameWindow.Draw_Black_Circle(x,y)
    pygameWindow.Reveal()

