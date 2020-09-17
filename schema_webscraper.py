import json
from abc import ABC, abstractmethod

from webscraper import WebscraperReviewPage, SkipPageException


class SchemaWebscraperReviewPage(WebscraperReviewPage):
    _schema_json = None

    def getAllJson(self):
        return self.soup.findAll('script', {'type':"application/ld+json"})
    
    def loadSchema(self, html):
        return json.loads(html.string)
    @property
    def schema_json(self):
        if not self._schema_json:
            for html in self.getAllJson():
                self._schema_json = self.loadSchema(html)
                if ('@type' in self._schema_json) and self._schema_json['@type'] == 'Product':
                    break
        if not self._schema_json:
            raise Exception('No schema on page')
        if self._schema_json['@type'] != 'Product':
            raise NotProductException(self.url)
        return self._schema_json

    PRODUCT_NAME_LABEL = 'name'
    PRODUCT_CATEGORY_LABEL = 'category'
    def getProductInfo(self):
        if 'name' not in self.schema_json:
            print(self.schema_json, self.url)
        return {
            'name': self.schema_json[self.PRODUCT_NAME_LABEL] if self.PRODUCT_NAME_LABEL in self.schema_json else '',
            'category': self.schema_json[self.PRODUCT_CATEGORY_LABEL] if self.PRODUCT_CATEGORY_LABEL in self.schema_json else ''
        }

    REVIEW_LABEL = 'review'
    REVIEW_RATING_LABEL = 'reviewRating'
    def getReviewInfo(self):
        review_obj = self.schema_json[self.REVIEW_LABEL]
        rating = -1
        if 'reviewRating' in review_obj:
            rating_obj = review_obj[self.REVIEW_RATING_LABEL]

            rating_value = float(rating_obj['ratingValue'])
            rating_min = float(rating_obj['worstRating']) if 'worstRating' in rating_obj else 0
            rating_max = float(rating_obj['bestRating'])
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