import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

kernel = [[-2, -1], [-2, 0], [-2, 1],
[-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
[0, -2],  [0, -1], [0, 0], [0, 1], [0, 2],
[1, -2],  [1, -1], [1, 0], [1, 1], [1, 2],
          [2, -1], [2, 0], [2, 1]]

# 先做 binarize
def binarize(image, threshold):
    row = image.shape[0] #image 高度
    col = image.shape[1] #image 寬度
    for i in range (row):
        for j in range(col):
            for k in range(3):
                if image[i, j, k] >= threshold:
                    image[i, j, k] = 255 #設成白色
                else:
                    image[i, j, k] = 0 #設成黑色
    return image

# dilation 膨脹
def dilation(image, kernel):
    row = image.shape[0] #image 高度
    col = image.shape[1] #image 寬度
    new_image = np.zeros((row, col, 3))
    
    for i in range(row):
        for j in range(col):
            if image[i, j, 0] == 255: #白色周圍 octogonal 只要在圖形範圍內都設成白色
                for k in kernel:
                    ki, kj = k
                    if ki + i >= 0 and ki + i < row and kj + j >= 0 and kj + j < col:
                        for m in range(3):
                            new_image[ki + i, kj + j, m] = 255
    return new_image

def erosion(image, kernel, target):
    row = image.shape[0] #image 高度
    col = image.shape[1] #image 寬度
    new_image = np.zeros((row, col, 3))
    if target == 0:
        for i in range(row):
            for j in range(col):
                for k in range(3):
                    new_image[i, j, k] = 255
    for i in range(row):
        for j in range(col):
            if image[i, j, 0] == target: #對白色點及其周圍進行 erosion 
                for k in kernel:
                    ki, kj = k
                    flag = 1
                    # 只要超過範圍或是位在 kernel 內的點有黑色 就不用繼續檢查
                    if ki + i < 0 or ki + i >= row or kj + j < 0 or kj + j >= col or image[ki + i, kj + j, 0] != target:
                        flag = 0
                        break
                if flag == 1: #代表此點和周圍位在 kernel 內的點都是白色 因此設為白色（目標色）
                    for m in range(3):
                            new_image[ki + i, kj + j, m] = target
    return new_image

def opening(image, kernel): 
    return dilation(erosion(image, kernel, 255), kernel)

def closing(image, kernel):
    return erosion(dilation(image, kernel), kernel, 255)

def hm(image, kernel_j, kernel_k):
    row = image.shape[0] #image 高度
    col = image.shape[1] #image 寬度
    image_c = np.zeros((row, col, 3)) #圖片補集
    image_out = np.zeros((row, col, 3)) 
    for i in range (row):
        for j in range(col):
            for k in range(3):
                if image[i, j, k] == 255:
                    image_c[i, j, k] = 0 
                else:
                    image_c[i, j, k] = 255 
            
    image = erosion(image, kernel_j, 255) 
    image_c = erosion(image_c, kernel_k, 0) 
    for i in range (row):
        for j in range(col):
            for k in range(3):
                if image[i, j, k] and image_c[i, j, k]:
                    image_out[i, j, k] = 255
    
    return image_out
    
                    
image1 = cv.imread('lena.bmp')
cv.imshow('lena', image1)
cv.waitKey(0)
image_bin = binarize(image1, 128)

image_dilation = dilation(image_bin, kernel)
cv.imshow('lena dilation', image_dilation)
cv.waitKey(0)

image_erosion = erosion(image_bin, kernel, 255)
cv.imshow('lena erosion', image_erosion)
cv.waitKey(0)

image_open = opening(image_bin, kernel)
cv.imshow('lena opening', image_open)
cv.waitKey(0)

image_close = closing(image_bin, kernel)
cv.imshow('lena closing', image_close)
cv.waitKey(0)


kernel_j = [[-1, 0], [0, 0], [0, -1]] #課本 kernel j 
kernel_k = [[0, 1], [1, 1], [1, 0]] #kernel_j 往左上橫移一單位
image_hitandmiss = hm(image_bin, kernel_j, kernel_k)
cv.imshow('lena hit and miss', image_hitandmiss)
cv.waitKey(0)

