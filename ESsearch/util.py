# coding=utf-8
import os
# import jieba


# 从dataset文件夹中读取诗句
def read_data() -> dict:
    poem_str = {}
    for s in sorted(os.listdir("./ESsearch/dataset")):
        with open("./ESsearch/dataset/" + s, 'r', encoding='utf8') as file:
            poem_str[int(s.split('-')[0])] = (file.read())
    return poem_str


# 生成词频字典
def generate_term_dict(text: list):
    term_dict = {}
    for sentence in text:
        # for c in jieba.cut_for_search(sentence):
        for c in sentence:
            if c in term_dict:
                term_dict[c] += 1
            else:
                term_dict[c] = 1
    return term_dict


def generate_biterm_dict(text: list):
    term_dict = {}
    for sentence in text:
        # for c in jieba.cut_for_search(sentence):
        if len(sentence) == 0:
            continue
        first = sentence[0]
        for c in sentence[1:]:
            word = first + c
            first = c
            if word in term_dict:
                term_dict[word] += 1
            else:
                term_dict[word] = 1
    return term_dict


def and2(p1, p2):
    """针对两个链表的and"""
    res = []
    i = 0
    j = 0
    while i < len(p1) and j < len(p2):
        if p1[i][0] < p2[j][0]:
            i += 1
        elif p1[i][0] > p2[j][0]:
            j += 1
        else:
            res.append((p1[i][0], p1[i][1] + p2[j][1]))
            i += 1
            j += 1
    return res


def or2_score(p1, p2):
    """带分数的链表的合并"""
    res = []
    i = 0
    j = 0
    while i < len(p1) and j < len(p2):
        if p1[i][0] < p2[j][0]:
            res.append(p1[i])
            i += 1
        elif p1[i][0] > p2[j][0]:
            res.append(p2[j])
            j += 1
        else:
            res.append((p1[i][0], min(p1[i][1] + p2[j][1], 1)))
            i += 1
            j += 1
    if i == len(p1):
        for m in range(j, len(p2)):
            res.append(p2[m])
    else:
        for m in range(i, len(p1)):
            res.append(p1[m])
    return res


def or2(p1, p2):
    """针对两个链表的or"""
    res = []
    i = 0
    j = 0
    while i < len(p1) and j < len(p2):
        if p1[i][0] < p2[j][0]:
            res.append(p1[i])
            i += 1
        elif p1[i][0] > p2[j][0]:
            res.append(p2[j])
            j += 1
        else:
            res.append((p1[i][0], p1[i][1] + p2[j][1]))
            i += 1
            j += 1
    if i == len(p1):
        for m in range(j, len(p2)):
            res.append(p2[m])
    else:
        for m in range(i, len(p1)):
            res.append(p1[m])
    return res


def and_not2(p1, p2):
    """针对两个链表的and-not"""
    if p2 is None:
        return p1
    res = []
    i = 0
    j = 0
    while i < len(p1) and j < len(p2):
        if p1[i][0] < p2[j][0]:
            res.append(p1[i])
            i += 1
        elif p1[i][0] > p2[j][0]:
            j += 1
        else:
            i += 1
            j += 1
    return res


def merge_content_title(content_list, title_list):
    """合并内容列表和标题列表，按照0.4：0.6的权重，并将结果分数按从大到小排序"""
    res = []
    i = 0
    j = 0
    if content_list is None and title_list is None:
        return None
    elif content_list is None:
        for i in range(len(title_list)):
            res.append((title_list[i][0], 0.6))
    elif title_list is None:
        for i in range(len(content_list)):
            res.append((content_list[i][0], 0.4 * content_list[i][1]))
    else:
        while i < len(content_list) and j < len(title_list):
            if content_list[i][0] < title_list[j][0]:
                res.append((content_list[i][0], 0.4 * content_list[i][1]))
                i += 1
            elif content_list[i][0] > title_list[j][0]:
                res.append((title_list[j][0], 0.6))
                j += 1
            else:
                res.append((title_list[j][0], 0.6 + 0.4 * content_list[i][1]))
                i += 1
                j += 1
        if i == len(content_list):
            for m in range(j, len(title_list)):
                res.append((title_list[m][0], 0.6))
        else:
            for m in range(i, len(content_list)):
                res.append((content_list[m][0], 0.4 * content_list[m][1]))
    return sorted(res, key=lambda value: value[1], reverse=True)[:5]  # 按照结果分数从大到小排序
    # return res  # 按照docid排序，最后统一按分数排序
