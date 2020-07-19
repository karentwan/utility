import xml.dom.minidom
import cv2
import numpy as np


class Document(object):

    def __init__(self):
        self.items = []
        self.width = None
        self.out_path = None
        self.span = 10

    def concate_in_axis_0(self, img1, img2):
        '''
        在第0维坐标上拼接, 因此要保证img1和img2的w一样大, 如果w1>w2, 那么扩展w2的大小, 否则扩展w1直至两个大小一样大
        :param img1:
        :param img2:
        :return:
        '''
        h1, w1, _ = img1.shape
        h2, w2, _ = img2.shape
        if w1 > w2:
            tmp = np.full((h2, w1, 3), fill_value=255)
            tmp[:, :w2, :] = img2
            img2 = tmp
        elif w2 > w1:
            tmp = np.full((h1, w2, 3), fill_value=255)
            tmp[:, :w1, :] = img1
            img1 = tmp
        img1 = np.concatenate([img1, img2], axis=0)
        return img1

    def save_in_whole(self):
        print('start process')
        cat_img = None
        for col_index, item in enumerate(self.items):
            length = len(item.keys())
            h, w, row_img = None, None, None
            print('======================>cat all method in picture')
            for index, key in enumerate(item.keys()):
                print('process picture :{}'.format(key))
                img_path = item[key]
                img = cv2.imread(img_path)
                img_h, img_w, _ = img.shape
                if img_w != self.width:
                    img_h = int((img_h * self.width) / img_w)
                    img_w = int(self.width)
                if row_img is None:
                    h = int(img_h + 2 * self.span)
                    w = int(img_w * length + (length + 1) * self.span)
                    row_img = np.full((h, w, 3), fill_value=255)
                img = cv2.resize(img, (img_w, img_h))
                # print('dst shape:{}\timg shape:{}'.format(row_img[self.span:self.span + img_h, index * img_w + (index+1) * self.span:(index+1) * img_w + (index+1) * self.span, :].shape, img.shape))
                row_img[self.span:self.span + img_h, index * img_w + (index+1) * self.span:(index+1) * img_w + (index+1) * self.span, :] = img[...]
                index += 1
            print('======================>process over')
            if cat_img is None:
                cat_img = row_img
            else:
                # cat_img = np.concatenate([cat_img, row_img], axis=0)
                cat_img = self.concate_in_axis_0(cat_img, row_img)
        cv2.imwrite(self.out_path, cat_img)

    def parse(self, xmlfile):
        dom = xml.dom.minidom.parse(xmlfile)
        root = dom.documentElement
        outpath = root.getElementsByTagName('outpath')[0].firstChild.data
        width = root.getElementsByTagName('width')[0].firstChild.data
        span_tag = root.getElementsByTagName('span')
        if len(span_tag) > 0:
            self.span = int(span_tag[0].firstChild.data)
        # print('span:{}'.format(self.span))
        self.out_path = outpath
        self.width = int(width)
        # 获取节点
        items = root.getElementsByTagName('item')
        for item in items:
            obj_item = dict()
            # 获取坐标点
            nodes = item.childNodes
            for node in nodes:
                if node.nodeName == 'path':
                    author = node.getAttribute('author')
                    path = node.firstChild.data
                    obj_item[author] = path
            self.items.append(obj_item)