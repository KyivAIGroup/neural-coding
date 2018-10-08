# here I encode the dot and the line

import numpy as np
import matplotlib.pyplot as plt



def get_neighbors(x, y, input_shape, radius=2):
    """
    Function necessary for topographical projection
    :param x: position x of a point
    :param y: position y of a point
    :param input_shape: need for account boundaries
    :param radius:
    :return: coordinates of square around x,y with radius
    """
    im_x, im_y = input_shape
    xl, xh, yl, yh = int((x - radius)), int((x + radius)), int((y - radius)), int((y + radius))
    yh = im_y if yh > im_y else yh
    xh = im_x if xh > im_x else xh
    yl = 0 if yl < 0 else yl
    xl = 0 if xl < 0 else xl
    return xl, xh, yl, yh

def kWTA(cells, sparsity):
    cells_shape = cells.shape
    cells = cells.flatten()
    n_active = max(int(sparsity * cells.size), 1)
    n_active = min(n_active, len(cells.nonzero()[0]))
    sdr = np.zeros(cells.size, dtype=bool)
    if n_active:
        winners = np.argsort(cells)[-n_active:]
        sdr[winners] = 1
    return sdr.reshape(cells_shape)


def local_kWTA(array, sparsity, window_size=5):
    # apply kWTA to local region (not ideal, problem with boundaries)
    w, h = array.shape
    result = np.zeros(array.shape, dtype=bool)
    for i in range(w - window_size):
        for j in range(h - window_size):
            result[i: i + window_size, j: j + window_size] = kWTA(array[i: i + window_size, j: j + window_size], sparsity)

    return result

# Init input image
space = np.zeros((100, 100))

space[50, 50] = 1
space[60, 40:60] = 1

# init
s0_w = 30
s0_h = 30
N = s0_w * s0_h

s1_w = 50
s1_h = 50
N1 = s1_w * s1_h

# crop region of space. Now it is redundant. at first had a different idea
x = space[35:65, 35:65]

y1 = np.zeros((N1, N1))
# radius of a receptive field of second to first layer
R = 3

# I chose not to flatten the image. It is easier to deal with topographical connections
w = np.zeros((s1_w, s1_h, s0_w, s0_h), dtype=bool)
for i in range(s1_w):
    for j in range(s1_h):
        # projection of an axon prom s0 to s1
        ind1 = int(round(i * float(s0_w) / s1_w))
        ind2 = int(round(j * float(s0_h) / s1_h ))  # minus to make 1.5 round go to 1
        xl, xh, yl, yh = get_neighbors(ind1, ind2, (s0_w, s0_h), radius=R)
        w[i, j] = np.zeros((s0_w, s0_h))
        w[i, j, xl:xh, yl:yh] = 1

w = w * np.random.binomial(1, 0.3, size=(s1_w, s1_h, s0_w, s0_h))

y1 = np.dot(w.reshape((N1, N)), x.reshape(N)).reshape(s1_w, s1_h)
plt.imshow(y1)
plt.show()

plt.imshow(local_kWTA(y1, 0.1))
plt.show()
