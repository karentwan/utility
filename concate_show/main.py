from concate_show.operator import Operate
from concate_show.whole_operate import Document


def concate_part():
    '''
    将图像和放大区域拼成一张图
    :return:
    '''
    file = './xml/854.xml'
    ops = Operate()
    document = ops.parse(file)
    ops.operate(document)
    print('Done...')

def concate_img():
    '''
    将各大方法的同一张效果图拼接在一张大图里面
    :return:
    '''
    file = 'xml/all_image.xml'
    doc = Document()
    doc.parse(file)
    doc.save_in_whole()
    print('process Done')

if __name__ == '__main__':
    # concate_part()
    concate_img()


