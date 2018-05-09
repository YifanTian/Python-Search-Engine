import json
import argparse
import numpy as np
import os
import time
from google import google
import google_search

def compare(url, gurl):
    if (url in gurl or gurl in url) and abs(len(url) - len(gurl)) < 2:
        return True
    return False

def dcg(relevances, rank=5):
    """Discounted cumulative gain at rank (DCG)"""
    relevances = np.asarray(relevances)[:rank]
    n_relevances = len(relevances)
    if n_relevances == 0:
        return 0

    discounts = np.log2(np.arange(n_relevances) + 2)
    return np.sum(relevances / discounts)

def ndcg(relevances, rank=10):
    """Normalized discounted cumulative gain (NDGC)"""
    best_dcg = dcg(sorted(relevances, reverse=True),rank)
    if best_dcg == 0:
        return 0

    return dcg(relevances, rank) / best_dcg

        
class SearchEngine:
    def __init__(self, index_file, bookkeeper, ground_truth_file, output_file, tfidf = 1.0, bigram = 1.0, rank = 10):
        self.bookkeeper = bookkeeper
        self.index_file = index_file
        self.index_dict = dict()
        self.ground_truth = dict()
        self.ground_truth_file = ground_truth_file
        self.read_json()
        print('finish read json')
        self.tfidf = tfidf
        self.bigram = bigram
        self.rank = rank
        self.url_results = []
        self.results = []
        self.relevance_list = []
        self.output_file = output_file
        self.ndcg = 0

    def read_json(self):
        with open(self.bookkeeper) as json_data:                # read bookkeeper
            self.bookkeeper_dict = json.load(json_data)
        with open(self.index_file) as index_json:               # read index json
            self.index_dict = json.load(index_json)
        with open(self.ground_truth_file) as index_json:               # read index json
            self.ground_truth = json.load(index_json)

    def search(self, query):
        token_list = query.split()
        for i in range(len(token_list)):
            if token_list[i].istitle():
                token_list[i] = token_list[i].lower()
        doc_set = set()
        for token in token_list:                            # get docs for any token
            for doc_key in self.index_dict[token]["docs"]:
                doc_set.add(doc_key)
        res = []
        for doc in doc_set:                                # scoring each doc that contain that query            
            score = 0
            complete = True
            for token in token_list:
                if doc in self.index_dict[token]["docs"]:
                    # len(self.index_dict[token][doc]): tf, len(self.index_dict[token]): df
                    # score += (1 + np.log10(len(self.index_dict[token][doc])))*(1/len(self.index_dict[token]))
                    score += self.tfidf*(1 + np.log10(self.index_dict[token]["docs"][doc]["tf"]))*self.index_dict[token]["idf"]
                else:
                    complete = False
            if complete and len(token_list) > 1:
                adj_list = self.doc_adj_score(doc, token_list)
                # print(adj_list)
                score += self.bigram*len(adj_list)
            res.append((doc, score))
        res.sort(key=lambda tup: -tup[1]) 
        url_list = []
        for item in res:
            url_list.append(self.bookkeeper_dict[item[0]])
        rank = 10
        self.url_list = url_list
        self.results = url_list[:rank]
        self.relevance_list = self.rank_relevance(query, url_list, rank)
        # print(res[:10])
        print(url_list[:rank])
        # print(len(relevance_list))
        print(self.relevance_list)
        self.ndcg = ndcg(self.relevance_list, rank)
        # self.write_output(query)
        return url_list[:rank], ndcg(self.relevance_list, rank)

    def google_search(self, query, num_pages):
        google_complete_results = google.search(query + " site:ics.uci.edu", num_pages)
        google_results_links = [doc.link for doc in google_complete_results]
        return google_results_links

    def relevance_score(self, pos):
        if pos <= 20:
            rscore = 3
        elif pos <= 50:
            rscore = 2
        else:
            rscore = 1
        return rscore
            
    def rank_relevance(self, query, url_list, rank = 10):
        ground_truth_dict = dict()
        if query in self.ground_truth:
            ground_truth_dict = self.ground_truth[query]
        else:
            ground_truth_dict = google_search.google_search_query_dict(query)
        relevance_list = []
        for url in url_list[:rank]:
            for gurl in ground_truth_dict:
                if compare("http://"+url, gurl) or compare("https://"+url, gurl):
                    relevance_list.append(self.relevance_score(ground_truth_dict[gurl]))
                    break
            else:
                relevance_list.append(0)
        return relevance_list
        
    def doc_adj_score(self, doc, token_list):
        pos_list = []
        for token in token_list:
            pos_list.append(self.index_dict[token]["docs"][doc]["pos"])
        res = []
        for pos in pos_list[0]:
            Add = True
            for i in range(len(token_list[1:])):
                if pos+i+1 not in set(pos_list[i+1]):
                    Add = False
            if Add:
               res.append([pos+i for i in range(len(pos_list))]) 
        score = len(res)
        return res

    def write_output(self, query):
        with open(self.output_file+query+'.txt','w') as output:
            output.write(self.results)
            output.write('\n')
            output.write(self.relevance_list)
            output.write('\n')
            output.write(self.ndcg)
            output.write('\n')

        

        

def main(args):
    print(args)
    # paper_dir_list = file_util.get_dir_list(args.input)
    # engine = SearchEngine('data.json', bookkeeper_path)
    # engine.search('information retrieval')

def make_report(engine,output,query_list):
    with open(output,'w') as f:
        for query in query_list:
            start_time = time.time()
            res = engine.search(query)
            f.write('Query: '+query+'\n')
            f.write('First 5 urls: '+'\n')
            f.write(str(res[:5])+'\n')
            print(res)
            end_time = time.time()
            f.write('\n')


if __name__ == '__main__':
    # path = '../WEBPAGES_CLEAN/'
    # bookkeeper_path = "/Users/yifantian/Desktop/Course/CS221/project3/SearchEngine/bookkeeping_single.json"
    # bookkeeper_path = "/Users/yifantian/Desktop/Course/CS221/project3/SearchEngine/bookkeeping_part.json"
    index_file = 'index_dict.json'
    bookkeeper_path = "/Users/yifantian/Desktop/Course/CS221/project3/SearchEngine/bookkeeping.json"
    ground_truth_file = 'google_results_latest.json'

    tfidf = 1.0
    bigram = 1.0
    output_file = 'results'
    rank = 10

    engine = SearchEngine(index_file, bookkeeper_path, ground_truth_file, output_file, tfidf, bigram, rank)

    query_list = ['Crista Lopes','mondego','machine learning','software engineering','security',\
    'student affairs','graduate courses','REST','computer games','information retrieval']

    res_dict = dict()
    for query in query_list:
        res_dict[query] = engine.search(query)[0]

    with open('search_results_latest.json', 'w') as outfile:
        json.dump(res_dict, outfile)

    # query = 'Crista Lopes'
    # res, ndcg_score = engine.search(query)
    # print(res, ndcg_score)

    # make_report(engine, 'report.txt', query_list)


