

def _operate_item(item, outpath):
    item.calculate_diff()
    item.write_to_file(outpath)


def operate(document):
    print('开始对计算差值, 并将结果按从大到小排序...')
    outpath = document.get_outpath()
    print('图片输出路径:{}'.format(outpath))
    # 开始处理
    for item in document.items:
        _operate_item(item, outpath)
    print('处理完成')
