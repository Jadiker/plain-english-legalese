global DPtable

def searchterm(term, lawdict):
	if not lawdict:
		raise NameError("Dictionary failed to load")
	if term in lawdict:
		return lawdict[term]

	nearterm = findmatch(term, lawdict)
	# print("hello!" + str(lawdict[nearterm]))
	return nearterm
# finds the words in the list that begin with the sam eletter
def split_lst(term, law_list):
	f = term[0]
	new_list = []

	for word in law_list:
		if f == word[0]:
			new_list.append(word)

	return new_list


def findmatch(term, lawdictterms):
	global DPtable
	lawdictterms = list(lawdictterms.keys())
	lawdictterms.sort()

	# binary search first index stored in i
	new_list = split_lst(term, lawdictterms)

	minword = False
	minlength = 1000
	for i in range(len(new_list)):
		# edit distance
		DPtable = []
		DPtable = [[-1 for a in range(len(new_list[i]))] for b in range(len(term))]
		if editdistance(term, new_list[i]) < minlength:
			minlength = editdistance(term, new_list[i])
			minword = new_list[i]
		
	# DPtable = []
	# DPtable = [[-1 for a in range(4)] for b in range(len(term))]
	# print(editdistance(term, "rove"))

	return minword


def editdistance(test, target):
	global DPtable

	testlen = len(test) - 1
	targetlen = len(target) - 1
	print(test + ": " + str(testlen))
	print(target + ": " + str(targetlen))
	if testlen == 0:
		DPtable[testlen][targetlen] = targetlen
		return targetlen - testlen

	elif targetlen == 0:
		DPtable[testlen][targetlen] = testlen
		return testlen - targetlen


	# print(DPtable[testlen - 1][targetlen - 1])
	if test[-1] == target[-1]:
		print("poop")
		return editdistance(test[:-1], target[:-1])

	if DPtable[testlen - 1][targetlen - 1] == -1:
		DPtable[testlen - 1][targetlen - 1] = editdistance(test[:-1], target[:-1]) + 1

	if DPtable[testlen - 1][targetlen] == -1:
		DPtable[testlen - 1][targetlen] = editdistance(test[:-1], target) + 1

	if DPtable[testlen][targetlen - 1] == -1:
		DPtable[testlen][targetlen - 1] = editdistance(test, target[:-1]) + 1

	print (DPtable)
	print(target)
	return min(DPtable[testlen - 1][targetlen - 1], 
			DPtable[testlen - 1][targetlen], 
			DPtable[testlen][targetlen - 1]) 


a = {
		"hello": "world",
		"airplane": "fuel", 
		"rocket": "fuel2", 
		"car": "electricity", 
		"boat": "propeller",
		"rover": "robotic arm",
		"submarine": "nuclear core",
		"triage": "jepardy"
	}

term = "you"
print(searchterm(term, a))