'''
Nick Boukis & Sami Shahin
EC504
bloomSync.py
'''

from pybloom import BloomFilter
import pprint

def compare_blooms(first_bloom, second_bloom, index_dict):
	packet_first_to_second 	   = []
	index_packet_first_to_second_def = []
	index_packet_first_to_second_meb = []

	# Check for differences in bloom filters
	for i in range(len(first_bloom.bitarray)):
		if first_bloom.bitarray[i] == True and second_bloom.bitarray[i] == False:
			index_packet_first_to_second_def.append(i)
		elif first_bloom.bitarray[i] == True and second_bloom.bitarray[i] == True:
			index_packet_first_to_second_meb.append(i)

	# Build packet based on bloom filter differences
	for index in index_packet_first_to_second_def:
		for entry in index_dict[index]:
			packet_first_to_second.append(entry)

	# Uncomment to increase accurace & decrease efficiency
	"""
	for index in index_packet_first_to_second_meb:
		for entry in index_dict[index]:
			if entry in first_bloom:
				packet_first_to_second.append(entry)
	"""

	# Remove duplicates
	return list(set(packet_first_to_second))
