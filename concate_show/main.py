import concate_show.operator as ops


if __name__ == '__main__':
    file = './test.xml'
    document = ops.parse(file)
    ops.operate(document)
    print('Done...')
