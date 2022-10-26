import numpy as np
import cv2 as cv

def zeroCross(image, t):
    pad = cv.copyMakeBorder(image, 1, 1, 1, 1, cv.BORDER_REPLICATE) #pad_around
    output_img = np.zeros((image.shape))
    row, col = image.shape
    for i in range(1, row + 1):
        for j in range(1, col + 1):
            if pad[i, j] == 0 or pad[i, j] == (-1) * t:
                output_img[i - 1, j - 1] = 255
            elif pad[i, j] == t:
                around = [pad[i - 1, j - 1], pad[i - 1, j], pad[i - 1, j + 1], pad[i, j - 1], \
                    pad[i, j + 1], pad[i + 1, j - 1],pad[i + 1, j], pad[i + 1, j + 1]]
                if(around.count((-1) * t)) == 0:
                    output_img[i - 1, j - 1] = 255
    return output_img

def laplacianOne(image, threshold):
    pad = cv.copyMakeBorder(image, 1, 1, 1, 1, cv.BORDER_REPLICATE) #pad_around
    output_img = np.zeros((image.shape))
    row, col = image.shape
    for i in range(1, row + 1):
        for j in range(1, col + 1):
            r = int(pad[i - 1, j]) + int(pad[i + 1, j]) + int(pad[i, j + 1]) + int(pad[i, j - 1]) - 4 * int(pad[i, j])
            if r >= threshold:
                output_img[i - 1, j - 1] = 1
            elif r <= (-1) * threshold:
                output_img[i - 1, j - 1] = -1
            else:
                output_img[i - 1, j - 1] = 0
    return output_img

def laplacianTwo(image, threshold):
    pad = cv.copyMakeBorder(image, 1, 1, 1, 1, cv.BORDER_REPLICATE) #pad_around
    output_img = np.zeros((image.shape))
    row, col = image.shape
    for i in range(1, row + 1):
        for j in range(1, col + 1):
            r = int(pad[i - 1, j - 1]) + int(pad[i - 1, j]) + int(pad[i - 1, j + 1]) + int(pad[i, j - 1]) \
                + int(pad[i, j + 1]) + int(pad[i + 1, j - 1]) + int(pad[i + 1, j]) + int(pad[i + 1, j + 1])\
                - 8 * int(pad[i, j])
            r = r / 3
            if r >= threshold:
                output_img[i - 1, j - 1] = 1
            elif r <= (-1) * threshold:
                output_img[i - 1, j - 1] = -1
            else:
                output_img[i - 1, j - 1] = 0
    return output_img

def minVarLaplacian(image, threshold):
    pad = cv.copyMakeBorder(image, 1, 1, 1, 1, cv.BORDER_REPLICATE) #pad_around
    output_img = np.zeros((image.shape))
    row, col = image.shape
    for i in range(1, row + 1):
        for j in range(1, col + 1):
            r = 2 * int(pad[i - 1, j - 1]) + (-1) * int(pad[i - 1, j]) + 2 * int(pad[i - 1, j + 1]) + (-1) * int(pad[i, j - 1]) \
                + (-1) * int(pad[i, j + 1]) + 2 * int(pad[i + 1, j - 1]) + (-1) * int(pad[i + 1, j]) + 2 * int(pad[i + 1, j + 1])\
                - 4 * int(pad[i, j])
            r = r / 3
            if r >= threshold:
                output_img[i - 1, j - 1] = 1
            elif r <= (-1) * threshold:
                output_img[i - 1, j - 1] = -1
            else:
                output_img[i - 1, j - 1] = 0
    return output_img           

def laplaceOfGaussian(image, threshold):
    pad = cv.copyMakeBorder(image, 5, 5, 5, 5, cv.BORDER_REPLICATE) #pad_around
    output_img = np.zeros((image.shape))
    row, col = image.shape
    kernel = np.array([
        [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],
        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
        [-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
        [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]
    ])
    for i in range(5, row + 5):
        for j in range(5, col + 5):
            r = np.sum(kernel * pad[i - 5: i + 6, j - 5: j + 6])
            if r >= threshold:
                output_img[i - 5, j - 5] = 1
            elif r <= (-1) * threshold:
                output_img[i - 5, j - 5] = -1
            else:
                output_img[i - 5, j - 5] = 0
    return output_img

def deferenceOfGaussian(image, threshold):
    pad = cv.copyMakeBorder(image, 5, 5, 5, 5, cv.BORDER_REPLICATE) #pad_around
    output_img = np.zeros((image.shape))
    row, col = image.shape
    kernel = np.array([
        [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
        [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
        [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
        [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
        [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
        [-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
        [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
        [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
        [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
        [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
        [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
    ])
    for i in range(5, row + 5):
        for j in range(5, col + 5):
            r = np.sum(kernel * pad[i - 5: i + 6, j - 5: j + 6])
            if r >= threshold:
                output_img[i - 5, j - 5] = 1
            elif r <= (-1) * threshold:
                output_img[i - 5, j - 5] = -1
            else:
                output_img[i - 5, j - 5] = 0
    return output_img
    
        
    
img = cv.imread('lena.bmp', cv.IMREAD_GRAYSCALE)
lapla_mask1 = zeroCross(laplacianOne(img, 15), 1)
cv.imshow('lapla_mask1', lapla_mask1)
cv.imwrite('results/lapla_mask1.jpg', lapla_mask1)
lapla_mask2 = zeroCross(laplacianTwo(img, 15), 1)
cv.imshow('lapla_mask2', lapla_mask2)
cv.imwrite('results/lapla_mask2.jpg', lapla_mask2)
min_lapla = zeroCross(minVarLaplacian(img, 20), 1)
cv.imshow('min_lapla', min_lapla)
cv.imwrite('results/min_lapla.jpg', min_lapla)
lapla_gaussian = zeroCross(laplaceOfGaussian(img, 3000), 1)
cv.imshow('lapla_gaussian', lapla_gaussian)
cv.imwrite('results/lapla_gaussian.jpg', lapla_gaussian)
dif_gaussian = zeroCross(deferenceOfGaussian(img, 1), 1)
cv.imshow('dif_gaussian', dif_gaussian)
cv.imwrite('results/dif_gaussian.jpg', dif_gaussian)
cv.waitKey(0)