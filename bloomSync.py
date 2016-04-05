from pybloom import BloomFilter
import pprint

def compare_blooms(first_bloom, second_bloom, index_dict):
	packet_first_to_second 	   = []
	packet_second_to_first     = []
	index_packet_first_to_second_def = []
	index_packet_first_to_second_meb = []
	index_packet_second_to_first_def = []
	index_packet_second_to_first_meb = []

	for i in range(len(first_bloom.bitarray)):
		if first_bloom.bitarray[i] == True and second_bloom.bitarray[i] == False:
			index_packet_first_to_second_def.append(i)
		elif first_bloom.bitarray[i] == False and second_bloom.bitarray[i] == True:
			index_packet_second_to_first_def.append(i)
		elif first_bloom.bitarray[i] == True and second_bloom.bitarray[i] == True:
			index_packet_first_to_second_meb.append(i)
			index_packet_second_to_first_meb.append(i)

	for index in index_packet_first_to_second_def:
		for entry in index_dict[index]:
			packet_first_to_second.append(entry)

	for index in index_packet_second_to_first_def:
		for entry in index_dict[index]:
			packet_second_to_first.append(entry)

	"""
	for index in index_packet_first_to_second_meb:
		for entry in index_dict[index]:
			if entry in first_bloom:
				packet_first_to_second.append(entry)

	for index in index_packet_second_to_first_meb:
		for entry in index_dict[index]:
			if entry in second_bloom:
				packet_second_to_first.append(entry)
	"""

	return list(set(packet_first_to_second)), list(set(packet_second_to_first))

def sync(database_one_list, database_two_list, database_three_list, size):
	database_one_bloom 	 = BloomFilter(capacity=size, error_rate=0.0001)
	database_two_bloom 	 = BloomFilter(capacity=size, error_rate=0.0001)
	database_three_bloom = BloomFilter(capacity=size, error_rate=0.0001)

	index_dict = {}
	

	print "UNSYNCED DATABASES"
	print "-----------------------------------------------------------"
	print "DB1: " + str(database_one_list)
	print "DB2: " + str(database_two_list)
	print "DB3: " + str(database_three_list)
	print

	for entry in database_one_list:
		indices_used = database_one_bloom.add(entry)
		for index in indices_used:
			if index in index_dict:
			    curr_list = index_dict[index]
			    curr_list.append(entry)
			    index_dict[index] = list(set(curr_list))
			else:
			    index_dict[index] = [entry]

	for entry in database_two_list:
		indices_used = database_two_bloom.add(entry)
		for index in indices_used:
			if index in index_dict:
			    curr_list = index_dict[index]
			    curr_list.append(entry)
			    index_dict[index] = list(set(curr_list))
			else:
			    index_dict[index] = [entry]

	for entry in database_three_list:
		indices_used = database_three_bloom.add(entry)
		for index in indices_used:
			if index in index_dict:
				curr_list = index_dict[index]
				curr_list.append(entry)
				index_dict[index] = list(set(curr_list))
			else:
			    index_dict[index] = [entry]

	"""
	print "INDEX ARRAY"
	print "-----------------------------------------------------------"
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(index_dict)
	print
	"""

	packet_one_to_two, packet_two_to_one	 = compare_blooms(database_one_bloom, database_two_bloom, index_dict)
	packet_one_to_three, packet_three_to_one = compare_blooms(database_one_bloom, database_three_bloom, index_dict)
	packet_two_to_three, packet_three_to_two = compare_blooms(database_two_bloom, database_three_bloom, index_dict)

	print "PACKETS"
	print "-----------------------------------------------------------"
	print "1 -> 2: " + str(packet_one_to_two)
	print "2 -> 1: " + str(packet_two_to_one)
	print "1 -> 3: " + str(packet_one_to_three)
	print "3 -> 1: " + str(packet_three_to_one)
	print "2 -> 3: " + str(packet_two_to_three)
	print "3 -> 2: " + str(packet_three_to_two)
	print "DB1 Receiving: " + str(list(set(packet_two_to_one + packet_three_to_one))) + "  (Sent " + str(len(list(set(packet_two_to_one + packet_three_to_one)))) + ", Was Missing " + str(size - len(database_one_list)) + ")"
	print "DB2 Receiving: " + str(list(set(packet_one_to_two + packet_three_to_two))) + "  (Sent " + str(len(list(set(packet_one_to_two + packet_three_to_two)))) + ", Was Missing " + str(size - len(database_two_list)) + ")"
	print "DB3 Receiving: " + str(list(set(packet_one_to_three + packet_two_to_three))) + "  (Sent " + str(len(list(set(packet_one_to_three + packet_two_to_three)))) + ", Was Missing " + str(size - len(database_three_list)) + ")"
	print

	database_one_list = list(set(database_one_list + packet_two_to_one + packet_three_to_one))
	database_two_list = list(set(database_two_list + packet_one_to_two + packet_three_to_two))
	database_three_list = list(set(database_three_list + packet_one_to_three + packet_two_to_three))

	print "SYNCED DATABASES"
	print "-----------------------------------------------------------"
	print "DB1: " + str(database_one_list)
	print "DB2: " + str(database_two_list)
	print "DB3: " + str(database_three_list)
	print


