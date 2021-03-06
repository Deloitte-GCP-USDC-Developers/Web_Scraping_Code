import json

import requests
from bs4 import BeautifulSoup
import pandas
import jellyfish

from webscraper import Webscraper, WebscraperReviewPage
from schema_webscraper import SchemaWebscraperReviewPage
from google_review_finder_webscraper import GoogleReviewFinderWebscraper
from csv_product_loader import CsvProductLoader
from utils import upload_to_gbucket, get_closest_match

class EngadgetWebscraper(CsvProductLoader, GoogleReviewFinderWebscraper, Webscraper):

    SEARCH_URL = 'https://search.engadget.com/search?p={query}&ei=UTF-8&cat=review&fr2=sortBy'
    PRODUCTNAME_CSVFILE = 'product_list.csv'
    @classmethod
    def getProductUrls(cls, params):
        names = cls.loadProductNames()
        check_urls = cls.loadProductDefaultUrls()
        urls = []

        matches = []
        n_match = 0
        not_matches = []
        for name, check_url in zip(names, check_urls):
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            result_html = requests.get(cls.SEARCH_URL.format(query = name), headers).content
            soup = BeautifulSoup(result_html, 'html.parser')
            results = [ { 
                'name': product.find('h4').text,
                'url': product.findChild('a')['href'],
                'distance': jellyfish.jaro_winkler_similarity(name, product.find('h4').text)
            } for product in soup.find_all('li', class_='ov-a')]
            
            if name =='Sennheiser Momentum True Wireless 2':
                print(cls.SEARCH_URL.format(query = name), soup)

            max_distance = -1
            sum_distance = 0
            max_product = None
            for product in results:
                if product['distance'] > max_distance:
                    max_distance = product['distance']
                    max_product = product
                sum_distance = sum_distance + product['distance']
            
            if max_product:
                urls.append(max_product['url'])
        
        return urls
        
    @staticmethod
    def getProductPage(url):
        return EngadgetWebscraperReviewPage(url)

class EngadgetWebscraperReviewPage(SchemaWebscraperReviewPage):
    def loadSchema(self, html):
        json = super().loadSchema(html)
        if json['@type'] == 'Review':
            json = json['itemReviewed']
        return json

if __name__ == "__main__":
    scraper = EngadgetWebscraper({})
    print(scraper)

    upload_to_gbucket(scraper.result_filename, '/tmp/')