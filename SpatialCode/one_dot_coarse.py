import numpy as np
import matplotlib.pyplot as plt

def kWTA(cells, sparsity):
    n_active = max(int(sparsity * cells.size), 1)
    winners = np.argsort(cells)[-n_active:]
    sdr = np.zeros(cells.shape, dtype=cells.dtype)
    sdr[winners] = 1
    return sdr

def get_neighbors(x, y, input_shape, radius=2):
    im_x, im_y = input_shape
    xl, xh, yl, yh = int((x - radius)), int((x + radius)), int((y - radius)), int((y + radius))
    yh = im_y if yh > im_y else yh
    xh = im_x if xh > im_x else xh
    yl = 0 if yl < 0 else yl
    xl = 0 if xl < 0 else xl
    return xl, xh, yl, yh


s0_w = 28
s0_h = 28
N = s0_w * s0_h

s1_w = 50
s1_h = 50
M = s1_w * s1_h

# this is the procedure of random topographical projections
# I create projection in a form of square of a given size and then randomize it
R = 5  # receptive field size
w = np.zeros((M, N))
for i in range(s1_w):
    for j in range(s1_h):
        # projection of axon prom s0 to s1
        ind1 = int(round(i * float(s0_w) / s1_w))
        ind2 = int(round(j * float(s0_h) / s1_h ))  # minus to make 1.5 round go to 1
        xl, xh, yl, yh = get_neighbors(ind1, ind2, (s0_w, s0_h), radius=R)
        dt = np.zeros((s0_w, s0_h), dtype=bool)
        dt[xl:xh, yl:yh] = 1
        w[i * s1_h + j, dt.flatten()] = 1

w = w*np.random.binomial(1, 0.2, size=(M, N))

# plt.imshow(w[55, :].reshape(s0_w, s0_h))
# plt.show()


x = np.zeros((s0_w, s0_h), dtype=bool)
x_c, y_c = 20, 15   # coordinates of a cursor

x[x_c, y_c] = 1

y1 = np.dot(w, x.flatten()) >= 1
# print(np.sort(np.dot(w, x.flatten()))[-100:])
# y1 = kWTA(np.dot(w, x.flatten()), 0.05)

x = x * 0
x_c, y_c = 19, 15   # coordinates of a cursor
x[x_c, y_c] = 1

y2 = np.dot(w, x.flatten()) >= 1
# y2 = kWTA(np.dot(w, x.flatten()), 0.05)

print(np.sum(y1 * y2))

plt.imshow(y2.reshape(s1_w, s1_h))
plt.show()
