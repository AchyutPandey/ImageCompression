# -*- coding: utf-8 -*-
"""ImgCompress.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RI3krpTbK20GpHZKStLgR9esHQEugDWa
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
from utils import *

def calc_cost(arr, carr,n):
    cost=0
    for it in range (n):
        cost+=(abs(arr[it]-carr[it]))**2

    return cost


def find_closest_centroids(X, centroids):
    K = centroids.shape[0]
    n=X.shape[1]
    idx = np.zeros(X.shape[0], dtype=int)

    for i in range(X.shape[0]):
        cntr=0
        mincost=2**32
        for j in range (K):
            cost=calc_cost(X[i], centroids[j],n)
            if cost < mincost:
                mincost=cost
                cntr=j
        idx[i]=cntr

    return idx

def compute_centroids(X, idx, K):
    m, n = X.shape
    centroids = np.zeros((K, n))
    arr = np.zeros(K,dtype=float)
    for i in range(m):
        closest=idx[i]
        arr[closest]=arr[closest]+1
        for j in range (n):

            centroids[closest][j]+=X[i][j]

    for i in range(K):
        for j in range (n):

            centroids[i][j]/=arr[i]


    return centroids

def run_kMeans(X, initial_centroids, max_iters=10, plot_progress=False):
    m, n = X.shape
    K = initial_centroids.shape[0]
    centroids = initial_centroids
    previous_centroids = centroids
    idx = np.zeros(m)
    plt.figure(figsize=(8, 6))

    for i in range(max_iters):
        print("K-Means iteration %d/%d" % (i, max_iters-1))
        idx = find_closest_centroids(X, centroids)
        if plot_progress:
            plot_progress_kMeans(X, centroids, previous_centroids, idx, K, i)
            previous_centroids = centroids


        centroids = compute_centroids(X, idx, K)
    plt.show()
    return centroids, idx

def kMeans_init_centroids(X, K):
    randidx = np.random.permutation(X.shape[0])
    centroids = X[randidx[:K]]
    return centroids

#************input the image to be compressed***********
original_img = plt.imread('/content/igicon.png')
plt.imshow(original_img)
print("Shape of input img is:", original_img.shape)

# in case of JPG img divide all values by 255 to bring values in betwn 0 and 1. for PNG no need as they are already in range
X_img = np.reshape(original_img, (original_img.shape[0] * original_img.shape[1], original_img.shape[2]))

K = 16
max_iters = 10
initial_centroids = kMeans_init_centroids(X_img, K)
centroids, idx = run_kMeans(X_img, initial_centroids, max_iters)

print("Shape of idx:", idx.shape)
print("Closest centroid for the first five elements:", idx[:5])

idx = find_closest_centroids(X_img, centroids)
X_recovered = centroids[idx, :]
X_recovered = np.reshape(X_recovered, original_img.shape)

fig, ax = plt.subplots(1,2, figsize=(16,16))
plt.axis('off')
ax[0].imshow(original_img)
ax[0].set_title('Original')
ax[0].set_axis_off()
ax[1].imshow(X_recovered)
ax[1].set_title('Compressed with %d colours'%K)
ax[1].set_axis_off()

