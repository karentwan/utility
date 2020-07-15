import os
import csv


class PSNR(object):

    def __init__(self, img_name, psnr, ssim):
        self.img_name = img_name
        self.psnr = psnr
        self.ssim = ssim

    def __str__(self):
        str = '[name:{}, psnr:{}, ssim:{}]'.format(self.img_name, self.psnr, self.ssim)
        return str


class Item(object):

    def __init__(self):
        self.name = None
        self.paths = dict()
        self.anchor = None
        self.diff_value = dict()  # {key: list}

    def _parse_str(self, key, path):
        print('开始解析文件：{}'.format(path))
        with open(path, 'r') as f:
            reader = list(csv.reader(f))
            psnr_list = []
            for row in range(1, len(reader)):
                item = reader[row]
                # print(item)
                psnr_list.append(PSNR(item[0], float(item[1]), float(item[2])))
            self.diff_value[key] = psnr_list

    def _calc_diff(self, list_value, anchor_list):
        # print('开始计算-----')
        for i in range(0, len(list_value)):
            psnr_obj = list_value[i]
            anchor_obj = anchor_list[i]
            psnr_obj.psnr = anchor_obj.psnr - psnr_obj.psnr
            psnr_obj.ssim = anchor_obj.ssim - psnr_obj.ssim
            list_value[i] = psnr_obj
            print(psnr_obj)

    def calculate_diff(self):
        anchor_path = '{}/{}.csv'.format(self.get_path(self.anchor), self.get_name())
        self._parse_str(self.anchor, anchor_path)
        for item in self.keys():
            # print('开始计算{}\tanchor:{}...'.format(item, self.anchor))
            if item == self.anchor:
                print(item)
                continue
            path = '{}/{}.csv'.format(self.get_path(item), self.get_name())
            self._parse_str(item, path)
            psnr_list = self.diff_value[item]
            anchor_list = self.diff_value[self.anchor]
            self._calc_diff(psnr_list, anchor_list)

    def write_to_file(self, path):
        for key in self.keys():
            list_obj = self.diff_value[key]
            list_obj.sort(key=lambda obj: -obj.psnr)
            dir = os.path.join(path, self.get_name())
            if not os.path.exists(dir):
                os.makedirs(dir)
            file_path = os.path.join(dir, '{}.csv'.format(key))
            with open(file_path, 'w') as f:
                str = 'img_name, psnr_diff, ssim_diff\n'
                f.write(str)
                for item in list_obj:
                    str = '{}, {}, {}\n'.format(item.img_name, item.psnr, item.ssim)
                    f.write(str)

    def set_anchor(self, anchor):
        self.anchor = anchor

    def get_anchor(self):
        return self.anchor

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def add_path(self, key, path):
        self.paths[key] = path

    def keys(self):
        return self.paths.keys()

    def get_path(self, key):
        return self.paths[key]


class Document(object):

    def __init__(self):
        self.outpath = None
        self.items = []

    def add_items(self, item):
        self.items.append(item)

    def get_item(self, index):
        return self.items[index]

    def set_outpath(self, outpath):
        self.outpath = outpath

    def get_outpath(self):
        return self.outpath
