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

    def showProgress(self, numSuc, numFail, prevNumSuc, prevNumFail):
        font = pygame.font.SysFont('Comic Sans MS', 50)
        prevSesh = font.render("Prev.", False, BLACK)
        currSesh = font.render("Curr.", False, BLACK)
        ratio = font.render("Ratio", False, BLACK)
        fails = font.render("Fails", False, BLACK)
        success = font.render("Succ", False, BLACK)
        numSucD = font.render(str(numSuc), False, BLACK)
        numFailD = font.render(str(numFail), False, BLACK)
        prevNumSucD = font.render(str(prevNumSuc), False, BLACK)
        prevNumFailD = font.render(str(prevNumFail), False, BLACK)
        self.screen.blit(success, (20, pygameWindowDepth-100))
        self.screen.blit(fails, (20, pygameWindowDepth-50))
        self.screen.blit(ratio, (20, pygameWindowDepth-150))

        self.screen.blit(prevSesh, (150, pygameWindowDepth-150))
        self.screen.blit(prevNumSucD, (150, pygameWindowDepth-100))
        self.screen.blit(prevNumFailD, (150, pygameWindowDepth-50))

        self.screen.blit(currSesh, (250, pygameWindowDepth-150))
        self.screen.blit(numSucD, (250, pygameWindowDepth-100))
        self.screen.blit(numFailD, (250, pygameWindowDepth-50))

    def showScores(self, highScores):
        font = pygame.font.SysFont('Comic Sans MS', 30)
        scoresD = font.render("TOP SCORES", False, BLACK)
        self.screen.blit(scoresD, (10, pygameWindowDepth-300))
        pl = 270
        for i in range(1,4):
            place = font.render(str(i)+".", False, BLACK)
            self.screen.blit(place, (10, pygameWindowDepth-pl))
            pl-=30
        pl = 270
        for score in highScores:
            string = str(str(score[0]) + " : " + str(score[1]))
            stringD = font.render(string, False, BLACK)
            self.screen.blit(stringD, (30, pygameWindowDepth-pl))
            pl -=30

    def warm(self):
        pygame.draw.rect(self.screen, GREEN, [230, pygameWindowDepth-290, 90, 90])
        
    def cold(self):
        pygame.draw.rect(self.screen, RED, [230, pygameWindowDepth-290, 90, 90])
