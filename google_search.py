from google import google
import json

def test():
    query_list = ['Crista Lopes','mondego','machine learning','software engineering','security',\
        'student affairs','graduate courses','REST','computer games','information retrieval']

    num_page = 2
    for query in query_list:
        search_results = google.search(query + " site:ics.uci.edu", num_page)
        for doc in search_results[0:5]:
            print(doc.link)
        print()
            # print(search_results[0:5])

def google_search_query(query):
    num_page = 1
    search_results = google.search(query + " site:ics.uci.edu", num_page)
    return search_results[0:5]

def google_search_query_pages(query, num_pages):
    # num_pages = 3
    search_results_pages = google.search(query + " site:ics.uci.edu", num_pages)
    return search_results_pages

def google_search_query_dict(query):
    res = google_search_query_pages(query,20)
    link_list = []
    for i,doc in enumerate(res,1):
        if ('.pdf' in doc.link) or ('.PDF' in doc.link) or ('.ppt' in doc.link) or ('.pptx' in doc.link):
            continue 
        link_list.append((doc.link,i))
    res_dict = dict(link_list) 
    return res_dict

def save_query_res_to_json(query_list):
    query_dict = dict()
    for query in query_list:
        # res = google_search_query_pages(query,10)
        # link_list = []
        # for i,doc in enumerate(res,1):
        #     link_list.append((doc.link,i))
        # res_dict = dict(link_list)
        res_dict = google_search_query_dict(query)
        query_dict[query] = res_dict
    with open('google_results.json', 'w') as outfile:
        json.dump(query_dict, outfile)

if __name__ == '__main__':
    query_list = ['Crista Lopes','mondego','machine learning','software engineering','security',\
        'student affairs','graduate courses','REST','computer games','information retrieval']
    
    save_query_res_to_json(query_list)

    # res = google_search_query_pages('REST',10)
    # print(len(res))
    # for doc in res:
    #     print(doc.link)
