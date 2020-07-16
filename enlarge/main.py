import enlarge.parser as parser
import enlarge.operator as operator

if __name__ == '__main__':
    xmlfile = './config/854.xml'
    document = parser.parse(xmlfile)
    operator.operate(document)

