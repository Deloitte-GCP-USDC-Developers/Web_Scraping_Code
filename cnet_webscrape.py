import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bs4'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])

import requests
from bs4 import BeautifulSoup
import pandas
import os

review = 'https://www.cnet.com/reviews/dell-xps-13-2020-review/'
review_page = requests.get(review)
review_soup = BeautifulSoup(review_page.content, 'html.parser')
results = review_soup.find(id='page-dell-xps-13-2020')

rating = results.find('div', class_='c-metaCard_rating')
body = results.find_all('p')

review_text = ''
for part in body:
    if(part.text == 'Be respectful, keep it civil and stay on topic. We delete comments that violate our policy, which we encourage you to read. Discussion threads can be closed at any time at our discretion.'):
        continue
    review_text += str(part.text.encode('utf-8'))
    
title = results.find('h1')
author = results.find('a', class_='author')
date = results.find('time')
category = results.find_all('a', class_='tag')
cats = [cat.text for cat in category]
product = results.find('h2', class_='c-metaCard_prodName')

data = {'Product Name': [product.text], 'Product Category':[cats[1]], 'Review Source':['CNET'], 'Review Headline':[title.text], 'Review Text':[review_text], 'Review Rating':[rating.text.strip()], 'Review Author':[author.text], 'Review Date':[date.text]}

df = pandas.DataFrame(data)
df.to_csv('cnet_reviews.csv', index=False)

path = 'cnet_reviews.csv'
command = 'gsutil cp %s gs://dlt-sntmnt-source-file-web-scraping' % path
os.system(command)
