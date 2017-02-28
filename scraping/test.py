from NYP import scraper
import json
sc = scraper()
headlines = sc.getTitles('2016-01-01')
f = open('testResults.js', 'w')
json.dump(headlines, f)
f.close()