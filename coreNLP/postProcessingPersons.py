# a script to generate the most common persons form
# the coreNLP extractions

import pandas as pd

# minimal number of appearances to be included in
# the name list
cutoff = 5

def makeCount(col):
    s = {}
    for st in rawTable['persons_raw']:
        if not pd.isnull(st):
            for n in st.split(','):
                if n in s.keys():
                    s[n] += 1
                else:
                    s[n] = 1
    return s

def partialNames(nameCount):
    parNames = {}
    for n in nameCount.keys():
        parts = n.split()
        l = len(parts)
        # general partial names
        if l > 1:
            for i in range(l):
                for j in range(i+1,l+1):
                    p = ' '.join(parts[i:j])
                    if p in nameCount.keys() and p != n:
                        if p in parNames.keys():
                            parNames[p].add(n)
                        else:
                            parNames[p] = set([n])
                    # for middle names
                    if l > 2:
                        p = ' '.join([parts[0], parts[l-1]])
                        if p in nameCount.keys() and p != n:
                            if p in parNames.keys():
                                parNames[p].add(n)
                            else:
                                parNames[p] = set([n])
    for p in parNames.keys():
        parNames[p] = sorted(list(parNames[p]), key=lambda x: nameCount[x], reverse=True)
    return parNames


def makeConvertDic(parNames):
    convert = {}
    for n in parNames.keys():
        if len(n.split()) == 1:
            mostCom = parNames[n][0].split()
            # ignore first names
            if mostCom[0] == n:
                convert[n] = None
            # convert last names to most common full name
            if  mostCom[len(mostCom)-1] == n:
                convert[n] = ' '.join(mostCom)
        # reduce long names to two words
        if len(n.split()) > 1:
            for long in parNames[n]:
                convert[long] = n
    return convert

def reduceCount(nameCount, parNames, convert):
    reducedNameCount = {}
    for n in nameCount.keys():
        if n in convert.keys():
            if convert[n] in reducedNameCount.keys():
                reducedNameCount[convert[n]] += nameCount[n]
            else:
                if convert[n] is not None:
                    reducedNameCount[convert[n]] = nameCount[n]
        else:
            reducedNameCount[n] = nameCount[n]
    return(reducedNameCount)

def makeCommonNameCol(col, convert, common):
    newCol = []
    for st in col:
        if not pd.isnull(st):
            oldNames = st.split(',')
            newNames = []
            for n in oldNames:
                if n in convert.keys():
                    n1 = convert[n]
                else:
                    n1 = n
                if n1 in common:
                    newNames.append(n1)
            newCol.append(','.join(set(newNames)))
        else:
            newCol.append('')
    return newCol

def nameCounts(table):
    entries = []
    g = table.groupby(['date', 'journal'])
    for p in g.groups.keys():
        nameCol = table.loc[g.groups[p],'common_names']
        names = set()
        for st in nameCol:
            if not pd.isnull(st):
                names.update([n for n in st.split(',')])
        names.remove('')
        entries += [{'date': p[0],
                     'journal': p[1],
                     'name': n,
                     'count': sum(
                         nameCol.apply(
                         lambda x: not pd.isnull(x)
                            and n in x))}
                         for n in names]
    return pd.DataFrame(entries)

rawTable = pd.read_csv('../data/nlpRaw.csv')
nameCount = makeCount(rawTable['persons_raw'])
parNames = partialNames(nameCount)
print('coreNLP found ' + str(len(nameCount)) +
      ' unique names')
convert = makeConvertDic(parNames)
reducedCount = reduceCount(nameCount, parNames,
                           convert)
print('reduced to ' + str(len(reducedCount)) +
      ' after searching partial names')
commonNames = pd.DataFrame.from_dict(reducedCount,
                                orient='index')
commonNames.columns = ['count']
commonNames = commonNames[commonNames['count'] > cutoff]
commonNames = commonNames.sort_values(by='count',
                            ascending=False)
print('after cutoff ' + str(len(commonNames)) + ' left')
print('single word names remaining: ' +
      str(sum([len(x.split()) == 1
               for x in commonNames.index])))
print('removing them..')
commonNames = commonNames[[len(x.split()) > 1
                 for x in commonNames.index]]
commonNames.to_csv('../data/commonNames.csv',
              encoding='utf8')

rawTable['common_names'] = (
    makeCommonNameCol(rawTable['persons_raw'],
                      convert,
                      commonNames.index))
rawTable.to_csv('../data/headlinesFull.csv', index=False,
                encoding='utf8')

countTable = nameCounts(rawTable)
countTable.to_csv('../data/nameCounts.csv',
                  index=False, encoding='utf8')





