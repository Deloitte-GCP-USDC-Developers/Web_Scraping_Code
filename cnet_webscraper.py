import requests
from bs4 import BeautifulSoup
import pandas

from webscraper import Webscraper, WebscraperReviewPage
from schema_webscraper import SchemaWebscraperReviewPage

class CnetWebscraper(Webscraper):

    @staticmethod
    def getProductUrls(params):
        topics = params['topics']

        
        review_links = set()

        for cat, page in topics.items():
            cnet_df = pandas.DataFrame()
            category = requests.get(page)
            category_soup = BeautifulSoup(category.content, 'html.parser')
            results = category_soup.find('div', class_='items')
            reviews = results.find_all('a', section='review-hed')
            review_links.update(['https://www.cnet.com' + rev.get('href') + '#comments' for rev in reviews])

        return review_links

    @staticmethod
    def getProductPage(url):
        return CnetWebscraperReviewPage(url)

class CnetWebscraperReviewPage(SchemaWebscraperReviewPage):
    pass

if __name__ == "__main__":
    urls = CnetWebscraper.getProductUrls({
        'topics': {
            'Drones':'https://www.cnet.com/topics/drones/products/',
            'Headphones':'https://www.cnet.com/topics/headphones/products/',
            'Laptops':'https://www.cnet.com/topics/laptops/products/',
            'Monitors': 'https://www.cnet.com/topics/monitors/products/',
            'Phones':'https://www.cnet.com/topics/phones/products/',
            'Printers':'https://www.cnet.com/topics/printers/products/',
            'Speakers':'https://www.cnet.com/topics/speakers/',
            'Tablets':'https://www.cnet.com/topics/tablets/products/',
            'TVs': 'https://www.cnet.com/topics/tvs/products/'
        }
    })
    print(CnetWebscraperReviewPage(urls.pop()).review)