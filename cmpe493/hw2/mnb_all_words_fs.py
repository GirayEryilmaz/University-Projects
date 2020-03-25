#!/usr/bin/python3
# -*- coding: utf-8 -*-

import utils
from collections import namedtuple
from pprocs import  Article
import math

# named tuple used in data_collection see pprocs's parse method

c_t = utils.c_t


def classify(article, training_set, token_volume, tot_num_articles):
	"""
	Classifies one article
	:param article: the article to classify
	:param training_set: the training set
	:param token_volume: the number of alll unique tokens in the training set
	:param tot_num_articles: total number of articles in the training set
	:return: a list of tuples sorted by similarity to the article, tuple form is:(<likelyhood_probability>, <topicname>)
	"""
	likelihoods = []
	for category in training_set:
		p_cat = len(training_set[category].cat_tok_counter)/tot_num_articles
		prob = math.log(p_cat) # for explicity
		for token in article.token_counter:
			prob_w_of_c = (training_set[category].cat_tok_counter[token] + 1) / (sum(training_set[category].cat_tok_counter.values()) + token_volume)
			prob += math.log(prob_w_of_c)
		likelihoods.append((prob,category))
	return sorted(likelihoods,key=lambda x: x[0],reverse=True)


if __name__ == '__main__':
	
	data_collection = utils.unpickle('data_collection')
	
	test_set = data_collection['test']  # actually a `dict` not a `set`
	training_set = data_collection['train']  # actually a `dict` not a `set`
	
	
	num_of_articles = sum(len(training_set[tpc].article_list) for tpc in training_set)
	
	
	Vocablory = training_set['earn'].cat_tok_counter \
	            + training_set['acq'].cat_tok_counter \
	            + training_set['money-fx'].cat_tok_counter \
	            + training_set['grain'].cat_tok_counter \
	            + training_set['crude'].cat_tok_counter
	
	
	vocab_size = len(Vocablory)

	num = 0
	score = 0
	for test_topic in test_set:
		for article in test_set[test_topic].article_list:
			num += 1
			x = classify(article, training_set, token_volume=vocab_size, tot_num_articles=num_of_articles)
			if article.topic == x[0][1]: score += 1


	
	# stats #
	
	n_o_a_TrainingS = list((tpc, len(training_set[tpc].article_list)) for tpc in training_set)
	n_o_a_TestS = list((tpc, len(test_set[tpc].article_list)) for tpc in test_set)
	
	
	print('number of articles in the traininbg set:', sum(x[1] for x in n_o_a_TrainingS,))
	print('number of articles in the test set:', sum(x[1] for x in n_o_a_TestS))
	print('number of unique tokens:', len(Vocablory))
	print(score * 100 / num, 'percent : (', score, 'correct out of', num, ')')
	print("training set :", n_o_a_TrainingS)
	print('test set :', n_o_a_TestS)