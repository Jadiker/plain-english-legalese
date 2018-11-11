import requests
import os.path
import time
from bs4 import BeautifulSoup

def scrapePlainDefs():
    # Get simple definitions from this site
    dataLink = "https://www.rocketlawyer.com/legal-dictionary.rl"
    try:
        page = requests.get(dataLink)
    except requests.exceptions.RequestException as e:
        raise

    soup = BeautifulSoup(page.content, 'html.parser')

    # Find the 'p' tags which correspond to valid letters
    allLetters = soup.find_all('p')
    numLetters = len(allLetters)
    validLetterIndices = []
    for i in range(numLetters):
        if('id' in soup.find_all('p')[i].attrs):
            validLetterIndices.append(i)

    allLetters = [allLetters[i] for i in validLetterIndices]

    # Find words and definitions
    wordDict = {}
    for i in range(len(allLetters)):
        # Names are in 'a' tags
        nameTags = allLetters[i].find_all("a")
        # Definitions are siblings of 'strong' tags
        defs = allLetters[i].find_all("strong")
        if(len(defs) == 0):
            continue
        for j in range(len(nameTags)):
            word = nameTags[j].get('name')
            definition = defs[j].next_sibling[2:] # Removes colon before def
            wordDict[word] = [definition]

    # Write dictionary to file
    if(not os.path.exists('easyDict.txt')):
        f = open("easyDict.txt", "x")
    f = open("easyDict.txt", "w")

    for i in wordDict:
        f.write(i + "\n")
        try:
            f.write(wordDict[i][0] + "\n")
        except UnicodeEncodeError:
            continue
        f.write("\n")

    # Return dictionary
    return wordDict
