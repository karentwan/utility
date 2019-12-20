import concate_show.operator as ops


if __name__ == '__main__':
    file = './xml/854.xml'
    document = ops.parse(file)
    ops.operate(document)
    print('Done...')
