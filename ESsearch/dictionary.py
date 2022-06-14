# coding=utf-8
import re
import math
from typing import List, Dict

from ESsearch import util
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
        self.raw_content = poem[2]
        self.content = re.split(r'[.。,，!！?？(（）):：;；、’“"”《》]', self.raw_content)
        if len(self.content[-1]) == 0:
            self.content.pop()
        self.content_term_dict = util.generate_term_dict(self.content)
        self.content_biterm_dict = util.generate_biterm_dict(self.content)
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

    def __init__(self, poem_list: Dict[int, Poem]):
        self.doc_list = poem_list
        self.content_term_list, self.title_term_list, self.content_biterm_list = self.__generate_term_list()
        self.doc_info, self.total_count = self.__generate_doc_info()
        print("初始化搜索引擎完成\n")

    def __generate_doc_info(self):
        # 生成doc_info和总的字长 key为docID v为内容的长度
        doc_dict = {}
        total = 0
        for poem in self.doc_list.values():
            doc_dict[poem.id] = len(poem.content_term_dict)
            total += len(poem.content_term_dict)
        return doc_dict, total

    # 根据doc_list生成term_list
    def __generate_term_list(self):
        content_term_dict = {}
        title_term_dict = {}
        content_biterm_dict = {}
        # 生成term_list
        for poem in self.doc_list.values():
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
            for term, fre in poem.content_biterm_dict.items():
                if term in content_biterm_dict:
                    content_biterm_dict[term].update(poem.id, fre)
                else:
                    content_biterm_dict[term] = Term(term, poem.id, fre)
        # 生成idf
        for key, value in content_term_dict.items():
            value.generate_idf(len(self.doc_list))
        for key, value in title_term_dict.items():
            value.generate_idf(len(self.doc_list))
        return content_term_dict, title_term_dict, content_biterm_dict

    def getlist(self, term):
        """根据term，返回内容索引和标题索引,均按docid排序"""
        content_list = None
        title_list = None
        if term in self.content_term_list.keys():
            content_list = self.content_term_list[term].posting_list
        if term in self.title_term_list.keys():
            title_list = self.title_term_list[term].posting_list
        if content_list is not None:
            content_list = sorted(content_list, key=lambda value: value[0], reverse=False)
        return content_list, title_list

    def union(self, *term):
        """输入为N个关键词，返回为两个关键词对应链表的并集，并综合标题索引和内容索引，结果 按照分数从大到小排序"""
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

    def intersection(self, *term):
        """输入为N个关键词，返回为两个关键词对应链表的交集，并综合标题索引和内容索引，结果按照分数从大到小排序"""
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

    def and_not(self, s1, s2) -> deque:
        """输入为两个关键词，返回为两个关键词对应链表的and not，并综合标题索引和内容索引，结果按照分数从大到小排序"""
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

    def union_title(self, *term):
        """仅针对标题索引的bool查询"""
        ans = []
        candidates_list = []
        for t in term:
            if t in self.title_term_list:
                candidates_list.append(self.content_term_list[t].posting_list)
        if len(candidates_list) != 0:
            list.sort(candidates_list, key=len, reverse=True)
            ans = candidates_list[0]
            for p in candidates_list[1:]:
                ans = util.or2(ans, p)
        return ans

    def intersection_title(self, *term):
        ans = []
        candidates_list = []
        for t in term:
            if t not in self.title_term_list:
                candidates_list.clear()
                break
            else:
                candidates_list.append(self.title_term_list[t].posting_list)
        if len(candidates_list) > 0:
            list.sort(candidates_list, key=len)
            ans = candidates_list[0]
            for p in candidates_list[1:]:
                ans = util.and2(ans, p)
        return ans

    def vector_search(self, *term):
        """向量搜索"""
        term = list(term)
        for t in term[:]:
            if t not in self.content_term_list.keys():
                term.remove(t)
        # 按照idf大小降序排序
        list.sort(term, key=lambda x: self.content_term_list[x].idf, reverse=True)
        # key: docId, value: score
        scores = {}
        # key: docId, value: doc length
        length = {}
        for doc in self.doc_list.values():
            length[doc.id] = sum(doc.content_term_dict.values())
        for t in term:
            # s : (docId, tf)
            idf = self.content_term_list[t].idf
            for s in self.content_term_list[t].posting_list[:20]:
                # wf_td = tf * idf
                if s[0] in scores:
                    scores[s[0]] += s[1] * idf
                else:
                    scores[s[0]] = s[1] * idf
        for doc_id in scores.keys():
            scores[doc_id] /= length[doc_id]
        # return top 5
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

    def rsv(self, term, start):
        # key: docId, value: score
        scores = {}
        for t in term:
            idf = float(self.content_term_list[t].idf)
            ut = 1 / idf
            pt = 1 / 3 + (2 / 3) * (1 / idf)
            ct = math.log2(pt / (1 - pt)) + math.log2((1 - ut) / ut)
            # s : (docId, tf)
            for s in self.content_term_list[t].posting_list:
                if s[0] in scores:
                    scores[s[0]] += ct
                else:
                    scores[s[0]] = ct
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[start:start+10]

    def unigram_mle(self, term, start):
        res = {}
        lamda = 0.5
        for t in term:
            if t not in self.content_term_list.keys():
                continue
            for docid, _ in self.content_term_list[t].posting_list:
                res[docid] = 1
        for t in term:
            if t not in self.content_term_list.keys():
                continue
            total = self.content_term_list[t].frequency
            temp_dic = {}
            for did, freq in self.content_term_list[t].posting_list:
                temp_dic[did] = freq
            for docid, _ in res.items():
                if docid in temp_dic.keys():
                    res[docid] *= (
                            lamda * temp_dic[docid] / self.doc_info[docid] + (1 - lamda) * total / self.total_count)
                else:
                    res[docid] *= (1 - lamda) * total / self.total_count
        return sorted(res.items(), key=lambda x: x[1], reverse=True)[start:start+10]

    def bigram_mle(self, term, start):
        res = {}
        lamda = 0.5
        first = term[0]
        # print(term)
        for t in term:
            if t not in self.content_term_list.keys():
                continue
            for docid, _ in self.content_term_list[t].posting_list:
                res[docid] = 1
        for t in term[1:]:
            word = first + t
            if first not in self.content_term_list.keys():
                first = t
                continue

            total = 0 if first not in self.content_term_list.keys() else self.content_term_list[first].frequency
            bi_total = 0 if word not in self.content_biterm_list.keys() else self.content_biterm_list[word].frequency
            uni_dic = {}
            bi_dic = {}
            for did, freq in self.content_term_list[first].posting_list:
                uni_dic[did] = freq
            if word in self.content_biterm_list.keys():
                for did, freq in self.content_biterm_list[word].posting_list:  # 有问题
                    bi_dic[did] = freq
            for docid in res.keys():
                uni = (1 - lamda) * total / self.total_count
                bi = (1 - lamda) * bi_total / self.total_count
                if docid in uni_dic.keys():
                    uni += lamda * uni_dic[docid] / self.doc_info[docid]
                if docid in bi_dic.keys():
                    bi += lamda * bi_dic[docid] / self.doc_info[docid]
                res[docid] *= 0.4 * uni + 0.6 * bi
            first = t
            # print(sorted(res.items(), key=lambda x: x[1], reverse=True)[:5])
        return sorted(res.items(), key=lambda x: x[1], reverse=True)[start:start+10]
