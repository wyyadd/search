# coding=utf-8
import re

from typing import List

import util
from collections import deque


class Poem:
    """
    Poem 类
    成员变量： title, author, content(内容), term_dict(词频字典)
    """

    def __init__(self, poem: str, poem_id: int):
        self.id = poem_id
        poem = poem.splitlines()
        self.title = poem[0]
        self.author = poem[1]
        self.content = re.split(r'[.。,，!！?？(（）):：;；、’“"”《》]', poem[2])
        if len(self.content[-1]) == 0:
            self.content.pop()
        self.content_term_dict = util.generate_term_dict(self.content)
        self.title_term_dict = util.generate_term_dict([self.title])


class Term:
    """
    Term 类
    成员变量: term, posting_list, frequency
    """

    def __init__(self, term, poem_id, frequency):
        self.idf = float
        self.posting_list = []
        self.term = term
        self.posting_list.append((poem_id, frequency))
        self.frequency = frequency

    # 更新posting_list和frequency
    def update(self, poem_id, frequency):
        self.frequency += frequency
        self.posting_list.append((poem_id, frequency))
        list.sort(self.posting_list, key=lambda x: x[1], reverse=True)

    # 获取term所在文档的个数
    def get_doc_num(self):
        return len(self.posting_list)

    def generate_idf(self, total: int):
        self.idf = total / self.get_doc_num()


class Dic:
    """
    Dic 类
    成员变量: doc_list(文档列表), term_list(term列表)
    """

    def __init__(self, poem_list: List[Poem]):
        self.doc_list = poem_list
        self.content_term_list, self.title_term_list = self.__generate_term_list()

    # 根据doc_list生成term_list
    def __generate_term_list(self):
        content_term_dict = {}
        title_term_dict = {}
        # 生成term_list
        for poem in self.doc_list:
            for term, fre in poem.content_term_dict.items():
                if term in content_term_dict:
                    content_term_dict[term].update(poem.id, fre)
                else:
                    content_term_dict[term] = Term(term, poem.id, fre)
            for term, fre in poem.title_term_dict.items():
                if term in title_term_dict:
                    title_term_dict[term].update(poem.id, fre)
                else:
                    title_term_dict[term] = Term(term, poem.id, fre)
        # 生成idf
        for key, value in content_term_dict.items():
            value.generate_idf(len(self.doc_list))
        for key, value in title_term_dict.items():
            value.generate_idf(len(self.doc_list))
        return content_term_dict, title_term_dict

    def getlist(self, term):
        """根据term，返回内容索引和标题索引的加权和"""
        content_list = None
        title_list = None
        if term in self.content_term_list.keys():
            content_list = self.content_term_list[term].posting_list
        if term in self.title_term_list.keys():
            title_list = self.title_term_list[term].posting_list
        return util.merge_content_title(content_list, title_list)

    """输入为N个关键词，返回为两个关键词对应链表的并集，并综合标题索引和内容索引，结果按照分数从大到小排序"""

    def union(self, *term):
        res = []
        for term_list in [self.content_term_list, self.title_term_list]:
            ans = deque()
            candidates_list = []
            for t in term:
                if t in term_list:
                    candidates_list.append(term_list[t].posting_list)
            if len(candidates_list) != 0:
                list.sort(candidates_list, key=len, reverse=True)
                ans = candidates_list[0]
                for p in candidates_list[1:]:
                    ans = util.or2(ans, p)
            res.append(ans)
        return util.merge_content_title(res[0], res[1])

    """输入为N个关键词，返回为两个关键词对应链表的交集，并综合标题索引和内容索引，结果按照分数从大到小排序"""

    def intersection(self, *term):
        res = []
        for term_list in [self.content_term_list, self.title_term_list]:
            ans = deque()
            candidates_list = []
            for t in term:
                if t not in term_list:
                    candidates_list.clear()
                    break
                else:
                    candidates_list.append(term_list[t].posting_list)
            if len(candidates_list) > 0:
                list.sort(candidates_list, key=len)
                ans = candidates_list[0]
                for p in candidates_list[1:]:
                    ans = util.and2(ans, p)
            res.append(ans)
        return util.merge_content_title(res[0], res[1])

    """输入为两个关键词，返回为两个关键词对应链表的and not，并综合标题索引和内容索引，结果按照分数从大到小排序"""

    def and_not(self, s1, s2) -> deque:
        res = []
        for term_list in [self.content_term_list, self.title_term_list]:
            ans = deque()
            if s1 in self.content_term_list.keys():
                if s2 not in self.content_term_list.keys():
                    ans = term_list[s1].posting_list
                else:
                    p1 = self.content_term_list[s1].posting_list
                    p2 = self.content_term_list[s2].posting_list
                    ans = util.and_not2(p1, p2)
            res.append(ans)
        return util.merge_content_title(res[0], res[1])

    """向量搜索"""
    def vector_search(self, *term):
        # key: docId, value: score
        scores = {}
        # key: docId, value: doc length
        length = {}
        for doc in self.doc_list:
            length[doc.id] = sum(doc.content_term_dict.values())
        for t in term:
            # s : (docId, tf)
            for s in self.content_term_list[t].posting_list[:20]:
                # wf_td = tf * idf
                if s[0] in scores:
                    scores[s[0]] += s[1] * self.content_term_list[t].idf
                else:
                    scores[s[0]] = s[1] * self.content_term_list[t].idf
        for doc_id in scores.keys():
            scores[doc_id] /= length[doc_id]
        # return top 5
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
