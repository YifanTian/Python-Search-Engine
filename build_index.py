import random
import string
import uuid
from random import randint
import time
import math
import json
from collections import defaultdict
import os
import sys
import numpy as np
import re


# PartA Word Frequencies
def tokenize(doc):
    """ return list of tokens of the file   O(N)
    Function Tokenize: Here I use a regular expression template to find matching word in text. 
    As the regular expression is a sliding window. So the Time complexity of Tokenize is O(N)
    """
    # doc = file.read()
    # token_pattern=r"(?u)\b\w\w+\b"
    token_pattern=r"(?u)\b\w[a-zA-Z]+\b"                # only word, not number
    token_pattern = re.compile(token_pattern)
    # tokenize = lambda doc: token_pattern.findall(doc.lower()
    tokenize = lambda doc: token_pattern.findall(doc)
    words = tokenize(doc)     
    for i in range(len(words)):
        if words[i].istitle():
            words[i] = words[i].lower()
    return words

class Index:
    def __init__(self, path, bookkeeper):
        self.path = path
        self.bookkeeper_json = bookkeeper
        self.bookkeeper_dict = dict()
        self.file_list = []
        with open(self.bookkeeper_json) as json_data:
            self.bookkeeper_dict = json.load(json_data)
        self.length = len(self.bookkeeper_dict)
        self.inverted_index = dict()
        self.inverted_index_dict = dict()
        self.output_path = 'index.json'

    def build_index(self):
        # print(self.length)
        print('Docs: ',len(self.bookkeeper_dict))
        for file_key in self.bookkeeper_dict:               # file key: X/XXX
            file_path = self.path + file_key                # path of file
            with open(file_path) as file_data:
                index_file = self.parse_count(file_data.read(),file_key)           
                self.file_list.append(index_file)                    
        self.merge_sort(self.file_list)
        return

    def parse_count(self, content, file_key):
        # read content of file, return a index dict of one file
        token_list = tokenize(content)
        token_dict = dict()
        for pos,token in enumerate(token_list):
            if token in token_dict:
                token_dict[token][1].append(pos)                # token: (X/XXX,[1,5,8]) list of position
            else:
                token_dict[token] = file_key,[pos]
        token_dict = sorted(token_dict.items(), key=lambda x: x[1], reverse=False)
        return token_dict

    def merge_sort(self, index_list, ):
        for index_file in index_list:
            for token_list in index_file:
                if token_list[0] in self.inverted_index:
                    self.inverted_index[token_list[0]].append(token_list[1])
                else:
                    self.inverted_index[token_list[0]] = [token_list[1]]        # key: token, value: list of pos

        # with open('index_list.json', 'w') as outfile:
        #     json.dump(self.inverted_index, outfile)
        N = len(self.inverted_index)
        print('N: ',N)
        for item in self.inverted_index.items():            #
            # print(item[0])
            index_dict = dict()
            index_dict['idf'] = np.log10(N/len(item[1]))
            index_dict['docs'] = dict()
            for doc in item[1]:   
                doc_info = dict()   
                doc_info['pos'] = doc[1]   
                doc_info['tf'] = len(doc[1])
                index_dict['docs'][doc[0]] = doc_info                 # doc[0]: doc key, doc[1]: list of pos
            self.inverted_index_dict[item[0]] = index_dict  # item[0]: token
        with open('index_dict_part.json', 'w') as outfile:
            json.dump(self.inverted_index_dict, outfile)
        return 


if __name__ == '__main__':
    print("start building index")
    path = '../WEBPAGES_CLEAN/'
    # bookkeeper_path = "/Users/yifantian/Desktop/Course/CS221/project3/SearchEngine/bookkeeping_single.json"
    bookkeeper_path = "/Users/yifantian/Desktop/Course/CS221/project3/SearchEngine/bookkeeping_part.json"
    # bookkeeper_path = "/Users/yifantian/Desktop/Course/CS221/project3/SearchEngine/bookkeeping.json"
    new_index = Index(path, bookkeeper_path)
    new_index.build_index()
