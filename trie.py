'''
Sami Shahin
EC504
Trie creation
Trie.py
'''

import re

#I guess it's time for auto complete


class trie:
	def __init__(self, key, hits):
		self.key = key
		self.hits = hits
		self.children = dict()

	def add_child(self, c_key, c_hits):
		#c_key c_hits, a single element ,creates a path in the trie
		if c_key[0] in self.children:
			if len(c_key) == 1:
				self.children[c_key[0]].hits = c_hits
			else:
				self.children[c_key[0]].add_child(c_key[1:], c_hits)
		elif len(c_key) == 1:
			self.children[c_key[0]] = trie(c_key[0], c_hits)
		else:
			self.children[c_key[0]] = trie(c_key[0], 0)
			self.children[c_key[0]].add_child(c_key[1:], c_hits)


	def search(self, word):
		#returns hits for a word
		if word[0] in self.children:
			if len(word) == 1:
				return self.children[word[0]].hits
			else:
				return self.children[word[0]].search(word[1:])
		else:
			return 0

	#define a method for finding most popular results starting with base string
	'''
	def popular(self, base = ''):
		#returns 4 popular results starting at base
		#check if len(base = 1)
		if len(base) == 1:
			return self.children[base].popular()
		elif not base:
			#find all words/elements below this node
			elements = {}
			for key in self.children:
				if self.children[key].hits:
					#add to elements
					elements.append((key, self.children[key].hits))
				subelements = self.children[key].popular()
				for elm in subelements:
					elm[0] = self.key + elm[0]
				elements.extend(subelements)
			final = [('', 0),('', 0),('', 0),('', 0)]
			for elm in elements:
				for fin in final:
					if elm[1] > fin[1]:




		else:
			#iterate down one child 
			return self.children[base[0]].popular(base[1:])
	'''
	def toString(self):
		#print out full trie
		#prints each branch, root to leaves
		#TESTING ONLY
		if self.hits:
			print(self.key + ": " + str(self.hits))
		else:
			print(self.key, end='')

		for key in self.children:
			self.children[key].toString()




'''
	def popular(self, base):
		#returns the keys of the top four highest hits values starting with base
		pop_list = [['', 0], ['', 0], ['', 0], ['', 0]]
		i = 0
		for key in self.children:
			if self.children[key].hits > pop_list[i][1]:
				#if hits more than what was previously found, 
'''

#root = trie('', 0)

'''
aaaaa  14
be  2
bee 999
been 10
ben 15
soup 3
so  1
zoo 99
zootopia 1000
'''
'''
words = [('aaaaa', 14),('be',2),('bee',999),('been', 10),('ben', 15), ('sami', 1), ('nick', 1),('soup', 20), ('so', 4),('zootopia', 1000), ('zoo', 99)]
for word in words:
	root.add_child(word[0], word[1])

'''

#root.toString()

"""
#print(root.search('aaaaa'))


#take file, create trie
#for new elements, adding to the trie is the height of the trie
#sample

text = '''yolo   13
sawg   6
dank 8
bananas345'''
"""
#entries = re.split("\n+",text)
"""
print(entries)



for word in wordmass:
	root.add_child(word[0], word[1])

root.toString()
#well I think that'll do

"""