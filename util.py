# coding=utf-8
import os
from collections import deque


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
    res = deque()
    i = 0
    j = 0
    while i < len(p1) and j < len(p2):
        if p1[i] < p2[j]:
            i += 1
        elif p1[i] > p2[j]:
            j += 1
        else:
            res.append((p1[i][0], p1[i][1] + p2[j][1]))
            i += 1
            j += 1
    return res


def or2(p1, p2):
    """针对两个链表的or"""
    res = deque()
    i = 0
    j = 0
    while i < len(p1) and j < len(p2):
        if p1[i] < p2[j]:
            res.append(p1[i])
            i += 1
        elif p1[i] > p2[j]:
            res.append(p2[j])
            j += 1
        else:
            res.append((p1[i][0], p1[i][1] + p2[j][1]))
            i += 1
            j += 1
    if i == len(p1):
        for m in range(j, len(p2)):
            res.append(p2[j])
    else:
        for m in range(i, len(p1)):
            res.append(p1[i])
    return res


def and_not2(p1, p2):
    """针对两个链表的and-not"""
    res = deque()
    i = 0
    j = 0
    while i < len(p1) and j < len(p2):
        if p1[i] < p2[j]:
            res.append(p1[i])
            i += 1
        elif p1[i] > p2[j]:
            j += 1
        else:
            i += 1
            j += 1
    return res
