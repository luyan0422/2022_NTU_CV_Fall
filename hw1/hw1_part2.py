import cv2 as cv
import numpy as np

#show oringinal image
image = cv.imread('lena.bmp')
cv.imshow('origianl image', image)
cv.waitKey(0)

#part 2.(d) rotate lena.bmp 45 degrees clockwise
image1 = cv.imread('lena.bmp')
row = image1.shape[0]
col = image1.shape[1]
center = (row / 2, col / 2)
matrix = cv.getRotationMatrix2D(center, 45, 1)
image_rotated = cv.warpAffine(image1, matrix, (row, col))
cv.imshow('rotate lena.bmp 45 degrees clockwise', image_rotated)
cv.waitKey(0)

#part 2.(e) shrink lena.bmp in half
image2 = cv.imread('lena.bmp')
row = image2.shape[0]
col = image2.shape[1]
image_shrink = cv.resize(image, (row // 2, col // 2))
cv.imshow('shrink lena.bmp in half', image_shrink)
cv.waitKey(0)

#part 2.(f) binarize lena.bmp at 128 to get a binary image
image3 = cv.imread('lena.bmp')
retVal, image_binarize = cv.threshold(image3, 127, 255, cv.THRESH_BINARY)
cv.imshow('binarize lena.bmp at 128 to get a binary image', image_binarize)
cv.waitKey(0)