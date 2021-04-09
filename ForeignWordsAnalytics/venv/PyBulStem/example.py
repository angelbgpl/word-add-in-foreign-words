#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# PyBulStem example usage

from nltk.tokenize import word_tokenize, sent_tokenize, wordpunct_tokenize
from bulstem import stem, MIN_WORD_LEN

text = "престъпността"

for word in wordpunct_tokenize(text):
	if len(word) >= MIN_WORD_LEN:
		print(stem(word)),
	# print word.encode('utf-8'),
