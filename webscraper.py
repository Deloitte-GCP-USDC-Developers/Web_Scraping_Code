from abc import ABC, abstractmethod
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

class Webscraper(ABC):

    @classmethod
    @abstractmethod
    def getProductUrls(cls, params):
        pass
    
    @classmethod
    def getProductPageWithErrorChecking(cls, url):
        try:
            return cls.getProductPage(url)
        except SkipPageException:
            print('Skipped', url)

    @classmethod
    @abstractmethod
    def getProductPage(cls, url):
        pass
    
    headers = [
        'Product Name',
        'Product Category',
        'Review Source',
        'Review Headline',
        'Review Text',
        'Review Author',
        'Review Rating',
        'Review Date'
    ]
    reviews = None
    def getAllProductPages(self, params):
        products = []
        for url in self.getProductUrls(params):
            page = self.getProductPageWithErrorChecking(url)
            if page:
                products.append({
                    'Product Name': page.product['name'],
                    'Product Category': page.product['category'],
                    'Review Source': page.review['source'],
                    'Review Headline': page.review['headline'],
                    'Review Text': page.review['text'],
                    'Review Author': page.review['author'],
                    'Review Rating': page.review['rating'],
                    'Review Date': page.review['date']
                })
        self.reviews = DataFrame(products, columns=self.headers)
    
    def getSaveFileName(self):
        return 'reviews_' + datetime.now().astimezone().isoformat() + '.csv'

    def saveCsv(self):
        return self.reviews.to_csv(self.getSaveFileName(), index=False)
            
    def __init__(self, params):
        self.getAllProductPages(params)
        self.saveCsv()


class WebscraperReviewPage(ABC):
    url = ''
    request = None
    soup = None
    product = {
        'name': '',
        'category': ''
    }
    
    review = {
        'source': '',
        'headline': '',
        'text': '',
        'rating': -1, # Out of 100
        'author': '',
        'date': ''
    }
    def __init__(self, url):
        self.url = url
        self.request = requests.get(url)
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.populateFields()

    @property
    def content(self):
        return self.request.content if self.request else None

    def populateFields(self):
        self.product = self.getProductInfo()
        self.review = self.getReviewInfo()

    @abstractmethod
    def getProductInfo(self):
        pass

    @abstractmethod
    def getReviewInfo(self):
        pass

class SkipPageException(Exception):
    pass