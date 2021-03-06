# a script to generate the most common persons form
# the coreNLP extractions

import pandas as pd

# minimal number of appearances to be included in
# the name list
cutoff = 5

singleWordNames = set(["rihanna", "prince", "beyoncé", "madonna", "banksy",
                       "rembrandt", "buddha", "debussy", "molière", "plato",
                       "shakespeare", "lorde", "gandhi"])
excludeNames = set(["boko haram", "charlie hebdo", " "])
manualConverts = {'jay-z': 'jay z', 'jesus': 'jesus christ', "beyonce": "beyoncé"}

def makeCount(col):
    s = {}
    for st in rawTable['persons_raw']:
        if not pd.isnull(st):
            for n in st.split(','):
                n = n.lower()
                if n in s.keys():
                    s[n] += 1
                else:
                    s[n] = 1
    return s


# trying to fix coreNLP mistakes
def convertDic(nameCount):
    convert = {}
    for n in nameCount.keys():
        # check all parts of multi-word names
        n = n.lower()
        words = n.split()
        l = len(words)
        parts = []
        if l>1:
            for i in range(l):
                for j in range(i+1, l+1):
                    part = ' '.join(words[i:j])
                    if part != n:
                        parts.append(part)
                    if j-i > 1 and j < l:
                        parts.append(words[i] +
                                     ' ' + words[j])
            for part in parts:
                if part in nameCount.keys():
                    if (nameCount[part] > nameCount[n] and
                            (len(part.split()) > 1 or
                            part in singleWordNames)):
                        # part is more common than whole
                        # name
                        if n in convert.keys():
                            convert[n].add(part)
                        else:
                            convert[n] = set([part])
                    elif (nameCount[n] > nameCount[part] and
                            part != words[0] and
                            words[l-1] not in ['jr.', 'junior']):
                        # whole name is more common than part
                        # and part is not a first name
                        # and last word in full name is not Jr.
                        if part in convert.keys():
                            if (max([nameCount[x] for x in convert[part]]) >
                                    nameCount[n]):
                                convert[part] = set([n])
                        else:
                            convert[part] = set([n])
    return convert




def reduceCount(nameCount, convert):
    reducedNameCount = {}
    for n in nameCount.keys():
        if n in convert.keys():
            for n1 in convert[n]:
                if n1 in reducedNameCount.keys():
                    reducedNameCount[n1] += nameCount[n]
                else:
                    reducedNameCount[n1] = nameCount[n]
        elif (#(len(n.split()) > 1 or n in singleWordNames) and
                n not in excludeNames):
            reducedNameCount[n] = nameCount[n]
    return(reducedNameCount)

def makeCommonNameCol(col, convert, common):
    newCol = []
    for st in col:
        if not pd.isnull(st):
            st = st.lower()
            oldNames = st.split(',')
            newNames = []
            for n in oldNames:
                if n in convert.keys():
                    for n1 in convert[n]:
                        if n1 in common:
                            newNames.append(n1)
                elif n in common:
                    newNames.append(n)
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

rawTable = pd.read_csv('../data/headlines2012-2016NLPRaw.csv')
nameCount = makeCount(rawTable['persons_raw'])
print('coreNLP found ' + str(len(nameCount)) +
      ' unique names')
convert = convertDic(nameCount)
convert.update(manualConverts)
reducedCount = reduceCount(nameCount, convert)
convert = convertDic(reducedCount)
reducedCount = reduceCount(reducedCount, convert)
print('reduced to ' + str(len(reducedCount)) +
      ' after searching partial names')
commonNames = pd.DataFrame.from_dict(reducedCount,
                                orient='index')
commonNames.columns = ['count']
commonNames = commonNames[commonNames['count'] > cutoff]
commonNames = commonNames.sort_values(by='count',
                            ascending=False)
print('after cutoff ' + str(len(commonNames)) + ' left')
remainingSingle = [x for x in commonNames.index
       if len(x.split()) == 1 and x not in singleWordNames]
print('single word names remaining: ' +
      str(len(remainingSingle)))
print(remainingSingle)
print('removing them..')
mask = commonNames.index.isin(remainingSingle)
commonNames = commonNames[~mask]
commonNames.to_csv('../data/commonNames.csv',
              encoding='utf8')

rawTable['common_names'] = (
    makeCommonNameCol(rawTable['persons_raw'],
                      convert,
                      commonNames.index))
rawTable.to_csv('../data/headlinesFull.csv', index=False,
                encoding='utf8')
print('making daily counts...')
countTable = nameCounts(rawTable)
countTable.to_csv('../data/nameCounts.csv',
                  index=False, encoding='utf8')
print('done!')





