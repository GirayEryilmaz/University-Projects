#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


data = {'1': set(), '-1': set(), '0': set()}



data_file = sys.argv[1]
ratio = float(sys.argv[2])

eq_num = False
count = 0
with open(data_file,'r') as all_data:
	for line in all_data:
		label, id_num, text = line.split("\t")
		data[label].add(line)
		count+=1
		# print(label, id_num, text)

print(count)

test_data = []
train_data = []

pos = list(data['1'])
notr = list(data['0'])
neq = list(data['-1'])

if eq_num:
	mi = min(len(pos), len(notr), len(neq))
	num_pos =  num_notr = num_neq = int(mi * ratio)
else:
	num_pos, num_notr, num_neq = int(ratio * len(pos)), int(ratio * len(notr)), int(ratio * len(neq))
	mi = -1
	

print(num_pos, num_notr, num_neq)

test_data.extend(pos[:num_pos])
train_data.extend(pos[num_pos:mi])

test_data.extend(notr[:num_notr])
train_data.extend(notr[num_notr:mi])

test_data.extend(neq[:num_neq])
train_data.extend(neq[num_neq:mi])


with open('train_set', 'w') as ts:
	for line in train_data:
		ts.write(line)


with open('test_set', 'w') as ts, open('test_correct_labels','w') as tcl:
	for line in test_data:
		label, id_num, text = line.split("\t")
		ts.write(text)
		tcl.write(label + '\n')
