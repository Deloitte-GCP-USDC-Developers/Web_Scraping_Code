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

class CnetWebscraper(CsvProductLoader, GoogleReviewFinderWebscraper, Webscraper):

    SEARCH_URL = 'https://www.cnet.com/search/xhr/?query={query}&rpp=30&sort=1#&typeName=content_review'

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
            result_json = json.loads(requests.get(cls.SEARCH_URL.format(query = name)).content)
            soup = BeautifulSoup(result_json['result']['html'], 'html.parser')
            results = [ { 
                'name': product.find('h3').text,
                'url': 'https://www.cnet.com' + product.findChild('a')['href'] + '#comments',
                'distance': jellyfish.jaro_winkler_similarity(name, product.find('h3').text)
            } for product in soup.find_all('div', class_='itemInfo')]
            

            max_distance = -1
            sum_distance = 0
            max_product = None
            for product in results:
                if product['distance'] > max_distance:
                    max_distance = product['distance']
                    max_product = product
                sum_distance = sum_distance + product['distance']
                
            urls.append(max_product['url'])
            if check_url == max_product['url']:
                n_match = n_match + 1
                matches.append(max_product['distance'])
            else:
                not_matches.append(max_product['distance'])
        
        return urls

    PRODUCT_NAME_LABEL = 'model'
    @staticmethod
    def getProductPage(url):
        return CnetWebscraperReviewPage(url)

class CnetWebscraperReviewPage(SchemaWebscraperReviewPage):
    pass

if __name__ == "__main__":
    scraper = CnetWebscraper({})
    print(scraper)

    upload_to_gbucket(scraper.result_filename, '/tmp/')