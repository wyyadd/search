# coding=utf-8
import util
import dictionary


def parser():
    keys = input("请输入查询语句:")
    pattens = keys.split('or')
    title_res = None
    content_res = None
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
        content_ans = dic.vector_search(*andterm)
        content_ans = sorted(content_ans, key=lambda value: value[0], reverse=False)
        title_ans = dic.intersection_title(*andterm)
        # print(content_ans)
        if len(notterm) > 0:
            for term in notterm:
                content_, title_ = dic.getlist(term)
                content_ans = util.and_not2(content_ans, content_)
                title_ans = util.and_not2(title_ans, title_)
        if content_res is None:
            content_res = content_ans
        else:
            content_res = util.or2_score(content_res, content_ans)
        if title_res is None:
            title_res = title_ans
        else:
            title_res = util.or2_score(title_res, title_ans)
        # print(content_res)
    res = util.merge_content_title(content_res, title_res)  # 对标题和内容查询到的结果进行合并
    # res = sorted(res, key=lambda value: value[1], reverse=True)
    print(str(res))


# 初始化字典函数
def init_dictionary() -> dictionary.Dic:
    poem_list = []
    for poem_id, p in util.read_data().items():
        poem_list.append(dictionary.Poem(p, poem_id))
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
    # print(dic.content_biterm_list['华夏'].posting_list)
    print(dic.bigram_mle('唐诗三百首'))
    # parser()
    # print(dic.getlist('明'))
    # print(dic.title_term_list['明'].posting_list)
    # print(dic.content_term_list['明'].posting_list)

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
