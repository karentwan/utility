from enlarge.operator import Operator

if __name__ == '__main__':
    xmlfile = './config/compare_dccan_share_with_others_real.xml'
    opr = Operator(xmlfile)
    opr.operate()

