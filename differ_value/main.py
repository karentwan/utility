import differ_value.parser as parser
import differ_value.operator as operator

if __name__ == '__main__':
    xmlfile = './config/different_value.xml'
    document = parser.parse(xmlfile)
    operator.operate(document)
