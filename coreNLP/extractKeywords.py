from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')
import pandas as pd
from functools import reduce

headlinesData = pd.read_csv('../data/headlines.csv')


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
    keywords = set(reduce(lambda x, y: x + y, wordLists))
    persons = ','.join([k[0] for k in keywords if k[1] == 'PERSON'])
    locations = ','.join([k[0] for k in keywords if k[1] == 'LOCATION'])
    organizations = ','.join([k[0] for k in keywords if k[1] == 'ORGANIZATION'])
    return {'persons_raw': persons,
            'locations_raw': locations,
            'organizations_raw': organizations}

def keywordsInRow(tableRow):
    title = tableRow['title']
    summary = tableRow['summary']
    if not pd.isnull(summary):
        text = title + ' ' + summary
    else:
        text = title
    return keywordsInTxt(text)


def extractFromHeadlines(headlineTable):
    print('extracting named entities from headline text using coreNLP:')
    l = len(headlineTable)
    keywords = []
    batchSize = 10000
    done = 0
    while done < l:
        keywords += [keywordsInRow(headlineTable.iloc[i,:])
                     for i in range(done, min(done + batchSize, l))]
        print(str(len(keywords)) + ' of ' + str(l) + ' done')
        done += batchSize
    return pd.DataFrame(keywords)

resultTable = extractFromHeadlines(headlinesData)
allData = pd.concat([headlinesData, resultTable], axis=1)
allData.to_csv('resultTable.csv', index = False)
