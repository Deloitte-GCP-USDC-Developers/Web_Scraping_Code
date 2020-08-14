import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'google-cloud-firestore'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'firebase_admin'])

import os
import pandas
import glob
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

command = 'gsutil cp gs://dlt-sntmnt-source-file-web-scraping/*.csv .'
os.system(command)

files = glob.glob('*.csv')
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'dlt-sntmnt-poc-284722',
})

db = firestore.client()
x = 0

for file in files:
    
    data = pandas.read_csv(file)

    for i in range(data.shape[0]):
        document_name = 'Product_Document'+str(x)+ '.' +str(i)
        db.collection(u'Product_Collection').document(document_name).set({
            u'Product_Name': unicode(data.loc[i,"Product Name"].decode('utf-8')),
            u'Product_Rating':data.loc[i,"Review Rating"] ,
            u'Product_Category':unicode(data.loc[i,"Product Category"].decode('utf-8')) 
        })

        db.collection(u'Product_Collection').document(document_name).collection(u'Review_Collection').document(u'Reveiw_Document').set({
            u'Review_Headline': unicode(data.loc[i,"Review Headline"].decode('utf-8')),
            u'Review_Rating': data.loc[i,"Review Rating"],
            u'Review_Source': unicode(data.loc[i,"Review Source"].decode('utf-8')),
            u'Review_Text': unicode(str(data.loc[i, "Review Text"]).decode('utf-8'))
        })
    x = x + 1
