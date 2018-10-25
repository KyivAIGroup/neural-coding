#/usr/bin/python
#####################################
#          ATARI BREAKOUT           #
#                                   #
#          Python code by           #
#           Adam Knuckey            #
#               2013                #
#                                   #
#    Original Game by Atari, inc    #
#                                   #
#  Controls:                        #
#  -arrow keys/mouse to move paddle #
#  -spacebar to launch ball         #
#  -enter key to use menu           #
#                                   #
#  Scoring:                         #
#  -Green and blue rows...........1 #
#  -Yellow and lower orange rows..4 #
#  -Upper orange and red rown.....7 #
#                                   #
#####################################

#Add mouse controls
#add half size paddle after hitting back wall

import math,pygame,sys,shutil,getpass
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
dx,dy = 18,6 #dimensions of board
bx,by = 50,150 #board position
score = 0 #score
wall1 = pygame.Rect(20,100,30,380) #walls of the game
wall2 = pygame.Rect(590,100,30,380)
wall3 = pygame.Rect(20,80,600,30)

#Creates a board of rectangles----------------
def new_board():
    board = []
    for x in range(dx):
        board.append([])
        for y in range(dy):
            board[x].append(1)
    return board
          
#Classes defined------------------------------ 
class Paddle: #class for paddle vars
    x = 320
    y = 450
    size = 2 #2 is normal size, 1 is half-size
    direction = 'none'

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

#Functions defined----------------------------
def print_board(board,colors): #prints the board
    for x in range(dx):
        for y in range(dy):
            if board[x][y] == 1:
                pygame.draw.rect(screen,colors[y],(((x*30)+bx),((y*12)+by),30,12))
          
def print_paddle(paddle): #prints the paddle
    if paddle.size == 2:
        pygame.draw.rect(screen,red,((paddle.x-20),(paddle.y),40,5))

def collide_paddle(paddle,ball): #recalculates the trajectory for the ball after collision with the paddle
    ball.adjusted = False
    if ball.x - paddle.x != 0:
        ball.xPos = (ball.x-paddle.x) / 8
        ball.yPos = -1
    else:
        ball.xPos = 0
        ball.yPos = 1
    return ball.adjusted, float(ball.xPos), float(ball.yPos)


def game(score,paddle,ball,board,wall1): #The game itself
    #starting variables
    running = True
    ball.alive = True
    ball.moving = False
    ball.x = 53
    ball.y = 300
    ball.collisions, ball.speed = 0,5
    colO = False #check collision with the orange row, for speed purposes
    colR = False #same but for red row
    ball.speed = 5
    ball.xPos = 1
    ball.yPos = 1
    ball.adjusted = False
          
    while running == True:
        #Draw all the things------------------------------
        screen.fill(black)
        pygame.draw.rect(screen,grey,wall1)
        pygame.draw.rect(screen,grey,wall2)
        pygame.draw.rect(screen,grey,wall3)
        pygame.draw.rect(screen,red,(ball.x-3,ball.y-3,6,6))
        print_board(board,colors)
        print_paddle(paddle)
        # write(20,20,grey,str(score))
        temp = 0
        for life in range(ball.remaining):
            if life != 0:
                pygame.draw.rect(screen,red,(600,400-temp,10,10))
                temp += 15

        #check all the collisions-------------------------
        if ball.moving == True:
            if ball.adjusted == False:
                ball.adjust()
            ball.x += ball.xPos
            ball.y += ball.yPos
            if ball.y < 455 and ball.y > 445:
                if ball.x > paddle.x-20 and ball.x < paddle.x+20:
                    ball.adjusted, ball.xPos, ball.yPos = collide_paddle(paddle,ball)#paddle collide
                    ball.collisions += 1
                    #increase ball speeds at 4 hits on paddle, 12 hits, orange row, red row
                    if ball.collisions == 4:
                        ball.speed += 1
                    if ball.collisions == 12:
                        ball.speed += 1
                    #if ball hits the back wall, paddle cuts in half
            #check wall collide----------------------------
            if wall1.collidepoint(ball.x,ball.y) == True or wall2.collidepoint(ball.x,ball.y):
                ball.xPos = -(ball.xPos)
            if wall3.collidepoint(ball.x,ball.y) == True:
                ball.yPos = -(ball.yPos)

            #check collision with bricks-------------------
            Break = False
            for x in range(dx):
                for y in range(dy):
                    if board[x][y] == 1:
                        block = pygame.Rect(30*x+bx-1,12*y+by-1,32,14)
                        if block.collidepoint(ball.x,ball.y) == True:
                            board[x][y] = 0
##                            if y*12+by+12 < ball.y: FIX THIS ITS THE BLOCK BUG
##                                ball.y = -(ball.y)
##                            elif x*30+bx+30 < 
                            ball.yPos = -ball.yPos #Cheat
                            if y == 4 or y == 5:
                                score += 1
                            elif y == 2 or y == 3:
                                score += 4
                                if colO == False:
                                    colO = True
                                    ball.speed+= 1
                            else:
                                score += 7
                                if colR == False:
                                    colR= True
                                    ball.speed+= 2
                            Break = True
                    if Break == True:
                        break
                if Break == True:
                    break
            if ball.y > 460:
                ball.alive = False
          
        #check if ball was lost
        if ball.alive == False:
            running = False
            ball.remaining -= 1
          
        #move paddle
        if paddle.direction == 'right':
            if paddle.x <= 561:
                paddle.x += 8
        elif paddle.direction == 'left':
            if paddle.x >= 79:
                paddle.x -= 8

        #get user input
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEMOTION:
                mx,my = event.pos
            elif event.type == MOUSEBUTTONUP:
                mx,my = event.pos

            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    paddle.direction = 'left'
                if event.key == K_RIGHT:
                    paddle.direction = 'right'
                if event.key == K_SPACE:
                    if ball.moving == False:
                        ball.moving = True
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    if paddle.direction == 'left':
                        paddle.direction = 'none'
                if event.key == K_RIGHT:
                    if paddle.direction == 'right':
                        paddle.direction = 'none'
          
        #update display
        pygame.display.update()
        fpsClock.tick(30)
    return score

#-----------------------------------------------------
if __name__ == '__main__':
    replay = True
    loop = 0
    screen.fill(black)
    board = new_board()
    score = 0
    paddle = Paddle()
    ball = Ball()
    while ball.remaining > 0:
        score = game(score,paddle,ball,board,wall1)
        if ball.remaining == 0:
            for x in range(16):
                for y in range(12):
                    pygame.draw.rect(screen,black,(x*40,y*40,40,40))
                    pygame.display.update()
                    pygame.time.wait(10)
                    boardcheck = 0
            for x in range(len(board)):
                for y in range(len(board[x])):
                    boardcheck += board[x][y]
            if boardcheck == 0:
                paddle = Paddle()
                ball = Ball()
                board = new_board()
                while ball.remaining > 0:
                    score = game(score,paddle,ball,board,wall1)
                    if ball.remaining == 0:
                        for x in range(16):
                            for y in range(12):
                                pygame.draw.rect(screen,black,(x*40,y*40,40,40))
                                pygame.display.update()
                                pygame.time.wait(10)
            replay = False



