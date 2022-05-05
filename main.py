# coding=utf-8
import util
import dictionary
from util import *

def init_dictionary() -> dictionary.Dic:
    poem_list = []
    poem_id = 0
    for p in util.read_data():
        poem_list.append(dictionary.Poem(p, poem_id))
        poem_id += 1
    return dictionary.Dic(poem_list)


if __name__ == '__main__':
    dic = init_dictionary()
    print(and2(dic.union('东', '南'),dic.ormany(['我','爱'])))    #（东 or 南）and (我 or 爱)
    print("done")
