import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import json


class FireBaseHandler:
    def __init__(self):
        cred_json = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON'))
        print(cred_json)
        cred = credentials.Certificate(cred_json)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def addSong(self, song):
        if not self.isExistingSong(song['title'], song['artist']):
            doc_ref = self.db.collection('songs').add(song)
            return doc_ref[1].id
        else:
            print(f"Song {song['title']} by {song['artist']} already exists in the database.")
            return None
    
    def isExistingSong(self, song_title, artist_name):
        return self.db.collection('songs').where('title', '==', song_title).where('artist', '==', artist_name).get()


