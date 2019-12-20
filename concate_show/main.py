import concate_show.operator as ops


if __name__ == '__main__':
    file = './xml/GOPR0854_11_00_000004.xml'
    document = ops.parse(file)
    ops.operate(document)
    print('Done...')
