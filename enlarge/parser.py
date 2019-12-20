import xml.dom.minidom
import enlarge.bean as bean


def get_point(p):
    x = p.getElementsByTagName('x')[0].firstChild.data
    y = p.getElementsByTagName('y')[0].firstChild.data
    h = p.getElementsByTagName('h')[0].firstChild.data
    w = p.getElementsByTagName('w')[0].firstChild.data
    return bean.Point(x, y, h, w)


def parse(xmlfile):
    dom = xml.dom.minidom.parse(xmlfile)
    root = dom.documentElement
    document = bean.Document()  # 创建对象
    merge = root.getElementsByTagName('merge')[0].firstChild.data
    outpath = root.getElementsByTagName('outpath')[0].firstChild.data
    ratio = root.getElementsByTagName('ratio')[0].firstChild.data
    calcpsnr = root.getElementsByTagName('calcpsnr')[0].firstChild.data
    document.set_merge(merge)
    document.set_outpath(outpath)
    document.set_ratio(ratio)
    document.set_calcpsnr(calcpsnr)
    # 获取节点
    items = root.getElementsByTagName('item')
    for item in items:
        obj_item = bean.Item()
        # 获取坐标点
        nodes = item.childNodes
        for node in nodes:
            if node.nodeName == 'name':
                name = node.firstChild.data
                obj_item.set_name(name)
            elif node.nodeName == 'point':
                p = get_point(node)
                obj_item.add_point(p)
            elif node.nodeName == 'path':
                author = node.getAttribute('author')
                path = node.firstChild.data
                obj_item.add_path(author, path)
            elif node.nodeName == 'label':
                label = node.firstChild.data
                obj_item.set_label(label)
        obj_item.generate_director_name()
        document.add_items(obj_item)
    return document
