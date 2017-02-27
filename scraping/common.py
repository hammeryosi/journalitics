import datetime
import pandas as pd
from .NYT import scraper as NYTsc
from .WSJ import scraper as WSJsc
from .NYDN import scraper as NYDNsc


scrapers = {'NYT': NYTsc,
            'WSJ': WSJsc,
            'NYDN': NYDNsc}

def nextDay(date):
    d = [int(n) for n in date.split('-')]
    return format(datetime.date(d[0], d[1], d[2]) +
                  datetime.timedelta(days=1),
                  '%Y-%m-%d')

def headLinesInRange(startDate, endDate, journal, saveEvery = 30,
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
            pd.DataFrame(headLines).to_csv(saveTo, encoding='utf8')
    dat = pd.DataFrame(headLines)
    dat.to_csv(saveTo, encoding='utf8')
    print('done! scraped ' + str(len(headLines)) + ' headlines')
    return dat

