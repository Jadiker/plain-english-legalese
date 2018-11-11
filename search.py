def searchterm(term, lawdict):
	if not lawdict:
		raise RuntimeError
	if term in lawdict:
		return lawdict[term]

	nearterm = findmatch(term, lawdict)

	return lawdict[nearterm]



def findmatch(term, lawdictterms):
	lawdictterms = list(lawdictterms.keys())
	lawdictterms.sort()

	# binary search first index stored in i

	mineditdist = 0;
	while(lawdictterms[i] == term[0]):
		# edit distance



a = {
		"hello": "world",
		"airplane": "fuel", 
		"rocket": "fuel2", 
		"car": "electricity", 
		"boat": "propeller"
	}

term = "boat"
findmatch(term, a)