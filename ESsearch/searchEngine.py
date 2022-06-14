# coding=utf-8
from typing import List

from ESsearch import util
from ESsearch import dictionary


# 初始化字典函数
def init_dictionary() -> dictionary.Dic:
    poem_list = {}
    for poem_id, p in util.read_data().items():
        poem_list[poem_id] = dictionary.Poem(p, poem_id)
    return dictionary.Dic(poem_list)


def parser(dic, keys):
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
    return util.merge_content_title(content_res, title_res)  # 对标题和内容查询到的结果进行合并
    # res = sorted(res, key=lambda value: value[1], reverse=True)
    # print(str(res))


def search(query, dic, search_type) -> List[dictionary.Poem]:
    poem_list = []
    if search_type == "一元MLE检索":
        ans = dic.unigram_mle([char for char in query])
    elif search_type == "二元MLE检索":
        ans = dic.bigram_mle([char for char in query])
    else:
        ans = parser(dic, query)
    for doc in ans:
        poem_list.append(dic.doc_list[doc[0]])
    return poem_list

