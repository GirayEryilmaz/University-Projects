# -*- coding: utf-8 -*-
#!/usr/bin/python

import string

count = 0
tot = 0

with open("combined-train.txt",'w') as comb:
	with open("Train/negative-train", 'r') as f:
		text = f.read()
		text = text.translate(str.maketrans('', '', string.punctuation))
		lines = text.replace("\t\t\t","\t").splitlines()
		
		# for i in range(1121):
		# 	comb.write("-1\t" + lines[i] + '\n')

		for line in lines:
			comb.write("-1\t" + line + '\n')
			comb.write("-1\t" + line + '\n')
			comb.write("-1\t" + line + '\n')
			comb.write("-1\t" + line + '\n')
			comb.write("-1\t" + line + '\n')
			comb.write("-1\t" + line + '\n')
			count+=1
	
	print('bad:', count)
	
	tot += count
	count=0
	
	with open("Train/notr-train",'r') as f:
		text = f.read()
		text = text.translate(str.maketrans('', '', string.punctuation))
		lines = text.replace("\t\t\t","\t").splitlines()
		
		# for i in range(1121):
		# 	comb.write("0\t" + lines[i] + '\n')
			
			
		for line in lines:
			comb.write("0\t" + line + '\n')
			comb.write("0\t" + line + '\n')
			count+=1

	print('notr:', count)
	
	tot += count

	count = 0
	
	with open("Train/positive-train", 'r') as f:
		text = f.read()
		text = text.translate(str.maketrans('', '', string.punctuation))
		lines = text.replace("\t\t\t","\t").splitlines()
		
		
		# for i in range(1121):
		# 	comb.write("1\t" + lines[i] + '\n')
		
		for line in lines:
			comb.write("1\t" + line + '\n')
			comb.write("1\t" + line + '\n')
			comb.write("1\t" + line + '\n')

			count += 1
	
	tot += count
	
	print('good:', count)
	
	print('all: ', tot)


