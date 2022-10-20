import cv2 as cv
import matplotlib.pyplot as plt
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
    print(type(new_image[0,0]))
    return new_image

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
    return new_image

def opening(image, kernel): 
    return dilation(erosion(image, kernel), kernel)

def closing(image, kernel):
    return erosion(dilation(image, kernel), kernel)

                    
image1 = cv.imread('lena.bmp',cv.IMREAD_GRAYSCALE)
cv.imshow('lena', image1)
cv.waitKey(0)
#print(type(image1[0,0]))  >>  <class 'numpy.uint8'>
image_dilation = dilation(image1, kernel)
plt.imshow(image_dilation, cmap = 'gray')
plt.title('image dilation')
plt.show()
#print(type(image_dilation[0,0])) >> <class 'numpy.float64'>
cv.imshow('lena', image_dilation)
cv.waitKey(0)

image_erosion = erosion(image1, kernel)
plt.imshow(image_erosion, cmap = 'gray')
plt.title('image erosion')
plt.show()

image_open = opening(image1, kernel)
plt.imshow(image_open, cmap = 'gray')
plt.title('image opening')
plt.show()

image_close = closing(image1, kernel)
plt.imshow(image_close, cmap = 'gray')
plt.title('image closing')
plt.show()





