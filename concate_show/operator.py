import numpy as np
import cv2
import xml.dom.minidom
import os


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
        self.local_number = int(s)

    def set_describe(self, str):
        self.describe = str


class Strategy(object):

    def __init__(self):
        pass

    def concate(self, item):
        raise NotImplementedError('please implements')


class InnerStrategy(Strategy):

    def concate(self, item):
        img_path = item.image_name
        local_path = item.local_imgs[0]
        img = cv2.imread(img_path)
        local = cv2.imread(local_path)
        [h, w, c] = img.shape
        [h1, w1, c] = local.shape
        img[h - h1:, w - w1:, :] = local
        return img


class OuterStrategy(Strategy):

    def __init__(self):
        self.span1 = 5
        self.span2 = 3

    def concate(self, item):
        imgpath = item.image_name
        local_path1 = item.local_imgs[0]
        local_path2 = item.local_imgs[1]
        img = cv2.imread(imgpath)
        local1 = cv2.imread(local_path1)
        local2 = cv2.imread(local_path2)
        local3 = None
        # print('===========>local_path:{}'.format(local_path1))
        if item.local_number == 3:
            local3 = cv2.imread(item.local_imgs[2])
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
        local = np.full((h2, w1 + w2 + self.span2, 3), 255, np.uint8)
        local[:, :w1, :] = local1
        local[:, w1 + self.span2:, :] = local2
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
            image = np.full((h1 + h2 + h3 + 2 * self.span1, w, 3), 255, np.uint8)
            image[:h1, :, :] = img
            image[h1 + self.span1: h1 + self.span1 + h2, :, :] = local
            image[h1 + h2 + 2 * self.span1:, :, :] = local3
        else:
            image = np.full((h1 + h2 + self.span1, w, 3), 255, np.uint8)
            image[:h1, :, :] = img
            image[h1 + self.span1:, :, :] = local
        return image


class Context(object):

    def __init__(self):
        self.strategy = None

    def set_strategy(self, strategy):
        self.strategy = strategy

    def concate(self, item):
        return self.strategy.concate(item)


class Operate(object):

    def __init__(self):
        self.context = Context()

    def parse(self, xmlfile):
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
                    # print('parse----------localnumber:{}'.format(str))
                    obj_item.set_local_number(str)
                elif node.nodeName == 'describe':
                    str = node.firstChild.data
                    obj_item.set_describe(str)
            document.add_item(obj_item)
        return document

    def operate_item(self, item):
        local_number = item.local_number
        # print('local number:{}'.format(local_number))
        if local_number == 1:
            self.context.set_strategy(InnerStrategy())
        else:
            self.context.set_strategy(OuterStrategy())
        image = self.context.concate(item)
        [h, w, _] = image.shape
        return image, h, w

    def save_in_bulk(self, imgs, path):
        for key in imgs.keys():
            img_path = os.path.join(path, '{}.jpg'.format(key))
            img = imgs[key]
            # print('=======>img_path:{}'.format(img_path))
            cv2.imwrite(img_path, img)

    def operate(self, document):
        items = document.get_items()
        images = dict()
        h = w = 0
        for i, item in enumerate(items):
            image, h, w = self.operate_item(item)
            images[item.describe] = image
            # images.append(image)
        self.save_in_bulk(imgs=images, path=document.outputpath)

