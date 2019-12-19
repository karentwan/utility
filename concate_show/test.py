import cv2
import numpy as np

img_path = r'E:\experimental\compare_experimental_local_magnify\our_four_level_compare_with_others\000007/img_blur.png'
local_path1 = r'E:\experimental\compare_experimental_local_magnify\our_four_level_compare_with_others\000007/local_blur_x276_y31.png'
local_path2 = r'E:\experimental\compare_experimental_local_magnify\our_four_level_compare_with_others\000007/local_blur_x492_y282.png'


def calculate_scale(img, local1, local2):
    # print('shape1:{}\tshape2:{}\tshape3:{}'.format(shape1, shape2, shape3))
    [h, w, _] = img.shape
    [h1, w1, _] = local1.shape
    [h2, w2, _] = local2.shape
    if w2 > w1:
        temp = local1
        local1 = local2
        local2 = temp
        [h1, w1, _] = local1.shape
        [h2, w2, _] = local2.shape
    scale_ratio_img = w / h
    scale_ratio_local1 = w1 / h1
    w = w1
    h = int(w / scale_ratio_img)
    img = cv2.resize(img, (w, h))
    h1 = h2
    w1 = int(h1 * scale_ratio_local1)
    local1 = cv2.resize(local1, (w1, h1))
    local = np.full((h2, w1 + w2 + 3, 3), 255, dtype=np.uint8)
    local[:, :w1, :] = local1
    local[:, w1 + 3:, :] = local2
    # local = np.concatenate([local1, local2], axis=1)
    [h3, w3, _] = local.shape
    print('img.shape:{}\tlocal.shape:{}'.format(img.shape, local.shape))
    # local区域比图像大，则缩放local
    if w3 > w:
        h3 = int(w * h3 / w3)
        w3 = w
        local = cv2.resize(local, (w3, h3))
    # 图像比local大，则缩放图像
    else:
        h = int(w3 * h / w)
        w = w3
        img = cv2.resize(img, (w, h))
    print('img.shape:{}\tlocal.shape:{}'.format(img.shape, local.shape))
    image = np.full((h + h3 + 5, w, 3), 255, dtype=np.uint8)
    image[:h, :w, :] = img
    image[h + 5:, :, :] = local
    return image


if __name__ == '__main__':
    canvas = np.zeros((600, 600, 3), dtype='uint8')
    img = cv2.imread(img_path)
    local1 = cv2.imread(local_path1)
    local2 = cv2.imread(local_path2)
    image = calculate_scale(img, local1, local2)
    cv2.imwrite(r'D:\experimental\test/img3.jpg', image)


