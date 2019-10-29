import pygame
from constants import *

class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((pygameWindowWidth,pygameWindowDepth))
        pygame.display.set_caption('Learn ASL')

    def Image(self):

        handOver = pygame.image.load('hci.jpg')
        self.screen.blit(handOver, (pygameWindowWidth-300, 0))

    def Prepare(self):
        self.screen.fill(WHITE)
        #self.Image()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.done = True

    def Reveal(self):
        pygame.display.update()
        
    
    def Draw_Black_Circle(self,x,y):
        pygame.draw.circle(self.screen, BLACK, (x, y), 20)

    def Draw_Black_Line(self, xBase, yBase, xTip, yTip, b):
        pygame.draw.line(self.screen, BLACK, (xBase, yBase), (xTip, yTip), (3-b))

    def Draw_Line(self, xBase, yBase, xTip, yTip):
        pygame.draw.line(self.screen, BLUE, (xBase, yBase), (xTip, yTip))

    def MoveLeft(self):
        handOver = pygame.image.load('moveLeft.png')
        self.screen.blit(handOver, (pygameWindowWidth-300, 0))

    def MoveRight(self):
        handOver = pygame.image.load('moveRight.png')
        self.screen.blit(handOver, (pygameWindowWidth-300, 0))

    def MoveDown(self):
        handOver = pygame.image.load('moveDown.png')
        self.screen.blit(handOver, (pygameWindowWidth-300, 0))

    def MoveUp(self):
        handOver = pygame.image.load('MoveUp.png')
        self.screen.blit(handOver, (pygameWindowWidth-300, 0))

    def Centered(self):
        handOver = pygame.image.load('center.png')
        self.screen.blit(handOver, (pygameWindowWidth-300, 0))

    def RandomNumber(self, number):
        font = pygame.font.SysFont('Comic Sans MS', 50)
        numDisplay = font.render(str(number), False, BLACK)
        self.screen.blit(numDisplay, (pygameWindowWidth-150, 100))
        
    def Numbers(self):
        numbers = pygame.image.load('numbers.jpg')
        self.screen.blit(numbers, (pygameWindowWidth-300, pygameWindowDepth/2))

