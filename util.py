# coding=utf-8
import os


# 从dataset文件夹中读取诗句
def read_data() -> list:
    poem_str = []
    for s in os.listdir("./dataset"):
        with open("./dataset/" + s, 'r', encoding='utf8') as file:
            poem_str.append(file.read())
    return poem_str


# 生成词频字典
def generate_term_dict(text: list):
    term_dict = {}
    for sentence in text:
        for c in sentence:
            if c in term_dict:
                term_dict[c] += 1
            else:
                term_dict[c] = 1
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
    res = deque()
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
            res.append((content_list[i][0], 0.4))
    else:
        while i < len(content_list) and j < len(title_list):
            if content_list[i][0] < title_list[j][0]:
                res.append((content_list[i][0], 0.4))
                i += 1
            elif content_list[i][0] > title_list[j][0]:
                res.append((title_list[j][0], 0.6))
                j += 1
            else:
                res.append((title_list[j][0], 1))
                i += 1
                j += 1
        if i == len(content_list):
            for m in range(j, len(title_list)):
                res.append((title_list[m][0], 0.6))
        else:
            for m in range(i, len(content_list)):
                res.append((content_list[m][0], 0.4))
    # return sorted(res, key=lambda value: value[1], reverse=True)  # 按照结果分数从大到小排序
    return res  # 按照docid排序，最后统一按分数排序
