'''
Sami Shahin
EC504
Trie creation
Trie.py
'''

from operator import itemgetter

#I guess it's time for auto complete


class trie:
	def __init__(self, key = '', hits = 0):
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
	
	def popular(self, base = '', branch = ''):
		#returns 4 popular results starting at base
		#check if len(base = 1)
		if len(base) == 1:
			return self.children[base].popular(branch = branch+base)
		elif not base:
			#find all words/elements below this node
			elements = []
			for key in self.children:
				if self.children[key].hits:
					#add to elements
					elements.append((branch + key, self.children[key].hits))
				elements.extend(self.children[key].popular(branch= branch + key) )
			#sort elements and keep only first four elements
			if len(elements) > 4:
				elements = popular_sort(elements)[0:4]
			return elements
			
		else:
			#iterate down one child 
			return self.children[base[0]].popular(base[1:], branch = branch+base[0])

	def toString(self):
		#print out full trie
		#prints each branch, root to leaves
		#TESTING ONLY
		if self.hits:
			print(self.key + ": " + str(self.hits))
		else:
			print(self.key)

		for key in self.children:
			self.children[key].toString()


#sorting function for popularity search
def popular_sort(some_list):
	#orders by number of hits
	return sorted(some_list, key = itemgetter(1), reverse = True)

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
root = trie()
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