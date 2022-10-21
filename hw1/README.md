## Computer vision homework 1

### homework discripition
Write a program to do the following requirement

1. upside-down

2. right-side-left

3. diagonally flip 

### how to implement

-  一些基本操作

    1.read image

    可以利用 OpenCV  
    ```
    cv2.imread('path name')
    ```
    或是 matplotlib.pyplot 
    ```
    matplotlib.pyplot.imread('path name')
    ```

    2.output (show image in screen)
    
    可以利用 OpenCV  
    ```
    cv2.imshow('image name', image object)
    cv2.waitkey(0)
    # cv2.waitkey(0) 是為了讓圖片停留在螢幕上，直到按q才會跳出，waitkey()中間放的是等待的時間，以ms為單位，0 的話表示無限等待
    ```
    或是利用 matplotlib.pyplot 
    ```
    matplotlib.pyplot.imshow(image object)
    matplotlib.pyplot.show()
    ```
    
    3.如果是想將圖片寫入檔案
    
    可以利用 OpenCV  
    ```
    cv2.imwrite('image name', image object)
    ```



    圖片讀入後是以陣列的方式儲存，彩色圖片會有三個channel，因此是三維陣列，因為作業給的範例圖片是灰色的，因此其實可以利用`cv2.IMREAD_GRAYSCALE`將圖片讀取進來，這樣只會有一個channel
    
    完整的寫法如下
    ```
    cv2.imread('path name', cv2.IMREAD_GRAYSCALE)
    ```
    
    也可以利用 Numpy 的功能`(image object).shape`來確認三維陣列分別的大小
    
- 作業
    基本上就是上下翻轉矩陣，以及左右翻轉矩陣，並將圖片輸出即可



