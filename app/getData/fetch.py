from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:pesco6@localhost:5432/journalitics')
import pandas as pd
from functools import reduce

def shorten(st):
    sp = st.split()
    l = len(sp)
    if l > 2:
        return ' '.join([sp[0]] + [n[0] + '.' for n in sp[1:l-1]] + [sp[l-1]])
    else:
        return st

def getTopNameCount(startDate, endDate):
    keep = 20
    data = pd.read_sql_query("select * from name_counts "+
                             "where date between '" + startDate + "' and '" +
                             endDate + "'", engine)

    def getNameCount(n, j, g):
        if (j, n) in g.keys():
            return int(sum(data['count'][groups[(j, n)]]))
        else:
            return 0

    jours = [str(j) for j in pd.unique(data['journal'])]
    groups = data.groupby(['journal', 'name']).groups
    journalCounts = []
    for j in jours:
        res = {}
        res['journal'] = j
        jGroups = [g for g in groups.keys() if g[0] == j]
        nameCount = [(g[1], sum(data['count'][groups[g]])) for g in jGroups]
        nameCount = sorted(nameCount, key=lambda x: x[1], reverse=True)[:keep]
        res = [{'name': shorten(x[0]), 'count': int(x[1])} for x in nameCount]
        journalCounts.append(res)
    groups2 = data.groupby('name').groups
    topNames = [x[0] for x in sorted(
                [(g, sum(data['count'][groups2[g]])) for g in groups2.keys()],
                key=lambda x: x[1], reverse=True)[:keep]]
    print(type(jours))
    compare = []
    for n in topNames:
        for j in jours:
            c = getNameCount(n,j,groups)
            compare.append(
                {'name': shorten(n), 'journal': j, 'count': c,
                 'rel': c / journalCounts[jours.index(j)][0]['count']}
            )
    return {"journals": jours, "journalCounts": journalCounts,
            'compare': compare}

#def getCountByName(name, startDate, endDate):
