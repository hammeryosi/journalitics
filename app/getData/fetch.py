from sqlalchemy import create_engine
#engine = create_engine('postgresql://postgres:pesco6@localhost:5432/journalitics')
engine = create_engine('postgresql://journalitics_app:Jour327@journalitics.ccteqcl24h7m.us-west-2.rds.amazonaws.com:5432/journalitics')
import pandas as pd

def shorten(st):
    sp = st.split()
    l = len(sp)
    if l > 2:
        return ' '.join([sp[0]] + [n[0] + '.' for n in sp[1:l-1]] + [sp[l-1]])
    else:
        return st

def getTopNameCount(startDate, endDate):
    q = ("select top_names.name, journal, sum(count) as count " +
         "from name_counts inner join " +
	        "(select name from " +
	        "name_counts where date between '" + startDate + "' and '" + endDate + "' " +
	        "group by name order by sum(count) desc " +
	        "limit 200) as top_names on (top_names.name=name_counts.name) " +
        "where date between '" + startDate + "' and '" + endDate + "' " +
        "group by top_names.name, journal " +
        "order by count desc, journal")
    keep = 20
    data = pd.read_sql_query(q, engine)
    data.loc[:,'name'] = data.loc[:,'name'].apply(lambda x: ' '.join([y.capitalize() for y in x.split()]))
    jours = [str(j) for j in pd.unique(data.loc[:,'journal'])]
    journalCounts = [data.loc[data['journal'] == j,('name', 'count')].sort_values(
        by='count',axis=0,ascending=False) for j in jours]
    journalCounts = [jc[:min(keep, len(j))] for jc in journalCounts]
    journalCountDics = [list(sorted(jc.T.to_dict().values(),
                                    key= lambda x: x['count'], reverse=True)) for jc in journalCounts]
    topNames = [str(x) for x in pd.unique(data['name'])]
    topNames = topNames[:min(keep, len(topNames))]
    jourMax = [max(data[data['journal'] == j]['count']) for j in jours]
    compare = data[data.loc[:,'name'].apply(lambda x: x in topNames)]
    compare.loc[:,'freq'] = compare.apply(lambda x: x['count'] / jourMax[jours.index(x['journal'])], 1)
    compare = list(compare.T.to_dict().values())
    return {"journals": jours, "journalCounts": journalCountDics,
            'compare': compare}

def getTopNames(startDate="2015-01-01", endDate="2016-12-31", n=100):
    q = ("select name from name_counts " +
         "where date between '" + startDate + "' and '" + endDate + "' " +
         "group by name " +
         "order by sum(count) desc " +
         "limit " + str(n))
    names = list(pd.read_sql_query(q, engine)['name'])
    names = [' '.join([x.capitalize() for x in n.split()])
             for n in names]
    return list(names)

def getCountsForNames(names, startDate, endDate):
    q = ("select * from name_counts where name in ('" +
         "','".join(names) + "') and date between '" + startDate +
         "' and '" + endDate + "'")
    data = pd.read_sql_query(q, engine)
