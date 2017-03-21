import datetime
import pandas as pd
from NYT import scraper as NYTsc
from WSJ import scraper as WSJsc
from NYDN import scraper as NYDNsc
from NYP import  scraper as NYPsc
from LAT import  scraper as LATsc
from ND import scraper as NDsc


scrapers = {'NYT': NYTsc,
            'WSJ': WSJsc,
            'NYDN': NYDNsc,
            'NYP': NYPsc,
            'LAT': LATsc,
            'ND': NDsc}

def nextDay(date):
    d = [int(n) for n in date.split('-')]
    return format(datetime.date(d[0], d[1], d[2]) +
                  datetime.timedelta(days=1),
                  '%Y-%m-%d')

retryTime = 3

def headLinesInRange(startDate, endDate, journal,
                     saveEvery = 1,
                     saveTo = 'titlesScraped.csv'):
    scraper = scrapers[journal]()
    d = startDate
    stop = nextDay(endDate)
    headLines = []
    count = 0
    while d != stop:
        headLines += scraper.getTitles(d)
        count += 1
        d = nextDay(d)
        if count % saveEvery == 0:
            pd.DataFrame(headLines).to_csv(saveTo,
                                           encoding='utf8',
                                           index=False)
    dat = pd.DataFrame(headLines)
    dat.to_csv(saveTo, encoding='utf8')
    print('done! scraped ' + str(len(headLines)) +
          ' headlines')
    return dat

