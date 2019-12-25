import concate_show.operator as ops


if __name__ == '__main__':
    file = './xml/GOPR0384_11_00_000002.xml'
    document = ops.parse(file)
    ops.operate(document, 100)
    print('Done...')
