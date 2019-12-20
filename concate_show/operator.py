import numpy as np
import cv2
import xml.dom.minidom


class Document(object):

    def __init__(self):
        super(Document, self).__init__()
        self.outputpath = ''
        self.items = []

    def set_outpath(self, path):
        self.outputpath = path

    def add_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items


class Item(object):
    def __init__(self):
        super(Item, self).__init__()
        self.image_name = ''
        self.local_imgs = []
        self.local_number = 2
        self.describe = ''

    def set_image_name(self, name):
        self.image_name = name

    def add_local_img(self, imgname):
        self.local_imgs.append(imgname)

    def set_local_number(self, s):
        self.local_number = 3 if s == '3' else 2

    def set_describe(self, str):
        self.describe = str


def parse(xmlfile):
    dom = xml.dom.minidom.parse(xmlfile)
    root = dom.documentElement
    document = Document()  # 创建对象
    outpath = root.getElementsByTagName('outpath')[0].firstChild.data
    document.set_outpath(outpath)
    # 获取节点
    items = root.getElementsByTagName('item')
    for item in items:
        obj_item = Item()
        # 获取坐标点
        nodes = item.childNodes
        for node in nodes:
            if node.nodeName == 'imgname':
                str = node.firstChild.data
                obj_item.set_image_name(str)
            elif node.nodeName == 'localimg':
                str = node.firstChild.data
                obj_item.add_local_img(str)
            elif node.nodeName == 'localnumber':
                str = node.firstChild.data
                obj_item.set_local_number(str)
            elif node.nodeName == 'describe':
                str = node.firstChild.data
                obj_item.set_describe(str)
        document.add_item(obj_item)
    return document


# 拼接两张图
def calculate_scale(img, local1, local2, local3=None, span1=5, span2=3):
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
    local = np.full((h2, w1 + w2 + span2, 3), 255, dtype=np.uint8)
    local[:, :w1, :] = local1
    local[:, w1 + span2:, :] = local2
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
    if local3 is None:
        image = np.full((h + h3 + span1, w, 3), 255, dtype=np.uint8)
        image[:h, :w, :] = img
        image[h + span1:, :, :] = local
    else:  # 添加第三个局部区域
        [h4, w4, _] = local3.shape
        # print('')
        h4 = int(w4 * h / w)
        w4 = w
        local3 = cv2.resize(local3, (w4, h4))
        image = np.full((h + h3 + h4 + 2 * span1, w, 3), 255, dtype=np.uint8)
        image[:h, :w, :] = img
        image[h + span1:, :, :] = local
        image[h + h3 + 2 * span1, :, :] = local3
    return image


def calculate_scale_v(img, local1, local2, local3=None, span1=5, span2=3):
    [h1, w1, _] = local1.shape
    [h2, w2, _] = local2.shape
    # 将local1和local2拼接在一起
    if h1 > h2:  # 以h2为基准
        w1 = int(h2 * w1 / h1)
        h1 = h2
        local1 = cv2.resize(local1, (w1, h1))
    else:  # 以h1为基准
        w2 = int(h1 * w2 / h2)
        h2 = h1
        local2 = cv2.resize(local2, (w2, h2))
    local = np.full((h2, w1 + w2 + span2, 3), 255, np.uint8)
    local[:, :w1, :] = local1
    local[:, w1 + span2:, :] = local2
    # 拼接成功, next 判断Local, img, local3谁最小就以谁为基准
    [h1, w1, _] = img.shape
    [h2, w2, _] = local.shape
    min = img
    min_w = w1
    if w2 < min_w:
        min = local
        min_w = w2
    if local3 is not None:
        [h3, w3, _] = local3.shape
        if w3 < min_w:
            min = local3
            min_w = w3
    [h, w, _] = min.shape
    h1 = int(w * h1 / w1)
    w1 = w
    img = cv2.resize(img, (w1, h1))
    h2 = int(w * h2 / w2)
    w2 = w
    local = cv2.resize(local, (w2, h2))
    if local3 is not None:
        [h3, w3, _] = local3.shape
        h3 = int(w * h3 / w3)
        w3 = w
        local3 = cv2.resize(local3, (w3, h3))
        image = np.full((h1 + h2 + h3 + 2 * span1, w, 3), 255, np.uint8)
        image[:h1, :, :] = img
        image[h1 + span1: h1 + span1 + h2, :, :] = local
        image[h1 + h2 + 2*span1:, :, :] = local3
    else:
        image = np.full((h1 + h2 + span1, w, 3), 255, np.uint8)
        image[:h1, :, :] = img
        image[h1+span1:, :, :] = local
    return image


def operate_item(item):
    img = cv2.imread(item.image_name)
    local_number = item.local_number
    local1 = cv2.imread(item.local_imgs[0])
    local2 = cv2.imread(item.local_imgs[1])
    if local_number == 3:
        local3 = cv2.imread(item.local_imgs[2])
        image = calculate_scale_v(img, local1, local2, local3)
    else:
        image = calculate_scale_v(img, local1, local2)
    [h, w, _] = image.shape
    return image, h, w


def operate(document):
    items = document.get_items()
    images = []
    h = w = 0
    for item in items:
        image, h, w = operate_item(item)
        images.append(image)
        # print()
    image = np.full((2 * h + 5, 4 * w + 3 * 5, 3), 255, dtype=np.uint8)
    for i in range(2):
        for j in range(4):
            x0 = i * h + i * 5
            x1 = x0 + h
            y0 = j * w + j * 5
            y1 = y0 + w
            image[x0: x1, y0: y1, :] = images[i * 4 + j]
    cv2.imwrite(document.outputpath, image)

