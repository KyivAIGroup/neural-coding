#/usr/bin/python

import math,pygame,sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((640,480)) #create screen - 640 pix by 480 pix
pygame.display.set_caption('Breakout') #set title bar

#generic colors-------------------------------
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)
grey = pygame.Color(142,142,142)
black = pygame.Color(0,0,0)

#row colors-----------------------------------
r1 = pygame.Color(200,72,72)
r2 = pygame.Color(198,108,58)
r3 = pygame.Color(180,122,48)
r4 = pygame.Color(162,162,42)
r5 = pygame.Color(72,160,72)
r6 = pygame.Color(67,73,202)
colors = [r1,r2,r3,r4,r5,r6]

#variables------------------------------------
controls = 'keys' #control method
mousex,mousey = 0,0 #mouse position
wall1 = pygame.Rect(20,80,10,380) #walls of the game
wall2 = pygame.Rect(590,80,10,380)
wall3 = pygame.Rect(20,80,580,10)
wall4 = pygame.Rect(20,450,580,10)




class Ball: #class for ball vars
    x = 0
    y = 0
    remaining = 10
    xPos = 1 #amount increasing by for x. adjusted for speed
    yPos = 1
    adjusted = False #says wether the xPos and yPos have been adjusted for speed
    speed = 5
    collisions = 0
    alive = False
    moving = False
    def adjust(self): #adjusts the x and y being added to the ball to make the hypotenuse the ball speed
        tSlope = math.sqrt(self.xPos**2 + self.yPos**2)
        self.xPos = (self.speed / tSlope) * self.xPos
        self.yPos = (self.speed / tSlope) * self.yPos
        self.adjusted = True



class Game(): #The game itself

    def __init__(self, ball):
        #starting variables
        self.running = True

        ball.alive = True
        ball.moving = True
        ball.x = 53
        ball.y = 300
        ball.collisions, ball.speed = 0, 5
        ball.speed = 5
        ball.xPos = 1
        ball.yPos = 1
        ball.adjusted = False



        self.play()
        # data = pygame.surfarray.array2d(screen)

    def play(self):
        self.draw()
        self.x = int(ball.x)
        self.y = int(ball.y)

    def draw(self):
        # Draw all the things------------------------------
        screen.fill(black)
        pygame.draw.rect(screen, grey, wall1)
        pygame.draw.rect(screen, grey, wall2)
        pygame.draw.rect(screen, grey, wall3)
        pygame.draw.rect(screen, grey, wall4)
        pygame.draw.rect(screen, red, (ball.x - 3, ball.y - 3, 6, 6))

        # check all the collisions-------------------------
        if ball.moving == True:
            if ball.adjusted == False:
                ball.adjust()
            ball.x += ball.xPos
            ball.y += ball.yPos

            # check wall collide----------------------------
            if wall1.collidepoint(ball.x, ball.y) == True or wall2.collidepoint(ball.x, ball.y):
                ball.xPos = -(ball.xPos)
            if wall3.collidepoint(ball.x, ball.y) == True or wall4.collidepoint(ball.x, ball.y):
                ball.yPos = -(ball.yPos)

        # get user input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(80)



#-----------------------------------------------------
if __name__ == '__main__':
    screen.fill(black)
    ball = Ball()
    ping = Game(ball)
    while True:
        ping.play()
        x = ping.x // 10
        y = ping.y // 10
        print(x, y)






