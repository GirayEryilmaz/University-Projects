#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import time
import sys
from stemmer import PorterStemmer
from collections import Counter


"""
	some statistics
"""
total_num_words_before = 0
total_num_words_after = 0
# unique_before_set = set() # take len(freqDict_before) instead
# unique_after = 0 # not needed, look from dictionary.txt instead

freqDict_before = Counter()
freqDict_after = Counter()

def add_freqDict_after(tk):
	if tk in freqDict_after:
		freqDict_after[tk] = freqDict_after[tk]+1
	else:
		freqDict_after[tk] = 1

def add_freqDict_before(tk):
	if tk in freqDict_before:
		freqDict_before[tk] = freqDict_before[tk]+1
	else:
		freqDict_before[tk] = 1




def getTextFromFile(fileName):
	with open(fileName, errors='ignore') as file_:
		return file_.read()


regex = r"NEWID=\"(?P<id>\d+)\"|<TITLE>(?P<title>.+?)</TITLE>|<BODY>(?P<body>.+?)</BODY>"
regexObject = re.compile(regex, re.DOTALL)

libraryBook = {} # A dict. Do not confuse with a set. If it was {1,2} then it would be a set. Weird huh?
"""
	a dict of `word stem : [IIIs]`
"""

class Doc():
	"""
		Representing one document
	"""
	def __init__(self, id=0):
		self.id = int(id)
		self.text = ''
		self.tokenList = None

	def appendText(self, textToAppend):
		self.text += textToAppend

	def __repr__(self):
		return self.text


	def doIndexing(self,libraryBook={}):
		"""
		
		:param libraryBook: the dictionary to put tokens and indexes in to
		you dont have to pass the parameter if you dont want to do indexing and just want the tokens
		:return:
		"""
		self.tokenList = [] # token list
		for i, token in enumerate(regexStyleGenerator(self.text)): # traverse tokens of this Doc`s text, `i` means i`th word(token) in the doc
			self.tokenList.append(token) # add this token to `list` of tokens of this Doc
			
			# we are also preparing for inverted index here
			try:
				invIndexItem_Dict = libraryBook[token]
				try:
					invIndexItem_Dict[self.id].addWordIndex(i)
				except KeyError: # meaning the III is not in the list of this token so index() threw exception
					III = invIndexItem(self.id)
					III.addWordIndex(i)
					invIndexItem_Dict[self.id] = III
					
			except KeyError: # exception means this token is not in the libraryBook `dictionary` yet
				temp_III = invIndexItem(self.id)
				temp_III.addWordIndex(i)
				libraryBook[token] =  {self.id : temp_III} # add this to libraryBook dict
				
		return self.tokenList # return it, it may be needed, @side-effect

class invIndexItem():
	"""
		a container for representing `docID:posIndex1;posIndex2;...` structure
		defined by docID, see __hash__() below
		holds docID and a list of positional indexes of a token in the doc
	"""
	
	def __init__(self,docID,wordIndexList=None):
		self.docID = docID
		if wordIndexList == None:
			self.wordIndexList = []
		else:
			self.wordIndexList = wordIndexList
	
	def __eq__(self, other):
		if isinstance(self,other.__class__):
			if self.docID == other.docID:
				return True
		elif self.docID == other:
			return True
		
		return False
	
	def __repr__(self):
		l = []
		for i in self.wordIndexList:
			l.append(i)
		return str(self.docID) + '-' + '/'.join(l)
	
	def __str__(self):
		return self.__repr__()
	
	
	def addWordIndex(self,index):
		"""
		
		:param index: the index of the token that is to be added to this inverted index item (doc)'s list
		:return:
		"""
		self.wordIndexList.append(str(index))
	
	def __lt__(self,other):
		if isinstance(self,other.__class__):
			if self.docID < other.docID:
				return True
		elif self.docID < other:
			return True
		
		return False
	
	def __gt__(self,other):
		if isinstance(self,other.__class__):
			if self.docID > other.docID:
				return True
		elif self.docID > other:
			return True
		
		return False
	
	def __hash__(self):
		return self.docID


def getDocsFromFile(fileName):
	"""
		returns list of Doc objects extracted from given file
		:rtype: list[Doc]
	"""
	
	text = getTextFromFile(fileName) # read the file
	docs = []
	iter_ = regexObject.finditer(text)
	for result in iter_:
		if result.group('id') is not None:
			docs.append(Doc(int(result.group('id')))) # add new doc to the `list` with the id
		else:
			# as far as we know, not both of these can be `not none` at the same time
			if result.group('title') is not None:
				docs[-1].appendText(result.group('title').lower() + '\n') # append to the last element docs `list`
			if result.group('body') is not None:
				docs[-1].appendText(result.group('body').lower()) # append to the last element docs `list`
	return docs


stopWords = {'a', 'all', 'an', 'and', 'any', 'are', 'as', 'be', 'been', 'but', 'by ', 'few', 'for', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its', 'many', 'me', 'my', 'none', 'of', 'on ', 'or', 'our', 'she', 'some', 'the', 'their', 'them', 'there', 'they', 'that ', 'this', 'us', 'was', 'what', 'when', 'where', 'which', 'who', 'why', 'will', 'with', 'you', 'your'}

portertStemmer = PorterStemmer()


ro= re.compile(r'\d+\.+\d+|\w+')
""" regex object for finding words and digits and floats containing dot IN them pre-cooked ready to eat"""

def regexStyleGenerator(text):
	"""
	 A generator that returns tokens of given text
	 makes stopword removel and stemming
	:param text: the text to tokenize
	:return: None but yields tokens
	"""
	global  total_num_words_before,total_num_words_after # for statistics
	
	
	for tk in  re.findall(ro,text):
		
		add_freqDict_before(tk) # collecting statistics
		total_num_words_before += 1 # collecting statistics
		
		if tk not in stopWords:
			total_num_words_after+=1
			add_freqDict_after(tk)
			yield portertStemmer.stem(tk, 0, len(tk) - 1)

def print_stat():
	global total_num_words_beforem, total_num_words_after, freqDict_before, libraryBook
	
	print('#words before', '#words after', '#unique words before' , '#unique words after')
	print(total_num_words_before, total_num_words_after, len(freqDict_before), len(libraryBook))
	
	print("Most frequent items BEFORE stopword removal etc... : ")
	for num, (tk, cnt) in enumerate(freqDict_before.most_common(26)):
		print(num, tk, cnt,sep = ' : ')
	
	print("Most frequent items AFTER stopword removal etc... : ")
	for num, (tk, cnt) in enumerate(freqDict_after.most_common(26)):
		print(num, tk, cnt,sep=' : ')
	

if __name__ == "__main__":
	
	start_time = time.time()
	
	
	allDocs = []
	

	numOfFiles = 22
	
	# see if user wants to limit #of files to use as data, also normalize if user acts unreasonable
	try:
		numOfFiles = int(sys.argv[1])
		if numOfFiles > 22 : numOfFiles =22
		elif numOfFiles < 1 : numOfFiles = 1
	except:
		pass
	
	# collect all docs
	for i in range(numOfFiles):
		allDocs.extend(getDocsFromFile('Dataset/reut2-' + '{:03d}'.format(i) + '.sgm'))
	print("files read... doc's imported...")
	
	print("--- %s seconds ---" % (time.time() - start_time))
	start_time = time.time()
	
	# traverse all docs to doIndexing them
	print("start tokenization... this may take a few secs...")
	for doc in allDocs:
		doc.doIndexing(libraryBook)
	print("tokenization done...", flush=True)
	allDocs.clear()
	
	print("--- %s seconds ---" % (time.time() - start_time))
	start_time = time.time()


	# print dictionary
	with open("dictionary.txt",'w') as dicTxt:
		for index, token in enumerate(sorted(libraryBook)):
			dicTxt.write(token + ' ' + str(index) + '\n')
	print("dictionary.txt printed...", flush=True)
	
	print("--- %s seconds ---" % (time.time() - start_time))
	start_time = time.time()

	# print index
	with open("invertedIndex.txt",'w') as indexFile:
		for index, token in enumerate(sorted(libraryBook)):
			indexFile.write(str(index) + ':')
			for id in sorted(libraryBook[token]): # note dangerous move : dont sort (libraryBook[token]) , it is already sorted
				indexFile.write(str(libraryBook[token][id]) + ' ')
			indexFile.write('\n')
	print("inverted index formed...")
	print("all done")
	
	print("--- %s seconds ---" % (time.time() - start_time))
	
	print_stat()
