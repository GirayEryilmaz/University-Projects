#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lexrank import  LexRank
from path import Path
import sys

documents = []
documents_dir = Path('Dataset')

for file_path in documents_dir.files('*.txt'):
    with file_path.open(mode='rt', encoding='utf-8') as fp:
        x = fp.readlines()
        i = x.index('\n')
        x = x[:i]
        documents.append(x)

    

lxr = LexRank(documents)


with open('Dataset/' + sys.argv[1], 'r') as f:
    sentences = list(f)

# get summary with classical LexRank algorithm
summary = lxr.get_summary(sentences, summary_size=3, threshold=0.15)
print(summary[0],end='')
print(summary[1],end='')
print(summary[2],end='')
