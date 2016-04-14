'''
Sami Shahin
EC504
autocomplete_Functions.py
'''

import re
import trie.py

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