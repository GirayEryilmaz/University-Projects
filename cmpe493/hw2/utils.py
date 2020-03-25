#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pickle
from collections import namedtuple

# named tuple used in data_collection see pprocs's parse method
c_t = namedtuple(typename='c_t',field_names=['cat_tok_counter','article_list', 'unqToken_artcl_counter'])



def get_articles_from_file(fileName):
	"""
	read a file and return it text
	:param fileName: the name of the file to read
	:return: the text
	"""
	with open(fileName, errors='ignore') as file_:
		return file_.read()


# the stop words
stopwords = {'a', 'all', 'an', 'and', 'any', 'are', 'as', 'be', 'been', 'but', 'by ', 'few', 'for', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its', 'many', 'me', 'my', 'none', 'of', 'on ', 'or', 'our', 'she', 'some', 'the', 'their', 'them', 'there', 'they', 'that ', 'this', 'us', 'was', 'what', 'when', 'where', 'which', 'who', 'why', 'will', 'with', 'you', 'your'}



def unpickle(filename):
	"""
	unpickles a file
	:param filename: name of the file to unpickle
	:return: the objects unpickled
	"""
	if not '.' in filename:
		filename += '.pickle'
	file_ = open(filename, 'rb')
	unpickled = pickle.load(file=file_)
	file_.close()
	return unpickled


def do_pickle(objct,filename):
	"""
	pickles an object
	:param objct: object to pickle
	:param filename: name of the pickle file
	:return: None
	"""
	if not '.' in filename:
		filename += '.pickle'
	file_ = open(filename, 'wb')
	pickle.dump(objct, file=file_)
	file_.close()
