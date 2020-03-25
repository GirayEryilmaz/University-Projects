#!/usr/bin/python3

import string
import re
from collections import Counter

a = Counter()
b = Counter()
a.update()

text = "abc df \n sdfv \t $3.45 \n"



def roughTokenGenerator(text):

	chars = []
	for ch in text:
		if not ch.isspace():
			chars.append(ch)
		else:
			if chars: #meaning not empty
				yield(''.join(chars))

				chars = []

blackList = string.punctuation.replace('.', '').replace('$','')

def harshTokenGenerator(text):
	chars = []
	for ch in text:
		if not (ch in blackList or ch.isspace()) :
			chars.append(ch)
		else:
			if chars: #meaning not empty
				yield(''.join(chars))
				chars = []



for token in enumerate(roughTokenGenerator(text)):
	print(token)

re.sub(r'(?<!\d)(\.)+(?!\d)','', '0.12')



