## Computer vision homework 5 
### homework discription
Write programs which do gray-scale morphology on a gray-scale image

1. Dilation

2. Erosion

3. Opening

4. Closing

### Hints

和 hw4 的作業很像，差別是 hw4 的作業是對二值化後的圖片進行操作

因此我們在寫函式的時候不能直接照抄上次的作業

以下是幾個 gray-scale morphology 的定義

> gray-level erosion reduces the brightness of pixels that are surrounded by neighbors with a lower intensity

> A gray-level dilation increases the brightness of each pixel that is surrounded by neighbors with a higher intensity

定義中的 `neighbors` 代入我們自己定義的kernel

所以在 hw5.py 中的函式，要用 `max` 和 `min` 去找出 kernel 中最亮和最暗的 pixel 

reference:

`https://www.ni.com/docs/en-US/bundle/ni-vision-concepts-help/page/grayscale_morphology.html`

#### 灰度圖和二值化
可以使用 `matplotlib.pyplot.imshow()` 中 `camp = 'gray'` 

或是利用 `cv2.IMREAD_GRAYSCALE` 將圖片讀進來，這樣只會有一個 channel，操作上比較方便

因為預設是三個channel