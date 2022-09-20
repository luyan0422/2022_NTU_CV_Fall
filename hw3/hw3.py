import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys
#create a histogram
def hist(image_to_process):
    hist = [0] * 256
    row = image_to_process.shape[0] #image 高度
    col = image_to_process.shape[1] #image 寬度
    for i in range (row):
        for j in range(col):
            hist[image_to_process[i, j, 0]] += 1
    return hist

# intensity divided by 3
def div_3(image_to_process):
    row = image_to_process.shape[0] #image 高度
    col = image_to_process.shape[1] #image 寬度
    for i in range (row):
        for j in range(col):
            for k in range(3):
                image_to_process[i, j, k] = image_to_process[i, j, k] / 3
    return image_to_process

# histogram equalization
def image_equ(image_to_process, hist):
    row = image_to_process.shape[0] #image 高度
    col = image_to_process.shape[1] #image 寬度
    
    min_val = sys.maxsize
    max_val = 0
    cdf_hist = [0 for i in range(256)]
    accum = 0
    for i in range(0, len(hist)): 
        if hist[i]:
            min_val = min(i, min_val)
            max_val = max(i, max_val)
            accum += hist[i]
            cdf_hist[i] = accum
    cdf_min = cdf_hist[min_val]
    cdf_max = cdf_hist[max_val]
    for i in range (row):
        for j in range(col):
            for k in range(3):
                a = cdf_hist[image_to_process[i, j, k]]
                image_to_process[i, j, k] = ((a - cdf_min) / (cdf_max - cdf_min)) * 255

    return image_to_process

            
#(a) original image and its histogram
image1 = cv.imread('lena.bmp')
cv.imshow('lene', image1)
cv.waitKey(0)
hist1 = hist(image1) 
plt.bar(range(0, 256), hist1) 
plt.show() #show part(a) histogram

#(b) image with intensity divided by 3 and its histogram
image2 = cv.imread('lena.bmp')
image2_new = div_3(image2)
cv.imshow('intensity divided by 3', image2_new)
cv.waitKey(0)
hist2 = hist(image2_new) 
plt.bar(range(0, 256), hist2) 
plt.show() #show part(b) histogram


#(c) applying histogram equalization to (b)
image_eq = image_equ(image2_new, hist2)
cv.imshow('histogram equalization', image_eq)
cv.waitKey(0)
hist3 = hist(image_eq)
plt.bar(range(0, 256), hist3) 
plt.show() #show part(c) histogram