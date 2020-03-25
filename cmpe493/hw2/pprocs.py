#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import utils
from collections import namedtuple, Counter
from Article import Article

# named tuple used in data_collection see pprocs's parse method
c_t = utils.c_t


topics_of_interest = ['earn', 'acq', 'money-fx', 'grain', 'crude']


# compile regex patterns once then use forevermore
article_pattern = re.compile(r'<reuters.*?</reuters>',re.DOTALL)
topic_pattern = re.compile(pattern=r'<d>(.*?)</d>')
id_pattern = re.compile(pattern=r'newid="(.*?)"')
title_pattern = re.compile(pattern=r'<title>(.*?)</title>',flags=re.DOTALL)
body_pattern = re.compile(pattern=r'<body>(.*?)</body>',flags=re.DOTALL)
type_pattern = re.compile(pattern=r'lewissplit="(.*?)"')
ascii_word_pattern = re.compile(r'[a-z]+') # the text shall be lowered before


def topics_of(article):
	"""
	helper method
	uses regex to extract `topics list` of article
	:param article: the article as a string in the xm format
	:return:the list of topics of given article
	"""
	return re.findall(pattern=topic_pattern,string=article)


def the_topic_of(article):
	"""
	uses regex to extract `the topic` of given article
	:param article: the article as a string in the xm format
	:return: the topic iff the article has one and only one of our 5 five topics of interest
	"""
	all_ready_got_one = False
	topic_of_article = None
	for topic in topics_of(article): # parse-fetch topics of this article
		if topic in topics_of_interest:
			if all_ready_got_one:
				return None
			else:
				all_ready_got_one = True
				topic_of_article = topic
	return topic_of_article


def id_of(article):
	"""
	uses regex to extract `the id` of given article
	:param article: the article as a string in the xm format
	:return: the id of the article as a string not int
	"""
	return re.search(pattern=id_pattern,string=article).group(1) # we dont expect any article with no id


def text_of(article):
	"""
	uses regex to extract `the text` of given article
	fetches body and title fields of the article if they exist to form the text, other text are ignored
	:param article: the article as a string in the xm format
	:return: title + '\n' + body of the article, empty string if neither exist
	"""
	title, body = '', ''
	try:
		title = re.search(pattern=title_pattern,string=article).group(1)
	except (IndexError , AttributeError):
		pass
	
	try:
		body = re.search(pattern=body_pattern,string=article).group(1)
	except (IndexError , AttributeError):
		pass
	
	return '\n'.join([title, body])


def type_of(article):
	"""
	uses regex to extract `the type` of given article that is one of 3 {'test', 'train', 'not-used'}
	:param article: the article as a string in the xm format
	:return: the type, one of three {'test', 'train', 'not-used'}
	"""
	return re.search(pattern=type_pattern,string=article).group(1)


def parse_data(text):
	"""
	parses given collection of articles in a text, prepares a data collection
	:param text: given collection of articles in a text, reuters data set xml format expected
	:return: the parsed data collection
	"""
	# first counter holds `token : number of occurrence in the topic` tuples
	# the list holds Article objects extracted
	# second one holds `token : number of articles that it occurrences in the topic` tuples  within the set of course
	data_collection =   {
							'train':{
								'earn':     c_t(Counter(), [], Counter()),
								'acq':      c_t(Counter(), [], Counter()),
								'money-fx': c_t(Counter(), [], Counter()),
								'grain':    c_t(Counter(), [], Counter()),
								'crude':    c_t(Counter(), [], Counter())
							},
		
							'test':{
								'earn':     c_t(Counter(), [], Counter()),
								'acq':      c_t(Counter(), [], Counter()),
								'money-fx': c_t(Counter(), [], Counter()),
								'grain':    c_t(Counter(), [], Counter()),
								'crude':    c_t(Counter(), [], Counter())
							},
		
							'not-used':{
								'earn':     c_t(Counter(), [], Counter()),
								'acq':      c_t(Counter(), [], Counter()),
								'money-fx': c_t(Counter(), [], Counter()),
								'grain':    c_t(Counter(), [], Counter()),
								'crude':    c_t(Counter(), [], Counter())
							}
						}
	
	# get article texts as a list
	article_texts_list = re.findall(pattern=article_pattern, string=text)
	
	# traverse all article texts
	for article in article_texts_list:
		
		# get topic
		topic = the_topic_of(article)
		if topic is None:
			continue
		
		# get text : title + body
		text = text_of(article)
		if text.isspace():
			continue
		
		# get id
		id = id_of(article)
		
		# get type
		type = type_of(article)
		
		# instabtiate Article object
		article = Article(id,topic,text,type)
		
		# make tokenization of text internally
		article.tokenize(stopwords=utils.stopwords,re_pattern=ascii_word_pattern)
		
		# update data_collection appropriately
		temp_counter, temp_lst ,unqs_counter = data_collection[type][topic] # tuples are immutable so we cheat
		temp_counter += article.token_counter # += wouldn't work on a tuples index   | adding new words to this topic counter of words
		temp_lst.append(article) # add the Article object to Articles of this topic
		unqs_counter.update(set(article.token_counter)) # For each token counting number of articles in this topic having it
	
	return data_collection


if __name__ == '__main__':
	
	# read all sgm files of interest to a list

	start = 0
	num_of_files = 22
	allTexts = []
	for i in range(start,start + num_of_files):
		allTexts.append(utils.get_articles_from_file('Dataset/reut2-' + '{:03d}'.format(i) + '.sgm'))
	
	corpus_dump = '\n'.join(allTexts).lower() # join all the text and make it lower-case
	data_collection = parse_data(text=corpus_dump) # fetch data_collection
	
	utils.do_pickle(data_collection,'data_collection') # pickle it for other scripts to use later
