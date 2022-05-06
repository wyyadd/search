# coding=utf-8
import util
import dictionary


def init_dictionary() -> dictionary.Dic:
    poem_list = []
    poem_id = 0
    for p in util.read_data():
        poem_list.append(dictionary.Poem(p, poem_id))
        poem_id += 1
    return dictionary.Dic(poem_list)


if __name__ == '__main__':
    dic = init_dictionary()
    print("东、南 并集：" + str(dic.union('东', '南')))
    print("东、南 交集：" + str(dic.intersection('东', '南')))
    print("东、南 AND NOT" + str(dic.and_not('东', '南')))
    print("东、南、人 并集：" + str(dic.union('东', '南', '人')))
    print("东、南、人 交集：" + str(dic.intersection('东', '南', '人')))

    print("明、月 并集：" + str(dic.union('明', '月')))
    print("明、月 交集：" + str(dic.intersection('明', '月')))
    print("明、月 AND NOT" + str(dic.and_not('明', '月')))
    print("明、月、人 并集：" + str(dic.union('明', '月', '人')))
    print("明、月、人 交集：" + str(dic.intersection('明', '月', '人')))

    print("done")
