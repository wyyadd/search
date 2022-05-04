# coding=utf-8
import os


def read_data() -> list:
    poem_str = []
    for s in os.listdir("./dataset"):
        with open("./dataset/" + s, 'r') as file:
            poem_str.append(file.read())
    return poem_str
