import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'google-cloud-firestore'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'firebase_admin'])

import os
import pandas

command = 'gsutil cp gs://dlt-sntmnt-source-file-web-scraping/cnet_reviews.csv .'
os.system(command)

data = pandas.read_csv('cnet_reviews.csv')
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'dlt-sntmnt-poc-284722',
})

db = firestore.client()

db.collection(u'Product_Collection').document(u'Product_Document2').set({
    u'Product_Name': unicode(data.loc[0,"Product Name"]),
    u'Product_Rating':data.loc[0,"Review Rating"] ,
    u'Product_Category':unicode(data.loc[0,"Product Category"]) 
})

db.collection(u'Product_Collection').document(u'Product_Document2').collection(u'Review_Collection').document(u'Reveiw_Document').set({
    u'Review_Headline': unicode(data.loc[0,"Review Headline"]),
    u'Review_Rating': data.loc[0,"Review Rating"],
    u'Review_Source': unicode(data.loc[0,"Review Source"]),
    u'Review_Text': unicode(data.loc[0, "Review Text"].decode('utf-8'))
})
