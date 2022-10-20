import cv2 as cv
import numpy as np

def image_bin(image_to_process, value):
    row = image_to_process.shape[0] #image 高度
    col = image_to_process.shape[1] #image 寬度
    for i in range (row):
        for j in range(col):
            if image_to_process[i, j] >= value:
                image_to_process[i, j] = 255 #設成白色
            else:
                image_to_process[i, j] = 0 #設成黑色
    return image_to_process

#down sampling image
def dump(image_to_process):
    dump_image = np.zeros((64, 64), np.uint8)
    row = dump_image.shape[0]
    col = dump_image.shape[1]
    for i in range(row):
        for j in range(col):
            dump_image[i, j] = image_to_process[8 * i, 8 * j] #take the topmost-left pixel as the downsampled data.
    return dump_image

#return yokoi connective number
def yokoi(image_to_process):
    def h(b, c, d, e): #according to textbook
        if b == c and (d != b or e != b):
            return 'q'
        if b == c and (d == b and e == b):
            return 'r'
        return 's'
    row = image_to_process.shape[0]
    col = image_to_process.shape[1]
    yokoi_image = np.zeros((row, col), np.uint8)
    for i in range(row):
        for j in range(col):
            if image_to_process[i, j] > 0: #針對白色點處理
                #以dump_image[i, j]為中心x0 求x1 ~ x8的值 超出邊界設為0
                if i - 1 < 0 or j - 1 < 0:
                    x7 = 0
                else:
                    x7 = image_to_process[i - 1, j - 1]
                if i - 1 < 0:
                    x2 = 0
                else:
                    x2 = image_to_process[i - 1, j]
                if i - 1 < 0 or j + 1 >= col:
                    x6 = 0
                else:
                    x6 = image_to_process[i - 1, j + 1]
                if j - 1 < 0:
                    x3 = 0
                else:
                    x3 = image_to_process[i, j - 1]
                    
                x0 = image_to_process[i, j]
                
                if j + 1 >= col:
                    x1 = 0
                else:
                    x1 = image_to_process[i, j + 1]
                if i + 1 >= row or j - 1 < 0:
                    x8 = 0
                else:
                    x8 = image_to_process[i + 1, j - 1]
                if i + 1 >= row:
                    x4 = 0
                else:
                    x4 = image_to_process[i + 1, j]
                if i + 1 >= row or j + 1 >= col:
                    x5 = 0
                else:
                    x5 = image_to_process[i + 1, j + 1]
            
                a1 = h(x0, x1, x6, x2)
                a2 = h(x0, x2, x7, x3)
                a3 = h(x0, x3, x8, x4)
                a4 = h(x0, x4, x5, x1)

                if a1 == 'r' and a2 == 'r' and a3 == 'r' and a4 == 'r':
                    ans = 5
                else:
                    ans = 0
                    for a in [a1, a2, a3, a4]:
                        if a == 'q':
                            ans += 1
                yokoi_image[i][j] = ans
    return yokoi_image

#pair relationship opreator
def pair(origin_image, yokoi_image):
    def pair_relation(yokoi_image, i, j):
        def h_p(a, m = 1):
            if a == m:
                return 1
            else:
                return 0
        #assume p = 1 and q = 2
        if yokoi_image[i][j] != 1: #not edge in yokoi image
            return 2
        else:
            x1, x2, x3, x4 = 0, 0, 0, 0
            if j + 1 < yokoi_image.shape[1]:
                x1 = h_p(yokoi_image[i][j + 1])
            if i + 1 < yokoi_image.shape[0]:
                x2 = h_p(yokoi_image[i + 1][j])
            if j - 1 >= 0:
                x3 = h_p(yokoi_image[i][j - 1])
            if i - 1 >= 0:
                x4 = h_p(yokoi_image[i - 1][j])
            if x1 + x2 + x3 + x4 < 1:
                return 2
            else:
                return 1
            
    row, col = origin_image.shape
    pair_image = np.zeros((row, col), np.uint8)
    for i in range(row):
        for j in range(col):
            if origin_image[i][j] > 0:
                pair_image[i][j] = pair_relation(yokoi_image, i, j)
    return pair_image


def connectShirnk(origin_image, pair_image):
    def h_c(b, c, d, e):
        if b == c and (d != b or e != b):
            return 1
        else:
            return 0
    def f(a1, a2, a3, a4, x0):
        if sum(np.array([a1, a2, a3, a4]) == 1) == 1:
            return 0 # 0 for backgroung（投影片上以g表示)
        else:
            return x0
    def calculate(origin_image, i , j):
        row, col = origin_image.shape
        if i - 1 < 0 or j - 1 < 0:
            x7 = 0
        else:
            x7 = origin_image[i - 1, j - 1]
        if i - 1 < 0:
            x2 = 0
        else:
            x2 = origin_image[i - 1, j]
        if i - 1 < 0 or j + 1 >= col:
            x6 = 0
        else:
            x6 = origin_image[i - 1, j + 1]
        if j - 1 < 0:
            x3 = 0
        else:
            x3 = origin_image[i, j - 1]
            
        x0 = origin_image[i, j]
        
        if j + 1 >= col:
            x1 = 0
        else:
            x1 = origin_image[i, j + 1]
        if i + 1 >= row or j - 1 < 0:
            x8 = 0
        else:
            x8 = origin_image[i + 1, j - 1]
        if i + 1 >= row:
            x4 = 0
        else:
            x4 = origin_image[i + 1, j]
        if i + 1 >= row or j + 1 >= col:
            x5 = 0
        else:
            x5 = origin_image[i + 1, j + 1]
    
        a1 = h_c(x0, x1, x6, x2)
        a2 = h_c(x0, x2, x7, x3)
        a3 = h_c(x0, x3, x8, x4)
        a4 = h_c(x0, x4, x5, x1)
        return f(a1, a2, a3, a4, x0)
                
    row, col = origin_image.shape
    result = origin_image.copy()
    for i in range(row):
        for j in range(col):
            # pair_image[i, j] == 2 means not edge in yokoi image
            if origin_image[i][j] > 0 and pair_image[i][j] != 2: 
                result[i][j] = calculate(result, i, j)
    return result


# main
image = cv.imread('lena.bmp', cv.IMREAD_GRAYSCALE)
image = dump(image_bin(image, 128)) # 先二值化在取sample
row, col = image.shape

while True:
    old = image.copy()
    # step 1 yokoi
    yokoi_image = yokoi(old)
    # step 2 make pair 
    pair_image = pair(old, yokoi_image)
    # step 3 connect shrink component
    image = connectShirnk(old, pair_image)
    # check change
    count = 0
    for i in range(row):
        for j in range(col):
            if image[i][j] == old[i][j]:
                count = count + 1
    if count == row * col:
        break

cv.imshow('result', image)
cv.waitKey(0)


