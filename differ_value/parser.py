import xml.dom.minidom
import differ_value.bean as bean


def parse(xmlfile):
    dom = xml.dom.minidom.parse(xmlfile)
    root = dom.documentElement
    document = bean.Document()  # 创建对象
    outpath = root.getElementsByTagName('outpath')[0].firstChild.data
    document.set_outpath(outpath)
    # 获取节点
    items = root.getElementsByTagName('item')
    for item in items:
        obj_item = bean.Item()
        # 获取坐标点
        nodes = item.childNodes
        for node in nodes:
            if node.nodeName == 'path':
                author = node.getAttribute('author')
                path = node.firstChild.data
                obj_item.add_path(author, path)
            elif node.nodeName == 'anchor':
                str = node.firstChild.data
                obj_item.set_anchor(str)
            elif node.nodeName == 'dirname':
                str = node.firstChild.data
                obj_item.set_name(str)
        document.add_items(obj_item)
    return document
