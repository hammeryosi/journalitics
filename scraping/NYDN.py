import requests
from bs4 import BeautifulSoup
import re


class scraper:
    def __init__(self):
        self.baseURL = 'http://www.nydailynews.com/archives?pdate='

    def parseElement(self, el):
        title = el.text
        link = el.a['href']
        journal = 'NYDN'
        author = ''
        section = ''
        summary = ''
        try:
            page = requests.get(link).text
            soup = BeautifulSoup(page, 'html.parser')
            section = soup.find(class_='on')
            if section is not None:
                section = section.text
            byline =soup.find(class_='ra-byline')
            if byline is not None:
                author = ' and '.join([a.text for a in byline.find_all(rel='author')])
            pars = soup.find_all('p')
            n = min(2, len(pars))
            summary = ' '.join([p.text for p in pars[:n]])
            summary = re.sub('\n', ' ', summary)
            summary = re.sub('\r', '', summary)
            summary = re.sub('\t', '', summary)
            summary = re.sub('^ ', '', summary)
        except:
            pass
        return {'title': title,
                'link': link,
                'section': section,
                'author': author,
                'journal': journal,
                'summary': summary}


    def getTitles(self, date):
        url = self.baseURL + ''.join(date.split('-'))
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        els = ([el for el in
                soup.find(class_='the-week left').find_all('dd')
                if el.text[0] != ' ']
               +
               [el for el in
                soup.find(class_='the-week right').find_all('dd')
                if el.text[0] != ' '])
        print(date + ': ' + str(len(els)) + ' articles')
        headlines = [self.parseElement(el) for el in els]
        for h in headlines:
            h['date'] = date
        return headlines