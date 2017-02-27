import requests
from bs4 import BeautifulSoup
import re

class scraper:
    def __init__(self):
        self.baseURL = 'http://www.wsj.com/public/page/archive'

    def parseElement(self, el):
        journal = 'WSJ'
        title = el.h2.text
        summary = el.p.text
        summary = re.sub('  *', ' ', re.sub('\n ', '', summary))
        summary = re.sub('^ ', '', summary)
        link = el.h2.a['href']
        page = requests.get(link).text
        soup = BeautifulSoup(page, 'lxml')
        byline = soup.find(class_='byline')
        if byline is None:
            author = ''
        else:
            names = byline.find_all(itemprop='name')
            if names is not None:
                author = ' and '.join([n.text for n in names])
            else:
                author = re.sub('\n', '', byline.text)
        cat = soup.find(class_='category')
        if cat is not None:
            As = cat.find_all('a')
            section = ','.join([a.text for a in As])
            section = re.sub('\n', '', section)
            section = re.sub('  +', '', section)
        else:
            section = ''
        return {'link': link, 'title': title, 'author': author,
                'section': section, 'summary': summary,
                'journal': journal}

    def getTitles(self, date):
        # date format: yyyy-mm-dd
        headLines = []
        url = self.baseURL + '-' + date + '.html'
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        els = [l for l in soup.find(class_='newsItem').find_all('li')]
        print(date + ': ' + str(len(els)) + ' articles')
        for el in els:
            headLine = self.parseElement(el)
            headLine['date'] = date
            headLines.append(headLine)
        return headLines
