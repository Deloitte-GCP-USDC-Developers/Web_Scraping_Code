import json
from abc import ABC, abstractmethod

from webscraper import WebscraperReviewPage

class SchemaWebscraperReviewPage(WebscraperReviewPage):
    _schema_json = None
    @property
    def schema_json(self):
        if not self._schema_json:
            self._schema_json = json.loads(self.soup.findAll('script', {'type':"application/ld+json"})[0].string)
        if not self._schema_json:
            raise Exception('No schema on page')
        if self._schema_json['@type'] != 'Product':
            raise Exception('Not a product page')
        return self._schema_json


    def getProductInfo(self):
        return {
            'name': self.schema_json['name'],
            'category': self.schema_json['category']
        }

    def getReviewInfo(self):
        print("HERE")
        review_obj = self.schema_json['review']
        rating_obj = review_obj['reviewRating']

        rating_value = int(rating_obj['ratingValue'])
        rating_min = int(rating_obj['worstRating'])
        rating_max = int(rating_obj['bestRating'])
        rating = (rating_value - rating_min) / (rating_max - rating_min)
        return {
            'source': review_obj['publisher']['name'],
            'headline': review_obj['name'],
            'text': review_obj['reviewBody'],
            'rating': rating, # Out of 100
            'author': review_obj['author']['name'],
            'date': review_obj['datePublished']
        }