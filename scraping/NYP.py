import requests
from bs4 import BeautifulSoup
import time
import re
from math import ceil

class scraper:
    def __init__(self):
        self.baseURL = 'http://pqasb.pqarchiver.com'
        self.waitTime = 30

    def dateUrl(self, date):
        y, m, d = date.split('-')
        return (self.baseURL +
                '/nypost/results.html?st=advanced&QryTxt=*&datetype=6' +
                '&frommonth=' + m + '&fromday=' + d + '&fromyear=' + y +
                '&tomonth=' + m + '&today=' + d + '&toyear=' + y)

    def fetchPage(self, url):
        success = False
        while not success:
            page = requests.get(url).text
            soup = BeautifulSoup(page, 'html.parser')
            if not (soup.title.text ==
                    '503 Service Temporarily Unavailable'):
                success = True
            else:
                print('Failed fetching page:\n'
                      + url + '\nRetrying in ' +
                      str(self.waitTime) + ' seconds..')
                time.sleep(self.waitTime)
        return soup

    def titlesInPage(self, soup, start):
        resultTable = soup.find(text=str(start) + '.').parent.parent.parent.parent
        trList = resultTable.findAll('tr')
        els = [trList[2 * i] for i in range(int(len(trList) / 2))]
        return els

    def parseElement(self, el):
        journal = 'NYP'
        link = self.baseURL + el.find_all('td')[1].a['href']
        soup = self.fetchPage(link)
        summary = soup.find(text=' (Document Summary)').next.next.text
        summary = re.sub('[\n|\t]', '', summary)
        title = soup.find(class_='docTitle').text
        authorAnchor = soup.find(lambda x: x.text == 'Author:')
        if authorAnchor is not None:
            author = authorAnchor.next.next.next.text
            author = ','.join([' '.join(reversed(x.split(', '))) for x in author.split('||||||')])
        else:
            author = ''
        section = soup.find(lambda x: x.text == 'Section:').next.next.next.text
        return {'link': link,
                'summary': summary,
                'title': title,
                'author': author,
                'section': section,
                'journal': journal}



    def getTitles(self, date):
        url = self.dateUrl(date)
        soup = self.fetchPage(url)
        if soup.find(text='No Articles Found') is not None:
            numOfResults = 0
        else:
            numOfResults = (
                int(soup.find(text=' to ').parent('b')[2].text))
        print(date + ': ' + str(numOfResults) + ' results')
        if numOfResults > 0:
            # titles from first page
            els = self.titlesInPage(soup, 1)
            headlines = [self.parseElement(el) for
                         el in els]
            print('page 1: ' + str(len(els)) + ' articles')
        else:
            headlines = []
        if numOfResults > 10:
            pages = int(ceil(numOfResults / 10.))
            for p in range(1,pages):
                start = p * 10
                pageUrl = url + '&start=' + str(start)
                soup = self.fetchPage(pageUrl)
                if soup.find(text='No Articles Found') is None:
                    els = self.titlesInPage(soup, start + 1)
                    headlines += [self.parseElement(el) for
                         el in els]
                    print('page ' + str(p + 1) +
                        ': ' + str(len(els)) + ' articles')
                else:
                    break
        for h in headlines:
            h['date'] = date
        return headlines




