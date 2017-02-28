import requests
from bs4 import BeautifulSoup

class scraper:
    def __init__(self):
        self.baseURL = 'http://pqasb.pqarchiver.com'

     def dateUrl(date):
        y, m, d = date.split('-')
        return (baseUrl +
                '/nypost/results.html?st=advanced&QryTxt=*&datetype=6' +
                '&frommonth=' + m + '&fromday=' + d + '&fromyear=' + y +
                '&tomonth=' + m + '&today=' + d + '&toyear=' + y)


