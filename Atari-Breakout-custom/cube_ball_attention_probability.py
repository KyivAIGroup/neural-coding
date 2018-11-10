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
        self.x_velocity = 0  # amount increasing by for x. adjusted for speed
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

        angle = np.arctan2(self.y - self.y_prev, self.x - self.x_prev)
        angle = (angle + np.pi) / (2 * np.pi)
        angle_bin = int(angle * ANGLE_BINS)
        self.direction[angle_bin] = 1


    @staticmethod
    def down_sample(r, scale):
        return int(r // scale)



class Game:  # The game itself

    def __init__(self):
        # starting variables
        # self.ball = Ball(wall_size + 1, wall_size + 1)
        self.ball = Ball(wall_size + 5, wall_size + 1)
        self.iters = 0
        self.correct = 0
        self.env = pygame.surfarray.array2d(screen) > 0

        self.label_prev = np.zeros(9, dtype=int)
        self.label = np.zeros(9, dtype=int)

        self.state_pred = np.zeros(SCREEN_SIZE ** 2 * ANGLE_BINS * self.label.size)
        self.p = np.zeros((9, 36))   # state, direction outer label

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
        global w

        self.ball.move()
        self.check_collision(self.ball)
        self.draw(self.ball)

        receptive_radius = 1
        feature = self.env[self.ball.x - receptive_radius: self.ball.x + receptive_radius + 1,
                  self.ball.y - receptive_radius: self.ball.y + receptive_radius + 1].astype(int)

        self.label_prev = np.copy(self.label)
        self.label = self.feature_classification(feature)

        delta_x = self.ball.x_bin - self.ball.x_bin_prev
        delta_y = self.ball.y_bin - self.ball.y_bin_prev
        r = np.sqrt(delta_x ** 2 + delta_y ** 2)


        transition = delta_y * 3 + delta_x
        direction_label = np.nonzero(np.outer(self.ball.direction, self.label).flatten())[0][0]

        # print(transition, 'tran')
        # print(direction_label)

        # state = np.outer(self.ball.position, self.ball.direction).flatten()
        # state = np.outer(state, self.label).flatten()

        # state_prev = np.outer(self.ball.position_prev, self.ball.direction_prev).flatten()
        # state_prev = np.outer(state_prev, self.label_prev).flatten()

        self.p[transition, direction_label] += 1

        # if np.nonzero(self.ball.position)[0] != np.nonzero(self.ball.position_prev)[0]:
            # w = (w + np.outer(state, state_prev)) > 0
            # np.fill_diagonal(w, 0)
            # state_pred = np.dot(w, state)
                # state_pred_new = np.dot(w, state_pred_new)
            # print(np.nonzero(state)[0], self.iters)
            # print(np.nonzero(state_pred)[0], self.iters)

            # self.iters += 1
            # self.correct += ball_pred == ball.pos_flatten
            # print(state_pred) #, ball.pos_flatten, self.correct / self.iters)

        # get user input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(1000)

if __name__ == '__main__':
    # w = np.zeros((SCREEN_BINS ** 2 * ANGLE_BINS * 9, SCREEN_BINS ** 2 * ANGLE_BINS * 9), dtype=bool)
    ping = Game()
    # while True:
    #     ping.step()
    #     plt.imshow(ping.p)
    #     plt.show(block=False)
    for i in range(200):
        ping.step()


    plt.imshow(np.log(ping.p), interpolation='none')
    # plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.colorbar()
    # print(ping.p)
    plt.show()
