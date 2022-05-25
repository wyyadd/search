# coding=utf-8
import re

import util
import dictionary


def parser():
    keys = input("请输入查询语句:")
    pattens = keys.split('or')
    res = None
    for pat in pattens:
        temps = pat.split('and')
        andterm = []
        notterm = []
        for temp in temps:
            if temp == '':
                continue
            elif 'not' in temp:
                notterm.append(temp.replace('not', ''))
            else:
                andterm.append(temp)
        ans = dic.union(*andterm)
        if len(notterm) > 0:
            for term in notterm:
                ans = util.and_not2(ans, dic.getlist(term))
        if res is None:
            res = ans
        else:
            res = util.or2_score(res, ans)
    res = sorted(res, key=lambda value: value[1], reverse=True)
    print(str(res))


# 初始化字典函数
def init_dictionary() -> dictionary.Dic:
    poem_list = []
    poem_id = 0
    for p in util.read_data():
        poem_list.append(dictionary.Poem(p, poem_id))
        poem_id += 1
    return dictionary.Dic(poem_list)


def interface():
    while 1:
        keys = input("请输入查询语句:")
        print(keys)
        if 'andnot' in keys:
            keys = keys.split('andnot')
            print("result" + str(dic.and_not(*keys)))
        elif 'and' in keys:
            keys = keys.split('and')
            print("result:" + str(dic.intersection(*keys)))
        elif 'or' in keys:
            keys = keys.split('or')
            print("result:" + str(dic.union(*keys)))


if __name__ == '__main__':
    dic = init_dictionary()
    # parser()
    print(dic.vector_search('明', '月', '人'))
    # print("测试一：")
    # print("东、南 并集：" + str(dic.union('东', '南')))
    # print("东、南 交集：" + str(dic.intersection('东', '南')))
    # print("东、南 AND NOT：" + str(dic.and_not('东', '南')))
    # print("东、南、人 并集：" + str(dic.union('东', '南', '人')))
    # print("东、南、人 交集：" + str(dic.intersection('东', '南', '人')))
    # print("测试二：")
    # print("明、月 并集：" + str(dic.union('明', '月')))
    # print("明、月 交集：" + str(dic.intersection('明', '月')))
    # print("明、月 AND NOT：" + str(dic.and_not('明', '月')))
    # print("明、月、人 并集：" + str(dic.union('明', '月', '人')))
    # print("明、月、人 交集：" + str(dic.intersection('明', '月', '人')))
    # print("done")
    # interface()
