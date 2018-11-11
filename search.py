global DPtable

def searchterm(term, lawdict):
	if not lawdict:
		raise NameError("Dictionary failed to load")
	if term in lawdict:
		return lawdict[term]

	nearterm = findmatch(term, lawdict)
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
	if len(new_list) > 0:
		for i in range(len(new_list)):
			# edit distance
			DPtable = []
			DPtable = [[-1 for a in range(len(new_list[i]))] for b in range(len(term))]
			if editdistance(term, new_list[i]) < minlength:
				minlength = editdistance(term, new_list[i])
				minword = new_list[i]
	else:	
		for i in range(len(lawdictterms)):
			# edit distance
			DPtable = []
			DPtable = [[-1 for a in range(len(lawdictterms[i]))] for b in range(len(term))]
			if editdistance(term, lawdictterms[i]) < minlength:
				minlength = editdistance(term, lawdictterms[i])
				minword = lawdictterms[i]

	return minword


# edit distance calculation, close to perfect!
def editdistance(test, target):
	global DPtable

	testlen = len(test) - 1
	targetlen = len(target) - 1

	if testlen == 0:
		DPtable[testlen][targetlen] = targetlen
		return targetlen - testlen

	elif targetlen == 0:
		DPtable[testlen][targetlen] = testlen
		return testlen - targetlen


	# print(DPtable[testlen - 1][targetlen - 1])
	if test[-1] == target[-1]:
		return editdistance(test[:-1], target[:-1])

	if DPtable[testlen - 1][targetlen - 1] == -1:
		DPtable[testlen - 1][targetlen - 1] = editdistance(test[:-1], target[:-1]) + 1

	if DPtable[testlen - 1][targetlen] == -1:
		DPtable[testlen - 1][targetlen] = editdistance(test[:-1], target) + 1

	if DPtable[testlen][targetlen - 1] == -1:
		DPtable[testlen][targetlen - 1] = editdistance(test, target[:-1]) + 1

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
		"triage": "jepardy", 
		"boaty people": "poop"
	}