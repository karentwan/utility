import enlarge.parser as parser
import enlarge.operator as operator

if __name__ == '__main__':
    xmlfile = './test.xml'
    document = parser.parse(xmlfile)
    operator.operate(document)



