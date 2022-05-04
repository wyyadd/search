# coding=utf-8
import re
from collections import deque


class Poem:
    def __init__(self, poem: str, poem_id: int):
        self.id = poem_id
        poem = poem.splitlines()
        self.title = poem[0]
        self.author = poem[1]
        self.content = re.split(r'[.。,，!！?？(（）):：;；、’“"”]', poem[2])
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
