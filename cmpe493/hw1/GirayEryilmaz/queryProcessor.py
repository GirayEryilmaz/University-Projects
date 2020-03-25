#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from preprocess import invIndexItem, Doc


def init():
	
	tokenID_token_dict = {} # we could use a tuple list too but this seemed easier
	libraryBook = {} # token : [ III( docID, [index,index,...] ) ] `dictionary`
	# note: this libraryBook has the same purpose but different structure
	
	# read dictionary
	with open('dictionary.txt','r') as dicTxt:
		for line in dicTxt:
			token, tokenID = line[:-1].split(' ') # remove trailing newline then split
			tokenID_token_dict[tokenID] = token
	
	# read the index and populate the `libraryBook`
	with open('invertedIndex.txt','r') as invIndex:
		
		# every line of this for loop is all about one token a a time
		for line in invIndex:
			
			colonIndex = line.index(':')  # get index of delimeter ':'
			
			tokenID = line[:colonIndex]	  # slice left of ':' as tokenID
			
			token = tokenID_token_dict[tokenID] # look up token with token id from tokenID_token_dict
			
			docIDStringList = line[colonIndex+1:-2].split(' ') # get docID-index/index...  as a list
			
			
			
			# prapere value of this token as [ III( docID, [index,index,...] ) ]
			InvIndex_ItemList = []
			for docIDString in docIDStringList:  # traverse `docID-index/index/in...` strings
			
				sepIndex = docIDString.index('-') # get index of seperater '-'
				
				docID = docIDString[:sepIndex]    # get docID, left of '-'
				
				wordIndexes = docIDString[sepIndex+1:].split('/') # get right part and split it to list [index,index,...]
				
				III = invIndexItem(int(docID),wordIndexes) # construct the item
				
				InvIndex_ItemList.append(III) # add it to the list of this tokens items 
			
			libraryBook[token] = InvIndex_ItemList # place the list where it belongs in the dicts
	
	return tokenID_token_dict , libraryBook


def preprocessQuery(query):
	queryL = query.lower()
	q = Doc()
	q.appendText(queryL)
	tokenList = q.doIndexing()
	return tokenList

def handleType1(query,libraryBook):
	queryWords = preprocessQuery(query)
	intersection = set()
	for queryWord in queryWords:
		s = set(libraryBook[queryWord])
		if not intersection: # meanin empty
			intersection = s
		else:
			intersection = s.intersection(intersection)
	
	return sorted([doc.docID for doc in intersection])


def getSurvivors(survivorList,candidateList, maxDistanceAllowed):
	"""
	survivorList,candidateList are index lists of neighboring words in the query
	and they are strictly form THE SAME DOCUMENT
	:param survivorList:
	:param candidateList:
	:param maxDistanceAllowed:
	:return:
	"""
	newSurvivorList = []
	
	if not survivorList: # if no one survived last time return None
		return None
	
	for i in survivorList:
		for j in candidateList:
			if int(i) < int(j)  and int(j) - int(i)  <= int(maxDistanceAllowed)+1:
				newSurvivorList.append(j)
	
	return newSurvivorList



def chainedSelection(queryWords, libraryBook,distances):
	docID_indexList_dict = {}
	
	inters = set() # set of docs
	for qw in queryWords:
		s = set(libraryBook[qw])
		if not inters:
			inters = s
		else:
			inters = inters.intersection(s)
			if not inters: return [] # do not continue, this is crutial because of  `if not inters: inters = s` above
	
	
	# now inters is the set which consists of docs that has all the words (exactly like type1 query)
	for doc in inters:
		docID_indexList_dict[doc.docID] = []
		for qw in queryWords:
			docID_indexList_dict[doc.docID].append(libraryBook[qw][libraryBook[qw].index(doc)])
	
	
	finalIDList = []
	# now docID_indexList_dict is a dictionary as docID : [qw1_IndexList, qw2_IndexList ...]
	for docID in docID_indexList_dict:
		
		indexesList = docID_indexList_dict[docID] # list of III's
		
		
		survivorList = indexesList[0].wordIndexList
		
		for i, dist in enumerate(distances):
			survivorList = getSurvivors(survivorList,indexesList[i+1].wordIndexList,dist)
			if not survivorList: break
			
		if survivorList:
			finalIDList.append(docID)
		
	
	return finalIDList


def handleType3(query, libraryBook):
	distances = list(map(int,re.findall(r'/(\d+)', query))) # get distances map to int than cast to list again
	query = re.sub(r'/\d+', '', query) # remove /<numbers>
	
	queryWords = preprocessQuery(query)
	
	return sorted(chainedSelection(queryWords,libraryBook,distances))


def handleType2(query,libraryBook):
	queryWords = preprocessQuery(query)
	
	distances = [0 for _ in range(len(queryWords)-1)] # w1 w2 w3 = w1 /0 w2 /0 w3
	
	return sorted(chainedSelection(queryWords,libraryBook,distances))




if __name__ == '__main__':
	
	tokenID_token_dict , libraryBook = init()
	
	print("q to exit")

	QueryType = 0
	Query = ''
	while True:
		Query = input("Query: \t")
		if Query == 'q':
			break
		QueryType = Query[:1]
		Query = Query[1:]
		# print(QueryType)
		# print(Query)
		
		try:
			if QueryType == '1':
				inters = handleType1(Query,libraryBook)
				
				print(sorted(inters))
			elif QueryType == '2':
				print(handleType2(Query,libraryBook))
			else:
				print(handleType3(Query,libraryBook))
		except KeyError:
			print([])
