import requests
import os.path
import time
from bs4 import BeautifulSoup

def scrapeLegalDefs():
    def closed_range(start, stop, step=1):
      dir = 1 if (step > 0) else -1
      return range(start, stop + dir, step)

    # Dictionary of words
    wordDict = {}

    # Num of words to search
    numWords = 1000
    # Index to start (low indices have no words)
    cntStart = 2000
    # Link to scrape data from
    dataLink = "https://dictionary.law.com/Default.aspx?selected=NUM"

    # Scrape up to 'numWords' words
    for i in closed_range(cntStart, cntStart + numWords):
        #start = time.time()
        currDataLink = dataLink.replace('NUM', str(i))
        # Page with word definition
        try:
            page = requests.get(currDataLink)
        except requests.exceptions.RequestException as e:
            continue

        # Parse HTML and find word and definition
        soup = BeautifulSoup(page.content, 'html.parser')

        word = soup.find_all('span', {'class': 'definedword'})
        if(len(word) == 0):
            continue
        word = word[0].get_text()
        definition = soup.find_all('p', {'class': 'text'})
        definition = definition[0].get_text()

        wordDict[word] = [definition]
        #end = time.time()
        #print(end - start)
    # Write data to file for testing
    if(not os.path.exists('dictionary.txt')):
        f = open("dictionary.txt", "x")
    f = open("dictionary.txt", "w")
    for i in wordDict:
        f.write(i + "\n")
        f.write(wordDict[i][0] + "\n")
        f.write("\n")

    # Return dictionary
    return wordDict



