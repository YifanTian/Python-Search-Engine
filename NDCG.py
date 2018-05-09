import numpy as np

def dcg(relevances, rank=5):
    """Discounted cumulative gain at rank (DCG)"""
    relevances = np.asarray(relevances)[:rank]
    print(relevances)
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


# /Users/prateeksingh/Library/Preferences/PyCharmEdu4.0/scratches/scratch_6.py
rel=[2,3,1,0,0,1,1,2,3,3,3,3,3,3,3,3,3,3,3]
rel1=6,8,3,4,3,3,2
print(dcg(rel1))
print(ndcg(rel1))
