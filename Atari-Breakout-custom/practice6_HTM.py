# /usr/bin/python
# It has the problem that association memory retrieves wrong patterns.


import math, pygame, sys
import numpy as np
import matplotlib.pyplot as plt
from pygame.locals import *

SCREEN_SIZE = 40
DOWN_SAMPLE = 1
SCREEN_BINS = SCREEN_SIZE // DOWN_SAMPLE
ANGLE_BINS = 4

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
wall_size = 2
wall1 = pygame.Rect(0, 0, wall_size, SCREEN_SIZE)  # walls of the game
wall2 = pygame.Rect(SCREEN_SIZE - wall_size, 0, wall_size, SCREEN_SIZE)
wall3 = pygame.Rect(0, 0, SCREEN_SIZE, wall_size)
wall4 = pygame.Rect(0, SCREEN_SIZE - wall_size, SCREEN_SIZE, wall_size)




class Ball:  # class for ball vars
    def __init__(self, x0=0, y0=0):
        self.x = x0
        self.y = y0
        self.x_prev = x0
        self.y_prev = y0
        self.x_history = []
        self.y_history = []
        self.x_velocity = 1  # amount increasing by for x. adjusted for speed
        self.y_velocity = 1

        self.x_bin = self.down_sample(self.x, DOWN_SAMPLE)
        self.y_bin = self.down_sample(self.y, DOWN_SAMPLE)

        self.pos_flatten = self.y_bin * SCREEN_BINS + self.x_bin
        self.pos_flatten_prev = self.down_sample(self.y_prev, DOWN_SAMPLE) * SCREEN_BINS + self.down_sample(self.x_prev, DOWN_SAMPLE)

        self.position = np.zeros(SCREEN_BINS ** 2, dtype=int)
        self.position_prev = np.zeros(SCREEN_BINS ** 2, dtype=int)

        self.direction = np.zeros(ANGLE_BINS, dtype=int)
        self.direction_prev = np.zeros(ANGLE_BINS, dtype=int)

    def move(self):
        self.move_to(x_new=self.x + self.x_velocity, y_new=self.y + self.y_velocity)

    def move_to(self, x_new, y_new):
        self.x_prev = self.x
        self.y_prev = self.y
        self.x = x_new
        self.y = y_new
        self.update_ball_states()

    def update_ball_states(self):
        self.position_prev = np.copy(self.position)
        self.direction_prev = np.copy(self.direction)
        self.position.fill(0)
        self.direction.fill(0)

        self.x_bin = self.down_sample(self.x, DOWN_SAMPLE)
        self.y_bin = self.down_sample(self.y, DOWN_SAMPLE)

        self.x_bin_prev = self.down_sample(self.x_prev, DOWN_SAMPLE)
        self.y_bin_prev = self.down_sample(self.y_prev, DOWN_SAMPLE)

        self.pos_flatten = self.y_bin * SCREEN_BINS + self.x_bin
        self.position[self.pos_flatten] = 1

        self.x_history.append(self.x_bin)
        self.y_history.append(self.y_bin)

        angle = np.arctan2(self.y - self.y_prev, self.x - self.x_prev)
        angle = (angle + np.pi) / (2 * np.pi)
        angle_bin = int(angle * ANGLE_BINS)
        self.direction[angle_bin] = 1


    @staticmethod
    def down_sample(r, scale):
        return int(r // scale)


class NN:
    def __init__(self, input_size, receptive_field, stride):
        self.activation = np.zeros((1 + (input_size - receptive_field) // stride,
                             1 + (input_size - receptive_field) // stride))
        self.input_size = input_size
        self.shape = self.activation.shape[0]
        self.receptive_field = receptive_field
        self.stride = stride
        self.x_hist = []
        self.y_hist = []

    def activate(self, x_hist, y_hist):
        if len(x_hist) % self.stride == 0 and len(x_hist) >= self.receptive_field:
            (x, y), direct = self.get_space_direction(x_hist[-self.receptive_field:], y_hist[-self.receptive_field:])
            self.activation[x, y] = direct
            self.x_hist.append(x)
            self.y_hist.append(y)

    def get_space_direction(self, x, y):
        # x is a list of ball_x positions
        # y is a list of ball_y positions
        # x_mean = np.mean(x)
        # y_mean = np.mean(y)
        x_mean = np.mean(x) / self.input_size * self.shape
        y_mean = np.mean(y) / self.input_size * self.shape

        angle = np.arctan2(y[-1] - y[0], x[-1] - x[0])
        angle = (angle + np.pi) / (2 * np.pi)
        num_bins = 9
        angle_bin = int(angle * num_bins)
        return (int(x_mean), int(y_mean)), angle_bin

class Game:  # The game itself

    def __init__(self):
        # starting variables
        # self.ball = Ball(wall_size + 1, wall_size + 1)
        self.ball = Ball(wall_size + 5, wall_size + 1)
        self.iters = 0
        self.correct = 0
        self.env = pygame.surfarray.array2d(screen) > 0

        self.nn1 = NN(input_size=SCREEN_BINS, receptive_field=4, stride=2)
        self.nn2 = NN(input_size=self.nn1.shape, receptive_field=4, stride=2)
        self.nn3 = NN(input_size=self.nn2.shape, receptive_field=4, stride=2)

        self.step()

    def draw(self, ball):
        screen.fill(black)
        pygame.draw.rect(screen, grey, wall1)
        pygame.draw.rect(screen, grey, wall2)
        pygame.draw.rect(screen, grey, wall3)
        pygame.draw.rect(screen, grey, wall4)
        pygame.draw.circle(screen, red, (ball.x, ball.y), 0)
        self.env = pygame.surfarray.array2d(screen) > 0

    def check_collision(self, ball):
        collide = False
        # check wall collide----------------------------
        if wall1.collidepoint(self.ball.x, ball.y) or wall2.collidepoint(ball.x, ball.y):
            ball.x_velocity *= -1
            collide = True
        if wall3.collidepoint(ball.x, ball.y) or wall4.collidepoint(ball.x, ball.y):
            ball.y_velocity *= -1
            collide = True
        if collide:
            ball.move()  # this moves the ball out of the wall
            ball.move()  # this moves one step further

    def feature_classification(self, feature):
        label = np.zeros(9, dtype=int)
        # for this task only to speed up the process use a hack. UGLY template matching
        templates = np.zeros((10, 3, 3))
        templates[0] = [[0, 0, 0],
                        [0, 1, 0],
                        [0, 0, 0]]
        templates[1] = [[0, 0, 0],
                        [0, 1, 0],
                        [1, 1, 1]]  # bottom
        templates[2] = [[0, 0, 1],
                        [0, 1, 1],
                        [1, 1, 1]]  # bottom right
        templates[3] = [[1, 0, 0],
                        [1, 1, 0],
                        [1, 1, 1]]  # bottom left
        templates[4] = [[1, 1, 1],
                        [0, 1, 0],
                        [0, 0, 0]]  # top
        templates[5] = [[1, 1, 1],
                        [1, 1, 0],
                        [1, 0, 0]]  # top left
        templates[6] = [[1, 1, 1],
                        [0, 1, 1],
                        [0, 0, 1]]  # top right
        templates[7] = [[1, 0, 0],
                        [0, 1, 0],
                        [1, 0, 0]]  # left
        templates[8] = [[0, 0, 1],
                        [0, 1, 1],
                        [0, 0, 1]]  # right
        winner = np.argmax(np.sum(np.sum(templates * feature, axis=1), axis=1))
        label[winner] = 1
        return label

    def step(self):

        self.ball.move()
        self.check_collision(self.ball)
        self.draw(self.ball)

        self.nn1.activate(self.ball.x_history, self.ball.y_history)
        self.nn2.activate(self.nn1.x_hist, self.nn1.y_hist)
        self.nn3.activate(self.nn2.x_hist, self.nn2.y_hist)

        # get user input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(1000)

if __name__ == '__main__':
    ping = Game()
    for i in range(200):
        ping.step()

    plt.subplot(131)
    plt.imshow(ping.nn1.activation)
    plt.colorbar()

    plt.subplot(132)
    plt.imshow(ping.nn2.activation)
    plt.colorbar()

    plt.subplot(133)
    plt.imshow(ping.nn3.activation)
    plt.colorbar()
    plt.show()
