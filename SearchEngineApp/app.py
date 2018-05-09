
import os
import sys
import json

from flask import Flask
from flask import request
from flask import render_template

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('search_panel.html',query = None,Google_results_html=None, Search_results=None)


@app.route('/query/', methods=['GET'])
def query():
    # query=request.form['query']
    query = request.args.get("query")
    # Google_results_html = ['https://www.google.com','https://www.baidu.com']
    Google_results_html = google_search(query)
    # Search_results = ['https://www.baidu.com','https://www.baidu.com','https://www.baidu.com','https://www.baidu.com','https://www.baidu.com']
    Search_results = search_engine(query)
    return render_template('search_panel.html', query=query, Google_results_html = Google_results_html, Search_results=Search_results)


def google_search(query):
    ground_truth_json = 'google_results_latest.json'
    with open(ground_truth_json) as index_json:               # read index json
        ground_truth_dict = json.load(index_json)
    if query in ground_truth_dict:
        ground_truth_list = [key for key,val in sorted(ground_truth_dict[query].items(), key=lambda x : x[1])]
        return ground_truth_list[:5]
    else:
        print("Not in google_search json")
        return ['https://www.google.com' for _ in range(5)]

def search_engine(query):
    our_search_results_json = 'search_results_latest.json'
    with open(our_search_results_json) as index_json:               # read index json
        our_search_results_dict = json.load(index_json)
    if query in our_search_results_dict:
        res = ['https://' + result for result in our_search_results_dict[query][:5]]
        return res
    else:
        print("Not in search_engine json")
        return ['https://www.google.com' for _ in range(5)]