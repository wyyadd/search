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
    print("done")
