from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

class GoogleReviewFinderWebscraper(ABC):

    GOOGLE_SEARCH_URL = 'https://www.google.com/search'

    SITE_URL = ''
    
    @classmethod
    def getProductUrls(cls, params):
        if 'product_name' in params:
            params['product_names'] = [params['product_name']]
        urls = []
        for product_name in params['product_names']:
            rq = requests.get(cls.GOOGLE_SEARCH_URL, {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36','q': product_name + ' site:' + cls.SITE_URL, 'client':'ubuntu', 'channel':'fs', 'ie':'utf-8', 'oe':'utf-8'})
            soup = BeautifulSoup(rq.content, 'html.parser')
            print(soup)
            new_url = 'https://google.com/' + soup.find('meta', {'http-equiv': 'refresh'})['content'][6:]
            rq = requests.get(new_url)
            soup = BeautifulSoup(rq.content, 'html.parser')
            results = [link['href'][7:].split('&')[0] for link in soup.find_all('a', href=lambda x: '/url' in x)]
            urls.append(results)
        return urls

if __name__ == "__main__":
    class GoogleReviewFinderWebscraperTest(GoogleReviewFinderWebscraper):
        SITE_URL = 'https://www.tutorialsteacher.com/python'
        
    print(GoogleReviewFinderWebscraperTest.getProductUrls({
        'product_name': 'property function'
    }))
        
