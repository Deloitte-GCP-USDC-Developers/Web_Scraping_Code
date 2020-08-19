from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

class Webscraper(ABC):

    @staticmethod
    @abstractmethod
    def getProductUrls(params):
        pass

    @staticmethod
    @abstractmethod
    def getProductPage(url):
        pass


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
        'author': ''
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
