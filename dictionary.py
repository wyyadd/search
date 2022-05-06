# coding=utf-8
import re
import util
from collections import deque


class Poem:
    def __init__(self, poem: str, poem_id: int):
        self.id = poem_id
        poem = poem.splitlines()
        self.title = poem[0]
        self.author = poem[1]
        self.content = re.split(r'[.。,，!！?？(（）):：;；、’“"”《》]', poem[2])
        if len(self.content[-1]) == 0:
            self.content.pop()
        self.term_dict = self.__generate_term_dict()

    def __generate_term_dict(self):
        term_dict = {}
        for sentence in self.content:
            for c in sentence:
                if c in term_dict:
                    term_dict[c] += 1
                else:
                    term_dict[c] = 1
        return term_dict


class Term:
    def __init__(self, term, poem_id, frequency):
        self.posting_list = deque()
        self.term = term
        self.posting_list.append((poem_id, frequency))
        self.frequency = frequency

    def update(self, poem_id, frequency):
        self.frequency += frequency
        self.posting_list.append((poem_id, frequency))

    def get_doc_num(self):
        return len(self.posting_list)


class Dic:
    def __init__(self, poem_list: list):
        self.doc_list = poem_list
        self.term_list = self.__generate_term_dict()

    def __generate_term_dict(self):
        term_dict = {}
        for poem in self.doc_list:
            for term, fre in poem.term_dict.items():
                if term in term_dict:
                    term_dict[term].update(poem.id, fre)
                else:
                    term_dict[term] = Term(term, poem.id, fre)
        return term_dict

    """输入为N个关键词，返回为两个关键词对应链表的并集"""
    def union(self, *term) -> deque:
        ans = deque()
        candidates_list = []
        for t in term:
            if t in self.term_list:
                candidates_list.append(self.term_list[t].posting_list)
        if len(candidates_list) == 0:
            return ans
        list.sort(candidates_list, key=len, reverse=True)
        ans = candidates_list[0]
        for p in candidates_list[1:]:
            ans = util.or2(ans, p)
        return ans

    """输入为N个关键词，返回为两个关键词对应链表的交集"""
    def intersection(self, *term) -> deque:
        ans = deque()
        candidates_list = []
        for t in term:
            if t not in self.term_list:
                return ans
            else:
                candidates_list.append(self.term_list[t].posting_list)
        list.sort(candidates_list, key=len)
        ans = candidates_list[0]
        for p in candidates_list[1:]:
            ans = util.and2(ans, p)
        return ans

    """输入为两个关键词，返回为两个关键词对应链表的and not"""
    def and_not(self, s1, s2) -> deque:
        if s1 not in self.term_list.keys():
            return deque()
        if s2 not in self.term_list.keys():
            return self.term_list[s1].posting_list
        p1 = self.term_list[s1].posting_list
        p2 = self.term_list[s2].posting_list
        return util.and_not2(p1, p2)

    # def union(self, s1, s2) -> deque:
    #     """输入为两个关键词，返回为两个关键词对应链表的并集"""
    #     if s1 not in self.term_list.keys() and s2 not in self.term_list.keys():
    #         return None
    #     if s1 not in self.term_list.keys():
    #         return self.term_list[s2].posting_list
    #     if s2 not in self.term_list.keys():
    #         return self.term_list[s1].posting_list
    #     p1 = self.term_list[s1].posting_list
    #     p2 = self.term_list[s2].posting_list
    #     return or2(p1, p2)
    #
    # def intersection(self, s1, s2) -> deque:
    #     """输入为两个关键词，返回为两个关键词对应链表的交集"""
    #     if s1 not in self.term_list.keys() or s2 not in self.term_list.keys():
    #         return None
    #     p1 = self.term_list[s1].posting_list
    #     p2 = self.term_list[s2].posting_list
    #     return and2(p1, p2)
    # def andmany(self, termlist) -> deque:
    #     """输入为关键词的列表，返回为多个关键词的交集"""
    #     for term in termlist:
    #         if term not in self.term_list.keys():
    #             return None
    #     if len(termlist) == 0:
    #         return None
    #     elif len(termlist) == 1:
    #         return self.term_list[termlist[0]].posting_list
    #     elif len(termlist) == 2:
    #         return self.intersection(termlist[0], termlist[1])
    #     else:
    #         p1 = self.term_list[termlist[0]].posting_list
    #         p2 = self.term_list[termlist[1]].posting_list
    #         p1 = and2(p1, p2)
    #         for i in range(2, len(termlist)):
    #             p2 = self.term_list[termlist[i]].posting_list
    #             p1 = and2(p1, p2)
    #         return p1
    #
    # def ormany(self, termlist) -> deque:
    #     """输入为关键词的列表，返回为多个关键词的并集"""
    #     termlist = [term for term in termlist if term in self.term_list.keys()]
    #     if len(termlist) == 0:
    #         return None
    #     elif len(termlist) == 1:
    #         return self.term_list[termlist[0]].posting_list
    #     elif len(termlist) == 2:
    #         return self.union(termlist[0], termlist[1])
    #     else:
    #         p1 = self.term_list[termlist[0]].posting_list
    #         p2 = self.term_list[termlist[1]].posting_list
    #         p1 = or2(p1, p2)
    #         for i in range(2, len(termlist)):
    #             p2 = self.term_list[termlist[i]].posting_list
    #             p1 = or2(p1, p2)
    #         return p1
