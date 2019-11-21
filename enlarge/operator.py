import cv2
import os
from enlarge.bean import Item
from skimage import measure


def psnr(img_path1, img_path2):
    img1 = cv2.imread(img_path1)
    img2 = cv2.imread(img_path2)
    return measure.compare_psnr(img1, img2, 255)


def ssim(img_path1, img_path2):
    img1 = cv2.imread(img_path1)
    img2 = cv2.imread(img_path2)
    return measure.compare_ssim(img1, img2, data_range=255, multichannel=True)


def _embed_enlarge(filepath, p, ratio, color=(0, 255, 0), thickness=2):
    img = cv2.imread(filepath)
    local = img[p.y:p.y + p.h, p.x:p.x + p.w, :]
    local = cv2.resize(local, (p.w * ratio, p.h * ratio))
    # 在原图上画矩形
    img_rec = cv2.rectangle(img, (p.x, p.y), (p.x + p.w, p.y + p.h), color, thickness)
    # 将放大区域放在图像的右下角
    [h, w, c] = img.shape
    img_rec[h - p.h * ratio: h, w - p.w * ratio: w, :] = local[:, :, :]
    return img_rec


def _operate_item(item, ratio, outpath):
    points = item.points
    name = item.get_name().split('.')[0]
    _outdir = os.path.join(outpath, name)
    if not os.path.exists(_outdir):
        os.makedirs(_outdir)
    p = points[0]
    # 处理图片
    keys = item.keys()
    for key in keys:
        path = os.path.join(item.get_path(key), item.get_name())
        img = _embed_enlarge(path, p, ratio)
        _outpath = os.path.join(_outdir, 'img_{}.png'.format(key))
        cv2.imwrite(_outpath, img)


def _enlarge_v(filepath, points, ratio, outpath, key, img_name, thickness=2):
    img = cv2.imread(filepath)
    for p in points:
        local = img[p.y:p.y + p.h, p.x:p.x + p.w, :]
        local = cv2.resize(local, (p.w * ratio, p.h * ratio))
        _outpath = os.path.join(outpath, 'local_{}_x{}_y{}.png'.format(key, p.x, p.y))
        cv2.imwrite(_outpath, local)
    # 在原图上画矩形
    for index, p in enumerate(points):
        img = cv2.rectangle(img, (p.x, p.y), (p.x + p.w, p.y + p.h), Item.get_color(index), thickness)
    # _outpath = os.path.join(outpath, 'img_{}.png'.format(key))
    print('保存的图像名：{}'.format(img_name))
    cv2.imwrite(img_name, img)


def _operate_item_v(item, ratio, outpath, calc):
    name = item.get_name().split('.')[0]
    _outdir = os.path.join(outpath, name)
    if not os.path.exists(_outdir):
        os.makedirs(_outdir)
    # 处理图片
    keys = item.keys()
    infor_file = '{}/information.txt'.format(_outdir)
    f = open(infor_file, 'w')
    label_path = os.path.join(item.get_label(), item.get_name())
    for key in keys:
        path = os.path.join(item.get_path(key), item.get_name())
        img_name = os.path.join(_outdir, 'img_{}.png'.format(key))
        if not path == label_path and calc:
            psnr_val = psnr(path, label_path)
            ssim_val = ssim(path, label_path)
            f.write('{}\tpsnr_val:{}\tssim_val:{}\n'.format(path, psnr_val, ssim_val))
        else:
            f.write('{}\n'.format(path))
        _enlarge_v(path, item.get_all_points(), ratio, _outdir, key, img_name)
    f.close()


def operate(document):
    print('开始对图片局部进行放大...')
    ratio = document.get_ratio()
    outpath = document.get_outpath()
    merge = document.get_merge()
    calcpsnr = document.get_calcpsnr()
    print('图片放大比例:{}'.format(ratio))
    print('图片输出路径:{}'.format(outpath))
    print('是否将放大的图片放置在同一个图片上:{}'.format(merge))
    print('是否计算图像的psnr:{}'.format(calcpsnr))
    # 开始处理
    for item in document.items:
        if merge:
            _operate_item(item, ratio, outpath)
        else:
            _operate_item_v(item, ratio, outpath, calcpsnr)
    print('处理完成')
