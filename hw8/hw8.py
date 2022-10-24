import math
import random
import cv2 as cv
import numpy as np
from utils import *
import matplotlib.pyplot as plt
kernel = [[-2, -1], [-2, 0], [-2, 1],
[-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
[0, -2],  [0, -1], [0, 0], [0, 1], [0, 2],
[1, -2],  [1, -1], [1, 0], [1, 1], [1, 2],
          [2, -1], [2, 0], [2, 1]]

def snr(img_old, img_new):
    row, col = img_old.shape
    size = row * col
    mean_old = 0
    for i in range(row):
        for j in range(col):
            mean_old += img_old[i, j]
    mean_old = mean_old / size
    
    VS = 0
    for i in range(row):
        for j in range(col):
            VS += math.pow(img_old[i, j] - mean_old, 2)
    VS = VS / size
    
    mean_new = 0
    for i in range(row):
        for j in range(col):
            mean_new += int(img_new[i, j]) - int(img_old[i, j])
    mean_new = mean_new / size
    
    VN = 0
    for i in range(row):
        for j in range(col):
            VN += math.pow(int(img_new[i, j]) - int(img_old[i, j]) - mean_new, 2)
    VN = VN / size
    
    return 20 * math.log(math.sqrt(VS) / math.sqrt(VN), 10)

def gussian(img, amplitude):
    gussian_img = img.copy()
    row, col = img.shape
    for i in range(row):
        for j in range(col):
            noise = img[i, j] + amplitude * np.random.normal(0, 1)
            if noise > 255:
                noise = 255
            gussian_img[i, j] = noise
    return gussian_img.astype(np.uint8)

def pepperAndSalt(img, amplitude):
    sp_img = img.copy()
    row, col = img.shape
    for i in range(row):
        for j in range(col):
            random_value = random.uniform(0, 1)
            if random_value <= amplitude:
                sp_img[i, j] = 0
            elif random_value >= 1 - amplitude:
                sp_img[i, j] = 255
            else:
                sp_img[i, j] = img[i, j]
    return sp_img.astype(np.uint8)
    
def median_filter(img, size):
    output = np.zeros(img.shape)
    row, col = img.shape
    #padding arround
    p = (size - 1) // 2
    img = cv.copyMakeBorder(img, p, p, p, p, cv.BORDER_REPLICATE)
    new_row, new_col = img.shape
    for i in range(p, new_row - p):
        for j in range(p, new_col - p):
            a = []
            for k in range(i - p, i + p + 1):
                for l in  range(j - p, j + p + 1):
                    a.append(img[k, l])
            a.sort()
            output[i - p, j - p] = a[(size * size) // 2]
    return output.astype(np.uint8)
            
def box_filter(img, size):
    output = np.zeros(img.shape)
    row, col = img.shape
    #padding arround
    p = (size - 1) // 2
    img = cv.copyMakeBorder(img, p, p, p, p, cv.BORDER_REPLICATE)
    new_row, new_col = img.shape
    for i in range(p, new_row - p):
        for j in range(p, new_col - p):
            a = 0
            for k in range(i - p, i + p + 1):
                for l in  range(j - p, j + p + 1):
                    a += img[k, l]
            output[i - p, j - p] = a / (size * size)
    return output.astype(np.uint8)

            
img = cv.imread('lena.bmp',cv.IMREAD_GRAYSCALE)
test = cv.imread('median_5x5.bmp',cv.IMREAD_GRAYSCALE)

g10 = gussian(img, 10)
b3g10 = box_filter(g10, 3)
m3g10 = median_filter(g10, 3)
ocg10 = opening_closing(g10, kernel)
b5g10 = box_filter(g10, 5)
m5g10 = median_filter(g10, 5)
cog10 = closing_opening(g10, kernel)

g30 = gussian(img, 30)
b3g30 = box_filter(g30, 3)
m3g30 = median_filter(g30, 3)
ocg30 = opening_closing(g30, kernel)
b5g30 = box_filter(g30, 5)
m5g30 = median_filter(g30, 5)
cog30 = closing_opening(g30, kernel)

ps01 = pepperAndSalt(img, 0.1)
b3ps01 = box_filter(ps01, 3)
m3ps01 = median_filter(ps01, 3)
ocps01 = opening_closing(ps01, kernel)
b5ps01 = box_filter(ps01, 5)
m5ps01 = median_filter(ps01, 5)
cops01 = closing_opening(ps01, kernel)

ps005 = pepperAndSalt(img, 0.05)
b3ps005 = box_filter(ps005, 3)
m3ps005 = median_filter(ps005, 3)
ocps005 = opening_closing(ps005, kernel)
b5ps005 = box_filter(ps005, 5)
m5ps005 = median_filter(ps005, 5)
cops005 = closing_opening(ps005, kernel)
n = 3
m = 3
fig1 = [g10, b3g10, m3g10, ocg10, b5g10, m5g10, cog10]
fig2 = [g30, b3g30, m3g30, ocg30, b5g30, m5g30, cog30]
fig3 = [ps01, b3ps01, m3ps01, ocps01, b5ps01, m5ps01, cops01]
fig4 = [ps005, b3ps005, m3ps005, ocps005, b5ps005, m5ps005, cops005]
together = [fig1, fig2, fig3, fig4]
title = ['box filter 3x3', 'median filter 3x3', 'opening then closing', 'box filter 5x5', 'median filter 5x5', 'closing then opening']
together_title = ['guaasian 10', 'guaasian 30', 'pepper and salt 0.1', 'pepper and salt 0.05']
for i in range(4):
    for j in range(7):
        outout_image = together[i][j]
        if j == 0:
            plt.subplot(n, m, 2)
            plt.imshow(outout_image, cmap = 'gray')
            plt.title("{}\nsnr = {}".format(together_title[i], snr(img, outout_image)))
        else:
            plt.subplot(n, m, j + 3)
            plt.imshow(outout_image, cmap = 'gray')
            plt.title("{}  snr = {:.6f}".format(title[j - 1], snr(img, outout_image)))
        plt.xticks([])
        plt.yticks([])
    plt.show()
