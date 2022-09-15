import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

#(a) a binary image (threshold at 128)
def image_bin(image_to_process, value):
    row = image_to_process.shape[0] #image 高度
    col = image_to_process.shape[1] #image 寬度
    for i in range (row):
        for j in range(col):
            for k in range(3):
                if image_to_process[i, j, k] >= value:
                    image_to_process[i, j, k] = 255 #設成白色
                else:
                    image_to_process[i, j, k] = 0 #設成黑色
    return image_to_process

#(b) a histogram
def hist(image_to_process):
    hist = [0] * 256
    row = image_to_process.shape[0] #image 高度
    col = image_to_process.shape[1] #image 寬度
    for i in range (row):
        for j in range(col):
            hist[image_to_process[i, j, 0]] += 1
    #print(hist)
    plt.bar(range(0, 256), hist, color = 'black')
    plt.show()
    return
#(c) connected components use (a) result
def drew_retangle(id):
    down = 0
    right = 0
    top = row
    left = col
    for i in range(row):
        for j in range(col):
            if(label_id[i, j] == id):
                if(i < top):
                    top = i
                elif(i > down):
                    down = i
                if(j < left):
                    left = j
                elif(j > right):
                    right = j
    cv.rectangle(image3, (left, top), (right, down), (0, 255, 0), 2)
    
      
#show oringinal image
image = cv.imread('lena.bmp')
cv.imshow('origianl image', image)
cv.waitKey(0)

#(a) a binary image (threshold at 128)
image1 = cv.imread('lena.bmp')
image_bin = image_bin(image1, 128)
cv.imshow('binary image', image_bin)
cv.waitKey(0)

#(b) a histogram
image2 = cv.imread('lena.bmp')
hist(image2)

#(c) connected components use (a) result
image3 = image_bin
row = image3.shape[0] #image 高度
col = image3.shape[1] #image 寬度

label_id = np.zeros((row, col), dtype = int) #紀錄label id 
label_cnt = 1
for i in range(row):
    for j in range(col):
        if image3[i, j, 0] != 0:
            if(i == 0 and j == 0): #原點
                label_id[i, j] = label_cnt
                label_cnt += 1
            elif(i == 0 and j != 0): #第一行
                if(label_id[i, j - 1]) != 0:
                    label_id[i, j] = label_id[i, j - 1]
                else:
                    label_id[i, j] = label_cnt
                    label_cnt += 1
            elif(i != 0 and j == 0): #第一列
                if(label_id[i - 1, j]) != 0:
                    label_id[i, j] = label_id[i - 1, j]
                else:
                    label_id[i, j] = label_cnt
                    label_cnt += 1
            else: #其他點
                if(label_id[i - 1, j] == 0 and label_id[i, j - 1] != 0):#左邊不為0
                    label_id[i, j] = label_id[i, j - 1]
                elif(label_id[i - 1, j] != 0 and label_id[i, j - 1] == 0):#上面不為0
                    label_id[i, j] = label_id[i - 1, j]
                elif(label_id[i - 1, j] != 0 and label_id[i, j - 1] != 0): #上左都不為零
                    if(label_id[i - 1, j] == label_id[i, j - 1]): #上左相同
                        label_id[i, j] = label_id[i, j - 1]
                    else: #上左不相同
                        color_left = label_id[i, j - 1]
                        color_up = label_id[i - 1, j]
                        label_id[i, j] = color_left #此點先設成跟左邊一樣
                        #更新讓上面的點和左邊的點相同
                        for a in range(row):
                            for b in range(col):
                                if(label_id[a, b] == color_up):
                                    label_id[a, b] = color_left
                else: #上左都沒有相鄰的點
                    label_id[i, j] = label_cnt
                    label_cnt += 1

threshold = 500
#計算大於 500 的面積有哪些 label_cnt 
area_cnt = np.zeros(row * col, dtype = int)
for i in range(row):
    for j in range(col):
          area_cnt[label_id[i, j]] += 1
area = [] #有五個 label_id 數量超過 500
for i in range(1, row * col):
    if(area_cnt[i] > 500):
        area.append(i)

for i in area:
    drew_retangle(i) 

cv.imshow('binary image', image3)
cv.waitKey(0)

                