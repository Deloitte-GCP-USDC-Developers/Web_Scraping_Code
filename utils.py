
from google.cloud.storage.client import Client
from google.cloud.storage.blob import Blob

def upload_to_gbucket(file, dir):
    storage_client = Client()
    bucket = storage_client.bucket('dlt-sntmnt-source-file-web-scraping')
    blob = bucket.blob(file)
    blob.upload_from_filename(dir + file)

def get_closest_match(search_term, search_results):

    max_distance = -1
    sum_distance = 0
    max_product = None
    for product in search_results:
        if product['distance'] > max_distance:
            max_distance = product['distance']
            max_product = product
        sum_distance = sum_distance + product['distance']