from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')
import pandas as pd
from functools import reduce
import sys
args = sys.argv

def keywordsInSen(sen):
    return [(m['text'], m['ner'])
            for m in sen['entitymentions']]


def keywordsInTxt(txt):
    an = nlp.annotate(txt, properties={
        'annotators': 'entitymentions',
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

src = args[1]
target = args[2]
headlinesData = pd.read_csv(src)
resultTable = extractFromHeadlines(headlinesData)
allData = pd.concat([headlinesData, resultTable], axis=1)
allData.to_csv(target, index=False, encoding='utf8')
