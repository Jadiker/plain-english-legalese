from scrapeLegalDefs import *
from scrapePlainDefs import *
import copy
import pickle

# with open('combinedDict.pkl', 'rb') as input:
#     combinedDict = pickle.load(input)
#
# print(combinedDict)
def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

legalDefs = scrapeLegalDefs()
plainDefs = scrapePlainDefs()

# Combine legal and plain defs (words map to tuples of [plain, legal] )
combinedDict = {}

for key in plainDefs:
    combinedDict[key] = (plainDefs[key], [])

for key in legalDefs:
    if(key in combinedDict.keys()):
        combinedDict[key] = (combinedDict[key][0], legalDefs[key])
    else:
        combinedDict[key] = ([], legalDefs[key])

# Pickle combined dict
save_object(combinedDict, "combinedDict.pkl")

# Write dictionary to file
if(not os.path.exists('combinedDict.txt')):
    f = open("combinedDict.txt", "x")
f = open("combinedDict.txt", "w")

for i in combinedDict:
    f.write(i + "\n")
    try:
        if(len(combinedDict[i][0]) > 0):
            f.write(combinedDict[i][0][0])
        else:
            f.write("\n")
        if (len(combinedDict[i][1]) > 0):
            f.write(combinedDict[i][1][0])
        else:
            f.write("\n")
    except UnicodeEncodeError:
        continue

