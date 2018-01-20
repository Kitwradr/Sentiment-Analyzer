from __future__ import division
import operator
from collections import Counter
import json
import math

from collections import defaultdict

import re

from nltk.corpus import stopwords
import string
 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt','RT', 'via']

 

positive_vocab = [
    'good', 'nice', 'great', 'awesome', 'outstanding',
    'fantastic', 'terrific', ':)', ':-)', 'like', 'love','Happy'
    # shall we also include game-specific terms?
    # 'triumph', 'triumphal', 'triumphant', 'victory', etc.
]
negative_vocab = [
    'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(','outrageous','unjust'
    # 'defeat', etc.
]



emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
 


com = defaultdict(lambda : defaultdict(int))

n_docs=0
fname = 'python2.json'
with open(fname, 'r') as f:
    count_all = Counter()
    count_single = Counter()
    count_stop_single = Counter()
    for line in f:
        n_docs+=1
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_all = [term for term in preprocess(tweet['text'])]
        # Update the counter
        count_all.update(terms_all)
        
        terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
        count_stop_single.update(terms_stop)

        terms_single = set(terms_all)
        count_single.update(terms_all)
        # Count hashtags only
        terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text'])   if term not in stop and not term.startswith(('#', '@'))] 
                      # mind the ((double brackets))
                      # startswith() takes a tuple (not a list) if 
                      # we pass a list of inputs

        for i in range(len(terms_only)-1):            
            for j in range(i+1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])                
                if w1 != w2:
                    com[w1][w2] += 1
        # Print the first 5 most frequent words
    print(count_stop_single.most_common(5))




    # n_docs is the total n. of tweets
    p_t = {}
    p_t_com = defaultdict(lambda : defaultdict(int))
     
    for term, n in count_stop_single.items():
        p_t[term] = n / n_docs
        for t2 in com[term]:
            p_t_com[term][t2] = com[term][t2] / n_docs

    #print(p_t)
    print("\n\n")
    #print(p_t_com)


    com_max = []
# For each term, look for the most common co-occurrent terms
    for t1 in com:
        t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
        for t2, t2_count in t1_max_terms:
            com_max.append(((t1, t2), t2_count))
    # Get the most frequent co-occurrences
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    print(terms_max[:5])









    pmi = defaultdict(lambda : defaultdict(int))
    for t1 in p_t:
        for t2 in com[t1]:
            denom = p_t[t1] * p_t[t2]
            if denom is not 0:
                pmi[t1][t2] = math.log((p_t_com[t1][t2] / denom),2)
     
    semantic_orientation = {}
    for term, n in p_t.items():
        positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
        negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
        semantic_orientation[term] = positive_assoc - negative_assoc

    semantic_sorted = sorted(semantic_orientation.items(), 
                             key=operator.itemgetter(1), 
                             reverse=True)
    top_pos = semantic_sorted[:10]
    top_neg = semantic_sorted[-10:]

    #print(semantic_sorted)
    print("\ntop negative: ")
    print(top_neg)
    print("\nTop positive: ")
    print(top_pos)
    print("\nChelsea: %f" % semantic_orientation['Chelsea'])



 
