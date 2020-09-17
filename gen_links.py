import json

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame


if __name__ == "__main__":
    # scraper = CnetWebscraper({
    #     # 'topics': 
    # })

    topics = {
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

    review_links = set()

    for cat, page in topics.items():
        category = requests.get(page)
        category_soup = BeautifulSoup(category.content, 'html.parser')
        results = category_soup.find('div', class_='items')
        reviews = results.find_all('a', section='review-hed')
        review_links.update(['https://www.cnet.com' + rev.get('href') + '#comments' for rev in reviews])


    count = 0
    products = []
    for review_url in review_links:
        soup = BeautifulSoup(requests.get(review_url).content, 'html.parser')
        schema = json.loads(soup.findAll('script', {'type':"application/ld+json"})[0].string)

        if schema and schema['@type'] == 'Product':
            count = count + 1

            products.append({
                'name': schema['model'],
                'category': schema['category'],
                'cnet_url_check': review_url,
            })

    
    product_df = DataFrame(products, columns=['name', 'category', 'cnet_url_check'])
    product_df.to_csv('product_list.csv', index=False)
            

    
    
    print(review_links, count)