#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import sys
import os
import numpy as np
from collections import Counter
from math import log, sqrt


TOTAL_NUM_OF_NEWS_STORIES = 1000

ReOb_FOR_WORDS = re.compile(r'[A-Za-z]+')

PATH_TO_DATASET = sys.argv[1]

FILE_FORMAT = '%d.txt'


def news_stories_and_summaries():
	"""
	generator for traversing news stories and summaries together
	stries are read from files
	:return: None
	yields one story at a time (ie one txt content at a time)
	"""
	for i in range(1, TOTAL_NUM_OF_NEWS_STORIES + 1):
		filePath = os.path.join(PATH_TO_DATASET, FILE_FORMAT % i)
		with open(filePath, 'r') as news_story:
			text = news_story.read()
			index_of_break = text.find('\n\n')
			yield i, text[:index_of_break - 1], text[index_of_break + 2:]


def get_idfs():
	"""
	calculates idf values of all words, values are logged on base `e`
	:return: Counter object of idf values
	"""
	df_Counter = Counter()  # will be used for one idf list for all! values are not inverted in this one
	for story_num, news_story, summary in news_stories_and_summaries():
		sentence_words_set = set(
			re.findall(ReOb_FOR_WORDS, news_story))  # find all words in the sentence and form a Counter
		df_Counter.update(sentence_words_set)  # for counting document frequencies of words
	
	# invert df to get idf as : for each word -> df  (number of all documents)/df
	for df_key in df_Counter:
		df_Counter[df_key] = log(TOTAL_NUM_OF_NEWS_STORIES / df_Counter[df_key])
	
	return df_Counter  # this is now idf_Counter


def idf_modified_cosine(s1, s2, idfs):
	"""
	an implementation of some kind of tf-idf-cosine similariy
	:param s1: one sentence
	:param s2: other sentence
	:param idfs: Counter of idf's
	:return: the cosine value (similarity metric 0< <1)
	"""
	tf_Counter_s1 = Counter(re.findall(ReOb_FOR_WORDS, s1))
	tf_Counter_s2 = Counter(re.findall(ReOb_FOR_WORDS, s2))
	
	nominator = 0
	denom_left_sqr = 0
	denom_right_sqr = 0
	for w in tf_Counter_s1.keys() | tf_Counter_s2.keys():  # union
		nominator += tf_Counter_s1[w] * tf_Counter_s2[w] * idfs[w] ** 2
		denom_left_sqr += (tf_Counter_s1[w] * idfs[w]) ** 2
		denom_right_sqr += (tf_Counter_s2[w] * idfs[w]) ** 2
	try:
		return nominator / (sqrt(denom_left_sqr) * sqrt(denom_right_sqr))
	except:
		return 0


def magnitude(x):
	"""
	length of x
	:param x: a vector (np.array)
	:return: length of given vector
	"""
	y = np.sqrt(np.transpose(x).dot(x))
	return y[0][0]


def power_method(cos_matrix, n, e=0.01):
	"""
	famous power iteration
	:param cos_matrix: the matrix to multiply with
	:param n: the size of matrix
	:param e: max error allowed
	:return: the resulting vector
	"""
	c_m_t = np.transpose(cos_matrix)
	
	p = 1/n
	pt_old = np.array([p]*n).reshape(n, 1)
	pt_curr = pt_old
	while True:
		pt_curr = np.matmul(c_m_t, pt_curr)
		sigma = magnitude(pt_curr - pt_old)
		if sigma < e: break
		pt_old = pt_curr
	return pt_curr[:, 0]


def add_teleportation_effect_to(transition_matrix, transportation_rate=0.14):
	"""
	adds teleportation vector to given matrix
	:param transition_matrix: the matrix to add teleportation effect to
	:param transportation_rate: the transportation rate
	:return: None
	"""
	n = len(transition_matrix)
	random_hop_prob = 1.0 / n
	transition_matrix *= (1 - transportation_rate)
	the_prob = transportation_rate * random_hop_prob
	transition_matrix += the_prob


# def normalize_columns_of(matrix):
# 	n = len(matrix)
# 	for column_num in range(n):
# 		column_max = max(matrix[row_num][column_num] for row_num in range(n))
# 		for row_num in range(n):
# 			matrix[row_num][column_num] = matrix[row_num][column_num] / column_max


def LexRank(sentences, idfs, t=0.1):
	"""
	famous lexrank algorithm
	:param sentences: list of sentences to summaries
	:param idfs: the idfs (assuming Counter object from collections)
	:param t: the threshold
	:return: vector of lexranks of given sentences
	"""
	n = len(sentences)
	cos_matrix = [[0 for i in range(n)] for j in range(n)]  # 2D array as in double[n][n]
	degree = [0] * n
	
	for i in range(n):
		for j in range(n):
			cos_matrix[i][j] = idf_modified_cosine(sentences[i], sentences[j], idfs)
			if cos_matrix[i][j] > t:
				cos_matrix[i][j] = 1
				degree[i] += 1
			else:
				cos_matrix[i][j] = 0
	
	for i in range(n):
		for j in range(n):
			try:
				cos_matrix[i][j] = cos_matrix[i][j] / degree[i]
			except:
				cos_matrix[i][j] = 0
	cos_matrix = np.array(cos_matrix)
	add_teleportation_effect_to(cos_matrix)
	l = power_method(cos_matrix, n)
	return l

##################################### printing stuff ###################################################

def print_sentences(arr):
	for sent in arr:
		print()
		print(sent)
		
	print("_________________________________________")
	print("-----------------------------------------")


def print_summaries():
	for story_num, news_story, summary in news_stories_and_summaries():
		sentences = news_story.splitlines()
		l = LexRank(sentences=sentences, idfs=idfsCounter)
		
		sum_sent_num =  len(summary.splitlines())
		best_sentences = []
		winner_indices = l.argsort()[-sum_sent_num:][::-1]
		
		for i in winner_indices:
			best_sentences.append(sentences[i])
		
		
		# # with open(os.path.join("summaries", FILE_FORMAT % story_num), 'w') as r_s:
		# 	# r_s.write(summary)
		
		with open(os.path.join("summaries", 'm' + FILE_FORMAT % story_num), 'w') as m_s:
			m_s.write("\n".join(x for x in best_sentences) + '\n')
		
		# print_sentences(best_sentences)


def print_matrix(matrix, dec='2',space='10'):
	dec , space = str(dec), str(space)
	x, y = None, None
	try:
		x,y = matrix.shape
	except:
		x = matrix.shape
	
	form = "{:" + space + "." + dec + "f}"
	if not y:
		print(' '.join(form.format(x) for x in matrix))
		return
		
	for row in matrix:
		print(' '.join(form.format(x) for x in row))


def print_best_sentences(lexranks, all_sentences):
	winner_indices = lexranks.argsort()[-3:][::-1]
	best_sentences = []
	for i in winner_indices:
		best_sentences.append(all_sentences[i])
	print_sentences(best_sentences)


######################################## main ############################

if __name__ == '__main__':
	
	idfsCounter = get_idfs()
	
	# print_summaries()
	
	##################### query processing ###############################
	
	with open(os.path.join(PATH_TO_DATASET, sys.argv[2]), 'r') as query_file:
		text = query_file.read()
		index_of_break = text.find('\n\n')
		q_sentences = text[:index_of_break - 1].splitlines()
	
	
	lexranks = LexRank(q_sentences, idfs=idfsCounter)
	
	# print_best_sentences(lexranks, q_sentences)
	
	print_matrix(lexranks,dec='6', space='0')