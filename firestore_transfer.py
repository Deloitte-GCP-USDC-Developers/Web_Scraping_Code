
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def init_firestore():
    firebase_admin.initialize_app()

    return firestore.client()

if __name__ == "__main__":
    db = init_firestore()

    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })