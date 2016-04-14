'''
Sami Shahin
EC504
autocomplete_Functions.py
'''

import re

from trie import trie

#define function to accept txt file, create trie, return that trie
def create_trie(filename):
	text = open(filename, buffering=1)
	#create an empty trie called file_trie
	file_trie = trie()

	#regex for parsing each line
	pattern = re.compile(r"^([\w]+)\s*(\d+)")
	
	#begin regular expressions on file line by line
	while(text):
		line = text.readline()
		if not line:
			break
		#parse with regex
		match = pattern.match(line)
		if match is not None:
			#add each line's word and hits to trie
			file_trie.add_child(match.groups()[0], int(match.groups()[1]))

	
	text.close()
	return file_trie

#returning popular results
def search_trie(some_trie, base=''):
	#returns 4 most popular elements of trie
	return some_trie.popular(base)


#check for faster txt handling

#root = create_trie(".\\db1\\DC1-sampleQueries.txt")

#print(search_trie(root, "b"))