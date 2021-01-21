import re

import cv2 as cv
import pytesseract
from PIL import Image



# 计算邻域非白色个数
def calculate_noise_count(img_obj, w, h):
    """
    计算邻域非白色的个数
    Args:
        img_obj: img obj
        w: width
        h: height
    Returns:
        count (int)
    """
    count = 0
    width, height, s = img_obj.shape
    for _w_ in [w - 1, w, w + 1]:
        for _h_ in [h - 1, h, h + 1]:
            if _w_ > width - 1:
                continue
            if _h_ > height - 1:
                continue
            if _w_ == w and _h_ == h:
                continue
            if (img_obj[_w_, _h_, 0] < 233) or (img_obj[_w_, _h_, 1] < 233) or (img_obj[_w_, _h_, 2] < 233):
                count += 1
    return count


# k邻域降噪
def operate_img(img, k):
    w, h, s = img.shape
    # 从高度开始遍历
    for _w in range(w):
        # 遍历宽度
        for _h in range(h):
            if _h != 0 and _w != 0 and _w < w - 1 and _h < h - 1:
                if calculate_noise_count(img, _w, _h) < k:
                    img.itemset((_w, _h, 0), 255)
                    img.itemset((_w, _h, 1), 255)
                    img.itemset((_w, _h, 2), 255)

    return img


def around_white(img):
    w, h, s = img.shape
    for _w in range(w):
        for _h in range(h):
            if (_w <= 5) or (_h <= 5) or (_w >= w - 5) or (_h >= h - 5):
                img.itemset((_w, _h, 0), 255)
                img.itemset((_w, _h, 1), 255)
                img.itemset((_w, _h, 2), 255)
    return img


def recognize_text(image):
    image = cv.imread(image)
    ret, image = cv.threshold(image, 150, 255, cv.THRESH_BINARY)
    img2 = operate_img(image, 4)
    img2 = operate_img(img2, 4)
    img2 = around_white(img2)
    gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

    ret, binary = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)

    cv.bitwise_not(binary, binary)
    cv.imshow('binary-image', binary)
    # 识别
    test_message = Image.fromarray(binary)
    text = re.sub("\D", "", pytesseract.image_to_string(test_message))
    text = int(text)
    print(f'识别结果：{text}')
    return text

# recognize_text('save.png')
# cv.waitKey(0)
# cv.destroyAllWindows()