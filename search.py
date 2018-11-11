
# Finds a definition in law dict closest to input term
# Returns tuple of lists (plain def, legal def)
# If edit distance > 2, then returns -1 and the closest term found or a tuple of empty lists
def searchterm(term, lawdict):
	if term in lawdict.keys():
		return lawdict[term]
	else:
		keyList = lawdict.keys()
		#editList = map(lambda x, y: levenshteinDistance(x, y), keyList, term)
		editList = [levenshteinDistance(val, term) for val in lawdict.keys()]

	if(min(editList) > 2 and min(editList) < 4):
		return ([-1], [lawdict[list(keyList)[editList.index(min(editList))]]])
	elif(min(editList) > 4):
		return ([-1], [])
	else:
		return lawdict[list(keyList)[editList.index(min(editList))]]


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

