# import sys
# import subprocess

# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bs4'])
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])

import requests
from bs4 import BeautifulSoup
import pandas
import os


topics = {'Drones':'https://www.cnet.com/topics/drones/products/', 'Headphones':'https://www.cnet.com/topics/headphones/products/', 'Laptops':'https://www.cnet.com/topics/laptops/products/', 'Monitors': 'https://www.cnet.com/topics/monitors/products/', 'Phones':'https://www.cnet.com/topics/phones/products/', 'Printers':'https://www.cnet.com/topics/printers/products/', 'Speakers':'https://www.cnet.com/topics/speakers/', 'Tablets':'https://www.cnet.com/topics/tablets/products/', 'TVs': 'https://www.cnet.com/topics/tvs/products/'}

for cat, page in topics.items():
    cnet_df = pandas.DataFrame()
    category = requests.get(page)
    category_soup = BeautifulSoup(category.content, 'html.parser')
    
    results = category_soup.find('div', class_='items')
    reviews = results.find_all('a', section='review-hed')
    review_links = [rev.get('href') for rev in reviews]
    
    for link in review_links:
        review = 'https://www.cnet.com' + link
        review_page = requests.get(review)
        review_soup = BeautifulSoup(review_page.content, 'html.parser')
        
        if(review_soup.find('div', class_='c-metaCard_rating') is None):
            if(review_soup.find('div', class_='col-1 overall') is None):
                rating = 'N/A'
            else:
                rating = review_soup.find('span', class_='text').text.split()[0]
        else:
            rating = review_soup.find('div', class_='c-metaCard_rating').text.strip()
        
        if(review_soup.find('div', section='review-body') is None):
            if(review_soup.find('div', id='editorReview') is None):
                continue
            else: 
                body = review_soup.find('div', id='editorReview').find_all('p')
        else: 
            body = review_soup.find('div', section='review-body').find_all('p')

        review_text = ''
        for part in body:
            review_text += str(part.text.encode('utf-8'))
    
        title = review_soup.find('h1').text
        
        if(review_soup.find('a', class_='author') is None):
            if(review_soup.find('a', rel='author') is None):
                continue
            else:
                author = review_soup.find('a', rel='author').text
        else:
            author = review_soup.find('a', class_='author').text
        
        date = review_soup.find('time').text.strip()
        
        if(review_soup.find('h2', class_='c-metaCard_prodName') is None):
            if(review_soup.find('span', class_='itemreviewed') is None):
                continue
            else:
                product = review_soup.find('span', class_='itemreviewed').text.split('review:')[0].strip()
        else:
            product = review_soup.find('h2', class_='c-metaCard_prodName').text

        data = {'Product Name': [product.encode('utf-8')], 'Product Category':[cat.title().encode('utf-8')], 'Review Source':['CNET'], 'Review Headline':[title.encode('utf-8')], 'Review Text':[review_text], 'Review Rating':[rating], 'Review Author':[author.encode('utf-8')], 'Review Date':[date]}

        df = pandas.DataFrame(data)
        cnet_df = cnet_df.append(df)
        
    cnet_df = pandas.DataFrame.drop_duplicates(cnet_df)  
    cnet_df = cnet_df.reset_index(drop=True)
    csv_name = 'cnet_reviews_' + cat.lower() + '.csv'
    cnet_df.to_csv(csv_name, index=False)

    path = csv_name
    # command = 'gsutil cp %s gs://dlt-sntmnt-source-file-web-scraping' % path
    # os.system(command)
