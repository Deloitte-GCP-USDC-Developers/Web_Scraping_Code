def upload_to_gbucket(file, dir):

    storage_client = Client()
    bucket = storage_client.bucket('dlt-sntmnt-source-file-web-scraping')
    blob = bucket.blob(file)
    blob.upload_from_filename(dir + file)