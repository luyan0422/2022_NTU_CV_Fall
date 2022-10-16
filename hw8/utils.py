import cv2 as cv
import numpy as np

kernel = [[-2, -1], [-2, 0], [-2, 1],
[-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
[0, -2],  [0, -1], [0, 0], [0, 1], [0, 2],
[1, -2],  [1, -1], [1, 0], [1, 1], [1, 2],
          [2, -1], [2, 0], [2, 1]]

# dilation 膨脹
def dilation(image, kernel):
    row = image.shape[0] #image 高度
    col = image.shape[1] #image 寬度
    new_image = np.zeros((row, col))
    
    for i in range(row):
        for j in range(col):
            max_v = 0
            for k in kernel:
                ki, kj = k
                if ki + i >= 0 and ki + i < row and kj + j >= 0 and kj + j < col: #在範圍內的點
                    max_v = max(max_v, image[ki + i, kj + j])
            new_image[i, j] = max_v
    return new_image.astype(np.uint8)

def erosion(image, kernel):
    row = image.shape[0] #image 高度
    col = image.shape[1] #image 寬度
    new_image = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            min_v = 255
            for k in kernel:
                ki, kj = k
                if ki + i >= 0 and ki + i < row and kj + j >= 0 and kj + j < col: #在範圍內的點
                    min_v = min(min_v, image[ki + i, kj + j])
            new_image[i, j] = min_v
    return new_image.astype(np.uint8)


def opening(image, kernel): 
    return dilation(erosion(image, kernel), kernel)

def closing(image, kernel):
    return erosion(dilation(image, kernel), kernel)

def opening_closing(image, kernel):
    return closing(opening(image, kernel), kernel)

def closing_opening(image, kernel):
    return opening(closing(image, kernel), kernel)