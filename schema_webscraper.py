import json
from abc import ABC, abstractmethod

from webscraper import WebscraperReviewPage, SkipPageException


class SchemaWebscraperReviewPage(WebscraperReviewPage):
    _schema_json = None
    @property
    def schema_json(self):
        if not self._schema_json:
            self._schema_json = json.loads(self.soup.findAll('script', {'type':"application/ld+json"})[0].string)
        if not self._schema_json:
            raise Exception('No schema on page')
        if self._schema_json['@type'] != 'Product':
            raise NotProductException(self.url)
        return self._schema_json


    def getProductInfo(self):
        if 'name' not in self.schema_json:
            print(self.schema_json, self.url)
        return {
            'name': self.schema_json['name'],
            'category': self.schema_json['category']
        }

    def getReviewInfo(self):
        review_obj = self.schema_json['review']
        rating = -1
        if 'reviewRating' in review_obj:
            rating_obj = review_obj['reviewRating']

            rating_value = int(rating_obj['ratingValue'])
            rating_min = int(rating_obj['worstRating'])
            rating_max = int(rating_obj['bestRating'])
            rating = round((rating_value - rating_min) / (rating_max - rating_min) * 100)
        return {
            'source': review_obj['publisher']['name'],
            'headline': review_obj['name'],
            'text': review_obj['reviewBody'],
            'rating': rating, # Out of 100
            'author': review_obj['author']['name'],
            'date': review_obj['datePublished']
        }

class NoSchemaException(SkipPageException):
    pass

class NotProductException(SkipPageException):
    pass