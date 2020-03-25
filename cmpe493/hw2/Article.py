import re
from collections import Counter


class Article:
	"""
	represent an Artcile from reuters data set
	"""
	def __init__(self, id, topic ,text ,type):
		"""
		
		:param id: id of the article
		:param topic: topic of the article
		:param text: text (title + body assumed) of the article
		:param type: one of 3 : {'train', 'test', 'not-used'}
		"""
		self.id = id
		self.topic = topic
		self.text = text
		self.type = type
	
	def __repr__(self):
		"""
		:overrrides the object's repr method for easy printing
		:return: string repr of the object
		"""
		return '  :  '.join(['\n Article ' + self.id, self.type, self.topic, self.text])
	
	def tokenize(self ,stopwords ,re_pattern = None):
		"""
		tokenizes internel text, removing stopwords
		:param stopwords:  set of stopwords
		:param re_pattern: regex the pattern to use while tokenizing the text
		:return: None, sets self.token_counter which is an counter object holding token:number of occurrence pairs
		"""
		tokens = []
		if re_pattern is not None:
			ptrn = re_pattern
		else:
			ptrn = r'[\-a-z]+'
		for tkn_match in re.finditer(pattern=ptrn, string=self.text):
			tkn = tkn_match.group()
			if not tkn in stopwords:
				tokens.append(tkn)
		self.token_counter = Counter(tokens)