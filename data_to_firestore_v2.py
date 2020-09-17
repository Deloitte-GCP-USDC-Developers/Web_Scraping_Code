# Import and install necessary packages
import sys
import subprocess

# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'google-cloud-firestore'])
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'firebase_admin'])

import os
import pandas
import glob
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def unicode(string):
    return str(string) # 'utf-8')

# Pull csv files from GCP bucket and create a Firestore instance
command = 'gsutil cp gs://dlt-sntmnt-source-file-web-scraping/*.csv .'
os.system(command)

files = glob.glob('reviews*.csv')
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'dlt-sntmnt-poc-284722',
})

db = firestore.client()
x = 0

# Read and add data to Firestore for each csv file
for file in files:
    
    data = pandas.read_csv(file)
    
    # Add data to Firestore for each record
    for i in range(data.shape[0]):
        
        # Add a new Product Document to the Product Collection (Product information)
        document_name = 'Prod_'+''.join(unicode(data.loc[i,"Product Name"]).capitalize().split(' '))
        if not db.collection(u'Product_Collection').document(document_name).get().exists:
            db.collection(u'Product_Collection').document(document_name).set({
                u'Product_Name': unicode(data.loc[i,"Product Name"]),
                u'Product_Rating':int(data.loc[i,"Review Rating"]),
                u'Product_Category':unicode(data.loc[i,"Product Category"]) 
            })

        # Add a new Reveiw Document to the Product Document's Review Collection (Review information)
        db.collection(u'Product_Collection').document(document_name).collection(u'Review_Collection').document(u'Reveiw_Document').set({
            u'Review_Headline': unicode(data.loc[i,"Review Headline"]),
            u'Review_Rating': int(data.loc[i,"Review Rating"]),
            u'Review_Source': unicode(data.loc[i,"Review Source"]),
            u'Review_Text': unicode(str(data.loc[i, "Review Text"])),
            u'User_Ref': unicode('/User_Collection/User_Document'+str(x)+'.'+str(i))
        })
        
        # Add a new User Document to the User Collection (author information)
        document_name = 'User_Document'+str(x)+ '.' +str(i)
        db.collection(u'User_Collection').document(document_name).set({
            u'User_Name': unicode(data.loc[i,"Review Author"]) 
        })
    x = x + 1
