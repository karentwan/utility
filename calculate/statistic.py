import os


class PSNR(object):
    def __init__(self, dir_name, p_val, s_val):
        self.dir_name = dir_name
        self.p_val = p_val
        self.s_val = s_val

    def display(self):
        print('dir_name:{}\tpsnr:{}\tssim:{}'.format(self.dir_name, self.p_val, self.s_val))


root_path = r'E:\experimental\gopro_compare\2017_Nah\temp'

filenames = ['GOPR0384_11_00.txt', 'GOPR0384_11_05.txt', 'GOPR0385_11_01.txt', 'GOPR0396_11_00.txt',
             'GOPR0410_11_00.txt', 'GOPR0854_11_00.txt', 'GOPR0862_11_00.txt', 'GOPR0868_11_00.txt',
             'GOPR0869_11_00.txt', 'GOPR0871_11_00.txt', 'GOPR0881_11_01.txt']


def calc(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        psnr_total = 0.
        ssim_total = 0.
        count = 0
        for line in lines:
            # print(line)
            str_arr = line.split('\t')
            # print(str_arr)
            psnr_val = float(str_arr[1].split(':')[1])
            ssim_val = float(str_arr[2].split(':')[1])
            psnr_total += psnr_val
            ssim_total += ssim_val
            count += 1
        print('psnr_total:{}\tssim_total:{}'.format(psnr_total, ssim_total))
        return psnr_total, ssim_total, psnr_total / count, ssim_total / count, count


def statistic():
    psnr_total = 0.
    ssim_total = 0.
    count = 0
    psnr_file = os.path.join(root_path, 'eveything.txt')
    psnr_list = []
    f = open(psnr_file, 'w')
    for item in filenames:
        path = os.path.join(root_path, item)
        local_psnr_sum, local_ssim_sum, psnr, ssim, local_count = calc(path)
        psnr_list.append(PSNR(item, psnr, ssim))
        f.write('{}\tpsnr:{}\tssim:{}\n'.format(item, psnr, ssim))
        psnr_total += local_psnr_sum
        ssim_total += local_ssim_sum
        count += local_count
    psnr_total /= count
    ssim_total /= count
    psnr_list.append(PSNR('total_psnr', psnr_total, ssim_total))
    f.write('mean psnr:{}\tssim:{}\n'.format(psnr_total, ssim_total))
    print('mean psnr:{}\tssim:{}'.format(psnr_total, ssim_total))
    # 生成latex需要的数据格式
    f.write('nextline\'s data is generated for latex table data format \n')
    for item in psnr_list:
        f.write('&{:.2f}dB/{:.4f}'.format(item.p_val, item.s_val))
    f.write('\n')
    f.close()


def statistic_v2():
    psnr_file = os.path.join(root_path, 'eveything.txt')
    psnr_list = []
    f = open(psnr_file, 'w')
    for item in filenames:
        path = os.path.join(root_path, item)
        with open(path, 'r') as f_temp:
            str = f_temp.readlines()
            values = str[-1].split('\t')
            psnr_value = float(values[0].split(':')[1])
            ssim_value = float(values[1].split(':')[1])
            f.write('{}\tpsnr:{}\tssim:{}\n'.format(item, psnr_value, ssim_value))
            # print('psnr_value:{:.2f}\tssim_value:{:.4f}'.format(psnr_value, ssim_value))
            psnr_list.append(PSNR(item, psnr_value, ssim_value))
    total_file_name = 'total_psnr.txt'
    path = os.path.join(root_path, total_file_name)
    with open(path, 'r') as f_temp:
        str = f_temp.readlines()
        values = str[0].split('\t')
        psnr_value = float(values[0].split(":")[1])
        ssim_value = float(values[1].split(':')[1])
        f.write('mean psnr:{}\tssim:{}\n'.format(psnr_value, ssim_value))
        psnr_list.append(PSNR(total_file_name, psnr_value, ssim_value))
        # print(str)
    for item in psnr_list:
        item.display()
        f.write('&{:.2f}dB/{:.4f}'.format(item.p_val, item.s_val))
    f.close()


if __name__ == '__main__':
    # statistic_v2()
    statistic()
