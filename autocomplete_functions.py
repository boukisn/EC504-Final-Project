'''
Sami Shahin
EC504
autocomplete_Functions.py
'''

import re
from trie import trie

#define function to accept txt file, create trie, return that trie
def create_trie(filename):
	text = open(filename)
	#create an empty trie called file_trie
	file_trie = trie('', 0)

	#regex for parsing each line
	pattern = re.compile(r"^([\w]+)\s*(\d+)")
	
	#begin regular expressions on file line by line
	while(text.readable()):
		line = text.readline()
		#parse with regex
		match = pattern.match(line)
		if match is not None:
			#add each line's word and hits to trie
			trie.add_child(match.groups()[0], match.groups()[1])
	
	text.close()
	return file_trie

#returning popular results
def search_trie(some_trie, base=''):
	#returns 4 most popular elements of trie
	return some_trie.popular(base)


root = trie()
words = [('aaaaa', 14),('be',2),('bee',999),('been', 10),('ben', 15), ('sami', 1), ('nick', 1),('soup', 20), ('so', 4),('zootopia', 1000), ('zoo', 99)]
for word in words:
	root.add_child(word[0], word[1])

print(search_trie(root, ""))