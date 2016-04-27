'''
Nick Boukis & Sami Shahin
EC504
autocomplete_functions.py
'''

import re
from trie import trie
import time

# Define function to accept txt file, create trie, return that trie
def create_trie(filename):
	text = open(filename, buffering=1)
	
	# Create an empty trie called file_trie
	file_trie = trie()

	# Regex for parsing each line
	pattern = re.compile(r"^(\w+?)\s*?(\d+?)$")
	
	# Begin regular expressions on file line by line
	while(text):
		line = text.readline()
		if not line:
			break
		
		# Parse with Regex
		match = pattern.match(line)
		if match is not None:
			# Add each line's word and hits to trie
			file_trie.add_child(match.groups()[0], int(match.groups()[1]))

	text.close()

	return file_trie

def new_elements(some_trie, *childs):
	# Adds elements to a trie
	# If elements coming in from other databases can be put into a list of tuples, this would work
	for child in childs:
		some_trie.add_child(child[0], int(child[1]))


# Returning popular results
def search_trie(some_trie, base=''):
	# Returns 4 most popular elements of trie
	return some_trie.popular(base)


