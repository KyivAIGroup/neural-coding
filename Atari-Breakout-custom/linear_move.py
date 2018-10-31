import numpy as np


N = 20
space = np.zeros(N, dtype=int)

reward_position = 5
agent_position = 10

space[agent_position] = 1

agent_moves = np.array([[0, 0, 1],    # move to the left
                        [0, 1, 0],     # stay
                        [1, 0, 0]])     # move to the right

selected_move = 2
print(space)
print(np.convolve(space, agent_moves[selected_move], mode='same'))


######### Alternative
moves = [0, 1, -1]
selected_move = 0
agent_position += moves[selected_move]

