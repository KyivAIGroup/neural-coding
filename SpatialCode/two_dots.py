# the task of recognizing the distance between two dots.

import numpy as np
import matplotlib.pyplot as plt

def kWTA(cells, sparsity):
    n_active = max(int(sparsity * cells.size), 1)
    winners = np.argsort(cells)[-n_active:]
    sdr = np.zeros(cells.shape, dtype=cells.dtype)
    sdr[winners] = 1
    return sdr

N = 100
x = np.zeros(N, dtype=int)


# I think the task should be solved through saccades. One of the dot is a salient feature, so we need
# to center the vector around the dot
# or for simplicity skip centering and make new centered vector

x[N // 2] = 1  # first dot
# j = np.random.randint(10, N-10)
j = 70  # second dot
x[j] = 1

print(j)

#layers init
N_l1 = 100
N_l2 = 100
N_l3 = 100
N_l4 = 100
l1 = np.zeros(N_l1)
l2 = np.zeros(N_l2)
l3 = np.zeros(N_l3)
l4 = np.zeros(N_l4)

w_x1 = np.zeros((N_l1, N))
w_12 = np.zeros((N_l2, N_l1))
w_23 = np.zeros((N_l3, N_l2))
w_34 = np.zeros((N_l4, N_l3))


# topographical connections init
rf = 10
k = rf
for i in range(rf, N_l1 - rf):
    weights = np.zeros(N)
    weights[k-rf:k+rf] = 1
    w_x1[i] = weights
    k += 1

rf = 10
k = rf
for i in range(rf, N_l2 - rf):
    weights = np.zeros(N_l1)
    weights[k-rf:k+rf] = 1
    w_12[i] = weights
    k += 1


rf = 10
k = rf
for i in range(rf, N_l3 - rf):
    weights = np.zeros(N_l2)
    weights[k-rf:k+rf] = 1
    w_23[i] = weights
    k += 1

rf = 10
k = rf
for i in range(rf, N_l4 - rf):
    weights = np.zeros(N_l3)
    weights[k-rf:k+rf] = 1
    w_34[i] = weights
    k += 1


# do iteration to average response
iters = 500
data = np.zeros((iters, N_l3))
for i in range(iters):
    w_x1N = w_x1 * np.random.binomial(1, 0.2, size=(N_l1, N))
    w_12N = w_12 * np.random.binomial(1, 0.2, size=(N_l2, N_l1))
    w_23N = w_23 * np.random.binomial(1, 0.2, size=(N_l3, N_l2))
    w_34N = w_34 * np.random.binomial(1, 0.2, size=(N_l4, N_l3))
    l1 = np.dot(w_x1N, x)
    l2 = np.dot(w_12N, l1)
    l3 = np.dot(w_23N, l2)
    l4 = np.dot(w_34N, l3)
    data[i] = l3


plt.plot(np.mean(data, axis=0))
plt.imshow([l1, l2, l3, kWTA(l3, 0.2), l4])
plt.show()


#TODO: add attention (and WTA) across layers


