#from __future__ import division
import operator
from collections import Counter
import json
import math
import globals as g 
from  globals import *
from collections import defaultdict
import os
import re

from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
import string

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except:
    from urllib import urlopen, urlencode # Python 2
 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt','RT', 'via']

 

positive_vocab = [
	'good', 'nice', 'great', 'awesome', 'outstanding',
	'fantastic', 'terrific', ':)', ':-)', 'like', 'love','happy','applause','😂','🤣','😁','😄','😃','😀','☺','😊','🙂','😉','😛','😝','😜','🤪','😬','😘','😍'
	# shall we also include game-specific terms?
	# 'triumph', 'triumphal', 'triumphant', 'victory', etc.
]
negative_vocab = [
	'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(','outrageous','unjust','stfu','defeat','tragic','🤨','😒','😞','😔','😟','😕','🙁','☹','😣','😫','😩','😤','😠','😡','🤬','😨'
	# 'defeat', etc.
]


#print(stop)
emoticons_str = r"""
	(?:
		[:=;] # Eyes
		[oO\-]? # Nose (optional)
		[D\)\]\(\]/\\OpP] # Mouth
	)"""
 
regex_str = [
	emoticons_str,
	r'<[^>]+>', # HTML tags
	r'(?:@[\w_]+)', # @mentions
	r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
	r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
	r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
	r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
	r'(?:[\w_]+)', # other words
	r'(?:\S)' # anything else
]
	
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)#verbose helps in writing multiline regular expressions
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
	return tokens_re.findall(s)
 
def preprocess(s, lowercase=True):
	tokens = tokenize(s)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens

if (os.path.exists("NewApp.json")):
	os.remove('NewApp.json')

com = defaultdict(lambda : defaultdict(int))

def mainAnalysis():
	n_docs=0
	if g.uploaded is True:
		fname = g.filename
	else:
		fname = 'NewApp.json'
	#fname  = 'Liverpool.json'
	print("filename = "+fname)
	with open(fname, 'r') as f:
		count_all = Counter()
		tweetList =  []
		count_single = Counter()
		count_stop_single = Counter()
		for line in f:
			if len(str(line))==1:
				continue
			tweet = json.loads(line)
			if 'retweeted_status' in tweet:
				str1=tweet['retweeted_status']['retweet_count']
				tweetText = tweet['retweeted_status']['text']
				id1 = tweet['retweeted_status']['id']
				tweetList= tweetList+[[str1,id1,tweetText]]

			n_docs+=1
			
			# Create a list with all the terms
			terms_all = [term for term in preprocess(tweet['text']) if 'text' in tweet ]
			# Update the counter
			count_all.update(terms_all)
			# print("preprocess")
			# print(preprocess(tweet['text']))
			terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
			

			terms_single = set(terms_all)
			count_single.update(terms_all)
			# Count hashtags only
			terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
			# Count terms only (no hashtags, no mentions)
			terms_only = [term for term in preprocess(tweet['text'])   if term not in stop and not term.startswith(('#', '@'))] 
							# mind the ((double brackets))
							# startswith() takes a tuple (not a list) if 
							# we pass a list of inputs
			count_stop_single.update(terms_only)
			# print("terms only")
			# print(terms_only)
			for i in range(len(terms_only)-1):            
				for j in range(i+1, len(terms_only)):
					# print("z"+terms_only[i]+" "+terms_only[j])
					w1, w2 = sorted([terms_only[i], terms_only[j]]) 
					# print("x"+w1+" "+w2)               
					if w1 != w2:
						com[w2][w1] += 1
						com[w1][w2] += 1

		# print("com")
		# print(com)
		# print(count_stop_single.items())	
		#print("most common")
		#print(count_stop_single.most_common(20))


		tweetList.sort()



		newlist = tweetList[::-1]
		idlist= list()
		ctr=0
		for i in newlist:
			if i[1] not in idlist:
				idlist.append(i[1])

				g.toptweets.append(i[2])
				ctr+=1
			if ctr>10:
				break
		#print("--------------------------------------------------------")
		#print(toptweets)
		for text in g.toptweets:
			for x,y in pos_tag(word_tokenize(text)):
				if y=="JJ" or y=="JJR" or y=="JJS":
					# print("Which category does \""+x+"\" belong to? 1 positive 2 negative 3 none.")
					# op=int(input())
 
					# if op==1 and x not in positive_vocab:
					# 	positive_vocab.append(x)
					# elif op==2 and x not in negative_vocab:
					# 	negative_vocab.append(x)
					adjectives_list.append(x)
	
			

					
		print("----------------------------------")
		print(adjectives_list)
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
		print("most concurrent")
		print(terms_max[:5])









		pmi = defaultdict(lambda : defaultdict(int))
		for t1 in p_t:
			for t2 in com[t1]:
				denom = p_t[t1] * p_t[t2]
				if denom is not 0:
					pmi[t1][t2] = math.log((p_t_com[t1][t2] / denom),2)
		
		#print(pmi)
		for term, n in p_t.items():
			positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
			negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
			if term=='insane':
				print(pmi[term])
				print("------------------")
			# if positive_assoc == negative_assoc:
			# 	print("EQUAL")
			# 	print(term+" pos"+str(positive_assoc)+" neg "+str(negative_assoc))
			
			semantic_orientation[term] = positive_assoc - negative_assoc

		semantic_sorted = sorted(semantic_orientation.items(), 
								key=operator.itemgetter(1), 
								reverse=True)
		# print("jfj,fgkjgkjbh")
		# print(semantic_orientation)
		# print("aaaaaaaaaa")
		# print(pmi)
		# print("bbbbbbb")
		# print(com)
		if __name__ == "__main__":
			top_pos = semantic_sorted[:20]
			top_neg = semantic_sorted[-20:]

			#print(semantic_sorted)
			print("\ntop negative: ")
			print(top_neg)
			print("\nTop positive: ")
			print(top_pos)
			print("mlk50:"+str(semantic_orientation["salah"]))
			print("MARTIN:"+str(semantic_orientation["anfield"]))
			print("HAZARD: "+str(semantic_orientation["hazard"]))
			print("willian: "+str(semantic_orientation["willian"]))
			print("conte: "+str(semantic_orientation["conte"]))
			print("ed: "+str(semantic_orientation["eduardo"]))
#mainAnalysis()