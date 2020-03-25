#!/usr/bin/python
# -*- coding: utf-8 -*-

point = 0
all = 0
with open('output.txt','r') as o, open('test_correct_labels', 'r') as corr:
	for output_line, correct_ans in zip(o,corr):
		label,text = output_line.split('\t\t\t')
		if label == correct_ans.strip():
			point+=1
		all+=1

print(point,all,point/all)