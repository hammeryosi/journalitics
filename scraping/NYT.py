# scraper for the New York Times

from bs4 import BeautifulSoup
from math import ceil
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
chromedriver = "c:/Users/yosi/Downloads/chromedriver_win32/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
import datetime

class scraper:
    def __init__(self):
        self.baseURL = 'https://query.nytimes.com/search/sitesearch/#/*/from'
        self.driver = webdriver.Chrome(chromedriver)

    def parseElement(self, el):
        journal = 'NYT'
        link = el.find('h3').a['href']
        title = el.find('h3').text
        author = el.find(class_='byline').text[3:]
        section = el.find(class_='section').text
        summary = el.find(class_='summary').text
        date = datetime.datetime.strptime(el.find(class_='dateline').text,
                                          '%B %d, %Y')
        date = date.strftime('%Y-%m-%d')
        return {'link': link, 'title': title, 'author': author,
                'section': section, 'summary': summary, 'date': date,
                'journal': journal}

    def getTitles(self, date):
        # date format: yyyy-mm-dd
        headLines = []
        d1 = ''.join(date.split('-'))
        url = self.baseURL + d1 + 'to' + d1 + '/document_type%3A%22article%22'
        self.driver.get(url)
        try:
            wait = WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(
                (By.ID, 'totalResultsCount'), 'about'))
            resultsInDay = int(self.driver.find_element_by_id('totalResultsCount').text.split()[3])
            print(date + ': ' + str(resultsInDay) + ' results')
        except:
            print(date + ': no results')
            return []
        pages = int(ceil(resultsInDay / 10))
        for p in range(pages):
            url = (self.baseURL + d1 + 'to' + d1 +
                   '/document_type%3A%22article%22/' + str(p + 1))
            self.driver.get(url)
            try:
                wait = WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'story'), '.'))
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                stories = soup.find_all(class_='story') + soup.find_all(class_='story noThumbs')
                pageTitles = [self.parseElement(s) for s in stories if s.h3.text[:11] != 'Paid Notice']
            except:
                pageTitles = []
                pass
            headLines += pageTitles
            print('page ' + str(p + 1) + ': ' + str(len(pageTitles)) + ' headlines')
        print(date + ': ' + str(len(headLines)) + ' articles')
        return headLines
