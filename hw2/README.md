## Computer vision homework 2

### homework discripition
Write a program to generate

1. a binary image (threshold at 128)

2. a histogram

3. connected components(regions with '+' at centroid, bounding box)

### how to implement

-  a binary image (threshold at 128)
    以下是 `thresholding` 的定義
    將圖片做 thresholding 完後，我們可以得到一張 `binary image`
    因為 thresholding 就是判斷圖片中每個 pixel，如果 pixel 的灰度值大於 threshold 的值，就設成灰度極大值，反之設成灰度極小值。
    這麼一來，圖片中只會剩下兩種數值，因此就是 `binary image`
    因此，只要一一判斷圖片中每個 pixel 的 value，就可以完成這份作業
    
    >Thresholding is the assignment of each pixel in an image to either a true or false class based on the pixel's value, location or both. The result of a thresholding operation is typically a binary image in which each pixel is assigned either a true or false value.
 
     reference: 
     `https://computervision.fandom.com/wiki/Thresholding`
`https://en.wikipedia.org/wiki/Thresholding_(image_processing)`

    
-  a histogram
    統計每個灰度值共有幾個 pixel，再將其以直方圖表示
    直方圖以 python 的實作方法如下
    ```
    plt.bar(range(0, 256), hist, color = 'black')
    ```
- connected components(regions with '+' at centroid, bounding box) 
    首先要先標記每個點的 label id，我是利用 iterative algorithm 去標記
    標記完後，就可以統計面積超過 500 的 label id 的 pixel
    最後一步就是計算這些 label id 的重心位置，並畫框以及標記重心
    python 畫框以及在中心畫十字線的的方法，如下所示：
    ```
    cv2.rectangle(image, (左上座標), (右下座標), (匡線顏色), 粗度) #draw retangle
    cv2.line(image, (起始點), (終點), (顏色), 粗度) #直線    
    ```