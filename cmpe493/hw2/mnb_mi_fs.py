#!/usr/bin/python3
# -*- coding: utf-8 -*-

import utils
from collections import namedtuple
from pprocs import Article
from math import log, log2
from  collections import  Counter

# named tuple used in data_collection see pprocs's parse method
c_t = utils.c_t


def classify(article, training_set, set_of_k_tokens_s, token_volume, tot_num_articles):
	"""
	Classifies one article
	:param article: the article to classify
	:param training_set: the training set
	:param set_of_k_tokens_s: the union of k words from all topics
	:param token_volume: the number of alll unique tokens in the training set
	:param tot_num_articles: total number of articles in the training set
	:return: a list of tuples sorted by similarity to the article, tuple form is:(<likelyhood_probability>, <topicname>)
	"""
	likelihoods = []
	for category in training_set:
		p_cat = len(training_set[category].cat_tok_counter) / tot_num_articles
		prob = log(p_cat)  # for explicity
		for token in article.token_counter:
			if token not in set_of_k_tokens_s: continue
			prob_w_of_c = (training_set[category].cat_tok_counter[token] + 1) / (
			sum(training_set[category].cat_tok_counter.values()) + token_volume)
			prob += log(prob_w_of_c)
		likelihoods.append((prob, category))
	return sorted(likelihoods, key=lambda x: x[0], reverse=True)

def calc_mut_info(token,topic,training_set):
	"""
	Calculates mutual inf. value between given topic and token
	:param token: the token (word)
	:param topic: the topic
	:param training_set: the training set
	:return: mutual inf. value
	"""
	unq_all = sum(training_set[tpc].unqToken_artcl_counter[token] for tpc in training_set)
	num_of_articles = sum(len(training_set[tpc].article_list) for tpc in training_set)
	
	N = num_of_articles
	N1_ = unq_all                                           # +token for all
	N0_ = num_of_articles - unq_all                         # -token for all
	N11 = training_set[topic].unqToken_artcl_counter[token] # +token : +topic
	N10 = N1_ - N11                                         # +token : -topic
	N01 = len(training_set[topic].article_list) - N11       # -token : +topic
	N00 = N0_ - N01                                         # -token : -topic
	N_1 = N11 + N01
	N_0 = N10 + N00
	
	
	
	mi = ((N11+1)/N)*log2((N*N11+1)/N1_/N_1) \
        + ((N01+1)/N)*log2((N*N01+1)/N0_/N_1) \
        + ((N10+1)/N) * log2((N * N10 +1)/ N1_ / N_0) \
        + ((N00+1)/N)*log2((N*N00+1)/N0_/N_0)
	
	return mi


if __name__ == '__main__':
	
	data_collection = utils.unpickle('data_collection')
	
	test_set = data_collection['test']  # actually a `dict` not a `set`
	training_set = data_collection['train']  # actually a `dict` not a `set`
	
	num_of_articles = sum(len(training_set[tpc].article_list) for tpc in training_set)
	
	# some all tokens from all categories
	Vocablory = training_set['earn'].cat_tok_counter \
	            + training_set['acq'].cat_tok_counter \
	            + training_set['money-fx'].cat_tok_counter \
	            + training_set['grain'].cat_tok_counter \
	            + training_set['crude'].cat_tok_counter
	
	k_tokens_s_temp  = {
		'earn':     Counter(),
		'acq':      Counter(),
		'money-fx': Counter(),
		'grain':    Counter(),
		'crude':    Counter()
	}
	
	k_tokens_set = set()
	
	for tpc in training_set:
		for tkn in Vocablory:
			k_tokens_s_temp[tpc][tkn] = calc_mut_info(tkn,tpc,training_set)
	
	for tpc in training_set:
		s = set((tpl[0] for tpl in k_tokens_s_temp[tpc].most_common(50)))
		k_tokens_set = k_tokens_set.union(s)
		print(tpc, s)
	
	
	
	# test classification and evaluate results starts here
	
	#this will hold the table with 4 statistics, `the truth values X what the classifier predicts`
	# [0] clsfr yes, truth yes ; [1] clsfr yes, truth no ; [2] clsfr no, truth yes ; [3] clsfr no, truth no
	# a.k.a. => [0] : tp  |  [1] : fp  |  [2] : fn  |  [3] :tp
	results  = {
		'earn':     [0,0,0,0],
		'acq':      [0,0,0,0],
		'money-fx': [0,0,0,0],
		'grain':    [0,0,0,0],
		'crude':    [0,0,0,0]
	}
	
	
	vocab_size = len(Vocablory)
	
	topics = test_set
	
	num = 0
	score = 0
	for topic in topics:                                                          # these two traverse all articles together
		num += len(test_set[topic].article_list)
		for article in test_set[topic].article_list:                              # these two traverse all articles together


			for some_topic in test_set: # is this article from test_topic
				real_topic = article.topic
				x = classify(article, training_set,set_of_k_tokens_s=k_tokens_set, token_volume=vocab_size, tot_num_articles=num_of_articles)
				predicted_topic = x[0][1]  #x[0] is the tuple of the `winner topic`, x[0][1] is the name of the topic
				if some_topic == predicted_topic: # we say yes
					if some_topic == real_topic: #truth says yes
						results[some_topic][0]+=1
						score+=1
					else:               #truth says no
						results[some_topic][1]+=1

				else: #we say no
					if some_topic == real_topic:  # truth says yes
						results[some_topic][2]+=1
					else:  # truth says no
						results[some_topic][3]+=1

	for topic in results:
		print(topic, results[topic], sum(results[topic]))
	
	macro_avg_prec = 0
	for topic in  results:
		r = results[topic]
		prec_on_topic = r[0]/(r[0]+r[1])
		macro_avg_prec+=prec_on_topic/5
		print('precision on topic "' + topic + '":', prec_on_topic)

	true = 0
	false = 0
	for topic in  results:
		r = results[topic]
		true+=r[0]
		false+=r[1]
	micro_avg_prec = true / (true + false)

	macro_avg_recall = 0
	for topic in  results:
		r = results[topic]
		recall_on_topic = r[0]/(r[0]+r[2])
		macro_avg_recall += recall_on_topic/5
		print('recall on topic "' +  topic + '":', recall_on_topic)


	positive = 0
	negative = 0
	for topic in  results:
		r = results[topic]
		positive+=r[0]
		negative+=r[2]
	micro_avg_recall = positive / (positive + negative)

	F_micro = 2*micro_avg_prec*micro_avg_recall/(micro_avg_prec+micro_avg_recall)
	F_macro = 2*macro_avg_prec*macro_avg_recall/(macro_avg_prec+macro_avg_recall)

	print('macro_avg_prec: ', macro_avg_prec, '\nmicro_avg_prec: ', micro_avg_prec, '\nmacro_avg_recall: ', macro_avg_recall, '\nmicro_avg_recall: ', micro_avg_recall, '\nHarmonic mean of  macro P and R: ', F_macro, '\nHarmonic mean of micro P and R: ', F_micro, sep='')
	
	
	# num = 0
	# score = 0
	# for test_topic in test_set:
	# 	for article in test_set[test_topic].article_list:
	# 		num += 1
	# 		x = classify(article, training_set,set_of_k_tokens_s=k_tokens_set, token_volume=vocab_size, tot_num_articles=num_of_articles)
	# 		# print(article.topic == x[0][1], article.topic , x[0])
	# 		if article.topic == x[0][1]: score += 1
			
	print('number of articles in the traininbg set:', num_of_articles)
	print('number of unique tokens:', len(Vocablory))
	# print(total_score * 100 / num, 'percent : (', total_score, 'correct out of', num, ')')
	print('success:', 100*score/num, score , 'out of', num)
