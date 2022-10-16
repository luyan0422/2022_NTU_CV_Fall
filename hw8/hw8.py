import math
import random
import cv2 as cv
import numpy as np
from utils import *
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
            output[i - p, j - p] = a[4]
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
            output[i - p, j - p] = a / 9
    return output.astype(np.uint8)


            
img = cv.imread('lena.bmp',cv.IMREAD_GRAYSCALE)
test = cv.imread('median_5x5.bmp',cv.IMREAD_GRAYSCALE)


