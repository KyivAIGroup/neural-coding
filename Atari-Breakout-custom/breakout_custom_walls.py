# /usr/bin/python

import math, pygame, sys
import numpy as np
from pygame.locals import *

SCREEN_SIZE = 40
DOWN_SAMPLE = 10
SCREEN_BINS = SCREEN_SIZE // DOWN_SAMPLE
ANGLE_BINS = 4

position_weights = np.zeros((SCREEN_BINS ** 2, SCREEN_BINS ** 2))
direction_weights = np.zeros((SCREEN_BINS ** 2, ANGLE_BINS))

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))  # create screen - 640 pix by 480 pix
pygame.display.set_caption('Breakout')  # set title bar

# generic colors-------------------------------
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
white = pygame.Color(255, 255, 255)
grey = pygame.Color(142, 142, 142)
black = pygame.Color(0, 0, 0)

# row colors-----------------------------------
r1 = pygame.Color(200, 72, 72)
r2 = pygame.Color(198, 108, 58)
r3 = pygame.Color(180, 122, 48)
r4 = pygame.Color(162, 162, 42)
r5 = pygame.Color(72, 160, 72)
r6 = pygame.Color(67, 73, 202)
colors = [r1, r2, r3, r4, r5, r6]

# variables------------------------------------
controls = 'keys'  # control method
# lef top, width height
wall_size = 10
wall1 = pygame.Rect(0, 0, wall_size, SCREEN_SIZE)  # walls of the game
wall2 = pygame.Rect(SCREEN_SIZE - wall_size, 0, wall_size, SCREEN_SIZE)
wall3 = pygame.Rect(0, 0, SCREEN_SIZE, wall_size)
wall4 = pygame.Rect(0, SCREEN_SIZE - wall_size, SCREEN_SIZE, wall_size)


class Ball:  # class for ball vars
    x = 0
    y = 0
    x_prev = 0
    y_prev = 0
    x_velocity = 1  # amount increasing by for x. adjusted for speed
    y_velocity = 1

    def move(self):
        self.move_to(x_new=self.x + self.x_velocity, y_new=self.y + self.y_velocity)

    def move_to(self, x_new, y_new):
        self.x_prev = self.x
        self.y_prev = self.y
        self.x = x_new
        self.y = y_new

    @property
    def x_bin(self):
        return int(self.x // DOWN_SAMPLE)

    @property
    def y_bin(self):
        return int(self.y // DOWN_SAMPLE)

    @property
    def pos_flatten(self):
        return self.y_bin * SCREEN_BINS + self.x_bin

    @property
    def pos_flatten_prev(self):
        return int(self.y_prev // DOWN_SAMPLE * SCREEN_BINS + self.x_prev // DOWN_SAMPLE)


class Game:  # The game itself

    def __init__(self, ball):
        # starting variables
        ball.x = wall_size + 1
        ball.y = wall_size + 1
        self.iters = 0
        self.correct = 0

        self.step()
        # data = pygame.surfarray.array2d(screen)

    def step(self):
        global angle_bin
        # Draw all the things------------------------------
        screen.fill(black)
        pygame.draw.rect(screen, grey, wall1)
        pygame.draw.rect(screen, grey, wall2)
        pygame.draw.rect(screen, grey, wall3)
        pygame.draw.rect(screen, grey, wall4)
        pygame.draw.rect(screen, red, (ball.x - 3, ball.y - 3, 6, 6))

        # check wall collide----------------------------
        if wall1.collidepoint(ball.x, ball.y) or wall2.collidepoint(ball.x, ball.y):
            ball.x_velocity *= -1
        if wall3.collidepoint(ball.x, ball.y) or wall4.collidepoint(ball.x, ball.y):
            ball.y_velocity *= -1

        ball_state = np.zeros(SCREEN_BINS ** 2, dtype=int)
        ball_state[ball.pos_flatten] = 1

        ball_pred = np.dot(position_weights, ball_state) + np.dot(direction_weights, direction)
        ball_pred = ball_pred.argmax()

        ball.move()

        direction_prev = direction.copy()
        angle = np.arctan2(ball.y - ball.y_prev, ball.x - ball.x_prev)
        angle = (angle + np.pi) / (2 * np.pi)
        angle_bin = int(angle * ANGLE_BINS)
        direction.fill(0)
        direction[angle_bin] = 1

        state = np.r_[ball_state, direction]
        state_prev = np.r_[ball_state_prev, direction_prev]

        w = (w + np.outer(state, state_prev)) > 1

        if ball.pos_flatten != ball.pos_flatten_prev:
            position_weights[ball.pos_flatten_prev, ball.pos_flatten] = 1
            direction_weights[ball.pos_flatten, angle_bin] = 1
            self.iters += 1
            self.correct += ball_pred == ball.pos_flatten
            print(ball_pred, ball.pos_flatten, self.correct / self.iters)

        # get user input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(80)


# -----------------------------------------------------
if __name__ == '__main__':
    screen.fill(black)
    position = np.zeros((SCREEN_BINS, SCREEN_BINS), dtype=int)
    direction = np.zeros(ANGLE_BINS, dtype=int)
    direction_prev = direction.copy()

    ball_state_prev = None
    w = np.zeros((SCREEN_BINS ** 2 + ANGLE_BINS, SCREEN_BINS ** 2 + ANGLE_BINS), dtype=bool)

    ball = Ball()
    ping = Game(ball)

    # np.arctan2(y, x)
    while True:
        ping.step()
        print(ball.x_bin, ball.y_bin)
