import cv2
import os
from enlarge.bean import Item
from skimage import measure
from enlarge.parser import parse


class Operator(object):

    def __init__(self, xmlfile):
        self.ref_h = None
        self.ref_w = None
        self.xmlfile = xmlfile

    def psnr(self, img_path1, img_path2):
        img1 = cv2.imread(img_path1)
        img2 = cv2.imread(img_path2)
        return measure.compare_psnr(img1, img2, 255)

    def ssim(self, img_path1, img_path2):
        img1 = cv2.imread(img_path1)
        img2 = cv2.imread(img_path2)
        return measure.compare_ssim(img1, img2, data_range=255, multichannel=True)

    def fixed_picture(self, img, points):
        assert img is not None, '要放大的图像不能为空, 请检查要放大图像的路径是否为空'
        h, w, _ = img.shape
        if self.ref_h is not None and (h != self.ref_h or w != self.ref_w):
            img = cv2.resize(img, (self.ref_w, self.ref_h))
        return img

    def _enlarge(self, filepath, points, ratio, outpath, key, img_name, thickness=2):
        img = cv2.imread(filepath)
        img = self.fixed_picture(img, points)
        for index, p in enumerate(points):
            local = img[p.y:p.y + p.h, p.x:p.x + p.w, :]
            local = cv2.resize(local, (p.w * ratio, p.h * ratio))
            cv2.rectangle(local, (0, 0), (p.w * ratio, p.h * ratio), Item.get_color(index), thickness * 2)
            _outpath = os.path.join(outpath, 'local_{}_{}.png'.format(key, index))
            cv2.imwrite(_outpath, local)
        # 在原图上画矩形
        for index, p in enumerate(points):
            img = cv2.rectangle(img, (p.x, p.y), (p.x + p.w, p.y + p.h), Item.get_color(index), thickness)
        print('保存的图像名：{}'.format(img_name))
        cv2.imwrite(img_name, img)

    def _get_ref_for_img(self, item):
        '''
        为图片得到用来参考的图片大小, 如此便可以resize所有图像到统一大小
        :return:
        '''
        if item.ref is not None:
            ref_path = os.path.join(item.get_path(item.ref), item.get_name())
            img = cv2.imread(ref_path)
            assert img is not None, 'img 不能为空, 请检查ref路径是否正确'
            self.ref_h, self.ref_w, _ = img.shape
            return self.ref_h, self.ref_w
        return None, None

    def _get_label_path(self, item):
        if item.get_label() is not None:
            return os.path.join(item.get_label(), item.get_name())
        return None

    def _operate_item(self, item, ratio, outpath, calc):
        name = item.get_name().split('.')[0]
        _outdir = os.path.join(outpath, item.dir_name)
        if not os.path.exists(_outdir):
            os.makedirs(_outdir)
        # 处理图片
        keys = item.keys()
        infor_file = '{}/information.txt'.format(_outdir)
        f = open(infor_file, 'w')
        label_path = self._get_label_path(item)
        self._get_ref_for_img(item)
        for key in keys:
            path = os.path.join(item.get_path(key), item.get_name())
            img_name = os.path.join(_outdir, 'img_{}.png'.format(key))
            if not path == label_path and calc:
                psnr_val = self.psnr(path, label_path)
                ssim_val = self.ssim(path, label_path)
                f.write('{}/img_{}.png\tpsnr_val:{}\tssim_val:{}\n'.format(name, key, psnr_val, ssim_val))
            else:
                f.write('{}/img_{}.png\n'.format(name, key))
            self._enlarge(path, item.get_all_points(), ratio, _outdir, key, img_name)
        f.close()

    def operate(self):
        document = parse(self.xmlfile)
        print('开始对图片局部进行放大...')
        ratio = document.get_ratio()
        outpath = document.get_outpath()
        calcpsnr = document.get_calcpsnr()
        print('图片放大比例:{}'.format(ratio))
        print('图片输出路径:{}'.format(outpath))
        print('是否计算图像的psnr:{}'.format(calcpsnr))
        # 开始处理
        for item in document.items:
            self._operate_item(item, ratio, outpath, calcpsnr)
        print('处理完成')
