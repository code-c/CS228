import pygame
from constants import *

class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((pygameWindowWidth,pygameWindowDepth))

    def Prepare(self):
        self.screen.fill(WHITE)

    def Reveal(self):
        pygame.display.update()
    
    def Draw_Black_Circle(self,x,y):
        pygame.draw.circle(self.screen, BLACK, [x, y], 50)
