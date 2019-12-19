import cv2
import os
from skimage import measure
# from skimage import metrics


def psnr(img_path1, img_path2):
    img1 = cv2.imread(img_path1)
    img2 = cv2.imread(img_path2)
    # return metrics.peak_signal_noise_ratio(img1, img2, 255)
    return measure.compare_psnr(img1, img2, 255)


def ssim(img_path1, img_path2):
    img1 = cv2.imread(img_path1)
    img2 = cv2.imread(img_path2)
    # return metrics.structural_similarity(img1, img2, data_range=255, multichannel=True)
    return measure.compare_ssim(img1, img2, data_range=255, multichannel=True)


def calc(src, label):
    dirs = os.listdir(src)
    psnr_total = 0.0
    ssim_total = 0.0
    count = 0
    for item in dirs:
        print(item)
        blur_list = os.listdir(os.path.join(src, item))
        psnr_file = '{}/{}.txt'.format(src, item)
        with open(psnr_file, 'w') as f:
            _psnr = 0.0
            _ssim = 0.0
            _count = 0
            for img_name in blur_list:
                p1 = os.path.join(src, item, img_name)
                p2 = os.path.join(label, item, 'sharp', img_name)
                print('input:{}'.format(p1))
                psnr_v = psnr(p1, p2)
                ssim_v = ssim(p1, p2)
                print('img_name:{}\tpsnr:{}\tssim:{}'.format(img_name, psnr_v, ssim_v))
                f.write('img_name:{}\tpsnr:{}\tssim:{}\n'.format(img_name, psnr_v, ssim_v))
                _psnr += psnr_v
                _ssim += ssim_v
                _count += 1
            psnr_total += _psnr
            ssim_total += _ssim
            count += _count
            _psnr /= _count
            _ssim /= _count
            f.write('mean psnr:{}\tssim:{}\n'.format(_psnr, _ssim))
    psnr_total /= count
    ssim_total /= count
    f = open('{}/total_psnr.txt'.format(src), 'w')
    print('mean psnr:{}\tssim:{}'.format(psnr_total, ssim_total))
    f.write('mean psnr:{}\tssim:{}\n'.format(psnr_total, ssim_total))
    f.close()


def calc_single_dir(src, label, file_name):
    blur_list = os.listdir(src)
    psnr_file = '{}/{}.txt'.format(src, file_name)
    with open(psnr_file, 'w') as f:
        _psnr = 0.0
        _ssim = 0.0
        _count = 0
        for img_name in blur_list:
            p1 = os.path.join(src, img_name)
            p2 = os.path.join(label, 'sharp', img_name)
            print('input:{}'.format(p1))
            psnr_v = psnr(p1, p2)
            ssim_v = ssim(p1, p2)
            print('img_name:{}\tpsnr:{}\tssim:{}'.format(img_name, psnr_v, ssim_v))
            f.write('img_name:{}\tpsnr:{}\tssim:{}\n'.format(img_name, psnr_v, ssim_v))
            _psnr += psnr_v
            _ssim += ssim_v
            _count += 1
        _psnr /= _count
        _ssim /= _count
        f.write('mean psnr:{}\tssim:{}\n'.format(_psnr, _ssim))


if __name__ == '__main__':
    src = r'E:\experimental\gopro_compare\2017_Nah\temp\GOPR0384_11_00'
    label = r'E:\data\GOPRO_Large\test/GOPR0384_11_00'
    # calc(src, label)
    calc_single_dir(src, label, 'GOPR0384_11_00')
