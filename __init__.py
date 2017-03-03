from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')
from functools import reduce
import pandas as pd

def keywordsInSen(sen):
    words = [(t['lemma'], t['index'], t['ner']) for t in sen['tokens']
           if t['ner'] != 'O']
    reducedWords = []
    if len(words) == 0:
        return []
    parWord = words[0]
    if len(words) > 1:
        for w in words[1:]:
            if w[1] == parWord[1] + 1 and w[2] == parWord[2]:
                parWord = (parWord[0] + ' ' + w[0], parWord[1] + 1, parWord[2])
            else:
                reducedWords.append((parWord[0], parWord[2]))
                parWord = w
        reducedWords.append((parWord[0], parWord[2]))
    return reducedWords

def keywordsInTxt(txt):
    an = nlp.annotate(txt, properties={
      'annotators': 'ner',
      'outputFormat': 'json'
      })
    wordLists = [keywordsInSen(s) for s in an['sentences']]
    return set(reduce(lambda x, y: x + y, wordLists))

def extractFromHeadlines(headlineTable):

