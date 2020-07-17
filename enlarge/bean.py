
class Point(object):

    def __init__(self, x, y, h, w):
        self.x = int(x)
        self.y = int(y)
        self.h = int(h)
        self.w = int(w)


class Item(object):

    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255)
    ]

    @staticmethod
    def get_color(index):
        return Item.colors[index % 3]

    def __init__(self):
        self.name = None
        self.points = []
        self.paths = dict()
        self.label_key = None
        self.dir_name = None
        self.ref = None

    def set_ref(self, ref):
        self.ref = ref

    def gt_ref(self):
        return self.ref

    def generate_director_name(self):
        name = self.name.split('.')[0]
        if self.label_key is not None:
            dir = self.paths[self.label_key].split('/')[-1]
            self.dir_name = '{}_{}'.format(dir, name)
        else:
            self.dir_name = name

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

    def add_point(self, p):
        self.points.append(p)

    def get_all_points(self):
        return self.points

    def get_point(self, index):
        return self.points[index]

    def set_label(self, label):
        self.label_key = label

    def get_label(self):
        if self.label_key is not None:
            return self.paths[self.label_key]
        return None


class Document(object):

    def __init__(self):
        self.ratio = 2  # 放大倍数
        self.outpath = None
        self.items = []
        self.calcpsnr = False  # 是否计算psnr

    def add_items(self, item):
        self.items.append(item)

    def get_item(self, index):
        return self.items[index]

    def set_ratio(self, ratio):
        self.ratio = int(ratio)

    def get_ratio(self):
        return self.ratio

    def set_merge(self, merge):
        self.merge = True if merge.lower() == 'true' else False

    def set_calcpsnr(self, flag):
        self.calcpsnr = True if flag.lower() == 'true' else False

    def get_calcpsnr(self):
        return self.calcpsnr

    def get_merge(self):
        return self.merge

    def set_outpath(self, outpath):
        self.outpath = outpath

    def get_outpath(self):
        return self.outpath
